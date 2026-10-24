# -*- coding: UTF-8 -*-

'''
Module
    holder_test.py
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
    Unit tests for ServerLogListenerHolder implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.logger.holder import ServerLogListenerHolder
from scaraemu.infrastructure.server.logger.iholder import IServerLogListenerHolder
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _RecordingServerLogListener:
    '''
        Recording listener for testing server log dispatching.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.logs: list[str] = []

    def on_server_log(self, message: str) -> None:
        '''
            Tests on server log.

            :param message: Input message.
            :exceptions: None.
        '''
        self.logs.append(message)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestServerLogListenerHolder(TestCase):
    '''
        Unit tests for ServerLogListenerHolder.

        It defines:

            :methods:
                | test_protocol_conformance - Tests that ServerLogListenerHolder satisfies protocols.
                | test_delegation_and_update - Tests forwarding events and updating listener target.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Tests that ServerLogListenerHolder satisfies protocols structurally.

            :exceptions: None.
        '''
        holder = ServerLogListenerHolder()
        self.assertIsInstance(holder, IServerLogListener)
        self.assertIsInstance(holder, IServerLogListenerHolder)

    def test_delegation_and_update(self) -> None:
        '''
            Tests forwarding events and updating listener target.

            :exceptions: None.
        '''
        holder = ServerLogListenerHolder()
        holder.on_server_log('unhandled message')

        rec = _RecordingServerLogListener()
        holder.set_listener(rec)
        holder.on_server_log('server started')

        self.assertEqual(rec.logs, ['server started'])
        self.assertIsInstance(holder.get_version(), str)


if __name__ == '__main__':
    unittest_main()
