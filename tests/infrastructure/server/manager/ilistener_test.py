# -*- coding: UTF-8 -*-

'''
Module
    ilistener_test.py
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
    Unit tests for IServerStateListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.manager.ilistener import IServerStateListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyServerStateListener:
    '''
        Dummy implementation for IServerStateListener protocol conformance.
    '''

    def __init__(self) -> None:
        self.state_events: list[tuple[bool, int]] = []

    def on_server_state(self, running: bool, port: int) -> None:
        '''
            Records server state notification.

            :param running: Server running state.
            :param port: Bound TCP port number.
            :exceptions: None.
        '''
        self.state_events.append((running, port))

    def get_version(self) -> str:
        '''
            Returns dummy version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestServerStateListener(TestCase):
    '''
        Test cases verifying IServerStateListener protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy satisfies protocol.
                | test_on_server_state - Verifies server state notification handling.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy satisfies IServerStateListener protocol.

            :exceptions: None.
        '''
        listener = _DummyServerStateListener()
        self.assertIsInstance(listener, IServerStateListener)

    def test_on_server_state(self) -> None:
        '''
            Verifies server state notification handling and version inquiry.

            :exceptions: None.
        '''
        listener = _DummyServerStateListener()
        listener.on_server_state(True, 8080)
        listener.on_server_state(False, 0)

        self.assertEqual(listener.state_events, [(True, 8080), (False, 0)])
        self.assertEqual(listener.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
