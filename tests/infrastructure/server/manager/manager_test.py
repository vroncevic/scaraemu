# -*- coding: UTF-8 -*-

'''
Module
    manager_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaraemu is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaraemu is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for VirtualServerManager.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.manager.imanager import IVirtualServerManager
from scaraemu.infrastructure.server.manager.manager import VirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockRobotServer:
    '''
        Mock robot server for manager testing.
    '''

    def __init__(self, start_success: bool = True) -> None:
        self.running: bool = False
        self.start_success: bool = start_success
        self.started_port: int = 0

    def is_running(self) -> bool:
        '''
            Checks running state.

            :exceptions: None.
        '''
        return self.running

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts server.

            :param host: Host string.
            :param port: Port integer.
            :exceptions: None.
        '''
        self.started_port = port
        if self.start_success:
            self.running = True
            return True
        return False

    def stop(self) -> None:
        '''
            Stops server.

            :exceptions: None.
        '''
        self.running = False

    def get_version(self) -> str:
        '''
            Returns version string.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockLogListener:
    '''
        Mock log listener for manager testing.
    '''

    def __init__(self) -> None:
        self.logs: list[str] = []

    def on_server_log(self, message: str) -> None:
        '''
            Records server log message.

            :param message: Input message.
            :exceptions: None.
        '''
        self.logs.append(message)

    def get_version(self) -> str:
        '''
            Returns version string.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockStateListener:
    '''
        Mock state listener for manager testing.
    '''

    def __init__(self) -> None:
        self.states: list[tuple[bool, int]] = []

    def on_server_state(self, running: bool, port: int) -> None:
        '''
            Records server state change.

            :param running: Running state.
            :param port: Port integer.
            :exceptions: None.
        '''
        self.states.append((running, port))

    def get_version(self) -> str:
        '''
            Returns version string.

            :exceptions: None.
        '''
        return '1.0.2'


class VirtualServerManagerTestCase(TestCase):
    '''
        Tests for VirtualServerManager operations and protocol conformity.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies satisfies IVirtualServerManager.
                | test_toggle_start_success - Verifies successful server start toggling.
                | test_toggle_stop_when_running - Verifies stopping server when toggled while running.
                | test_toggle_failure - Verifies error handling when server fails to start.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies VirtualServerManager satisfies IVirtualServerManager.

            :exceptions: None.
        '''
        server = _MockRobotServer()
        log_listener = _MockLogListener()
        state_listener = _MockStateListener()
        manager = VirtualServerManager(
            server=server,
            log_listener=log_listener,
            state_listener=state_listener,
        )
        self.assertIsInstance(manager, IVirtualServerManager)
        self.assertEqual(manager.get_version(), '1.0.2')

    def test_toggle_start_success(self) -> None:
        '''
            Verifies successful server start toggling.

            :exceptions: None.
        '''
        server = _MockRobotServer(start_success=True)
        log_listener = _MockLogListener()
        state_listener = _MockStateListener()
        manager = VirtualServerManager(
            server=server,
            log_listener=log_listener,
            state_listener=state_listener,
        )

        result: bool = manager.toggle(port=8888)
        self.assertTrue(result)
        self.assertTrue(manager.is_running())
        self.assertEqual(state_listener.states, [(True, 8888)])
        self.assertEqual(len(log_listener.logs), 1)
        self.assertIn('8888', log_listener.logs[0])

    def test_toggle_stop_when_running(self) -> None:
        '''
            Verifies stopping server when toggled while already running.

            :exceptions: None.
        '''
        server = _MockRobotServer(start_success=True)
        log_listener = _MockLogListener()
        state_listener = _MockStateListener()
        manager = VirtualServerManager(
            server=server,
            log_listener=log_listener,
            state_listener=state_listener,
        )

        manager.toggle(port=9999)
        self.assertTrue(manager.is_running())

        result: bool = manager.toggle(port=9999)
        self.assertFalse(result)
        self.assertFalse(manager.is_running())
        self.assertEqual(state_listener.states, [(True, 9999), (False, 0)])
        self.assertIn('stopped', log_listener.logs[-1])

    def test_toggle_failure(self) -> None:
        '''
            Verifies error handling when server fails to start.

            :exceptions: None.
        '''
        server = _MockRobotServer(start_success=False)
        log_listener = _MockLogListener()
        state_listener = _MockStateListener()
        manager = VirtualServerManager(
            server=server,
            log_listener=log_listener,
            state_listener=state_listener,
        )

        result: bool = manager.toggle(port=8888)
        self.assertFalse(result)
        self.assertFalse(manager.is_running())
        self.assertEqual(state_listener.states, [(False, 0)])
        self.assertIn('Failed', log_listener.logs[-1])


if __name__ == '__main__':
    unittest_main()
