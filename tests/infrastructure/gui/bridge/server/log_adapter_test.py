# -*- coding: UTF-8 -*-

'''
Module
    log_adapter_test.py
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
    Unit tests for ServerLogAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.bridge.server.log_adapter import ServerLogAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _CapturingLogListener:
    '''
        Capturing mock log listener for testing ServerLogAdapter.
    '''

    def __init__(self) -> None:
        '''
            Initializes capturing log listener.

            :exceptions: None.
        '''
        self.messages: list[tuple[str, str]] = []

    def append_log(self, text: str, tag: str) -> None:
        '''
            Captures log entry.

            :param text: Message text.
            :param tag: Tag name.
            :exceptions: None.
        '''
        self.messages.append((text, tag))

    def get_version(self) -> str:
        '''
            Returns mock component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class ServerLogAdapterTestCase(TestCase):
    '''
        Test cases verifying ServerLogAdapter bridging functionality.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies ServerLogAdapter matches IServerLogListener protocol.
                | test_on_server_log_normal - Verifies messages without error emoji receive host tag.
                | test_on_server_log_error - Verifies messages containing error emoji receive err tag.
                | test_get_version - Verifies version retrieval.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies ServerLogAdapter matches IServerLogListener protocol.

            :exceptions: None.
        '''
        adapter = ServerLogAdapter(_CapturingLogListener())
        self.assertIsInstance(adapter, IServerLogListener)

    def test_on_server_log_normal(self) -> None:
        '''
            Verifies messages without error emoji receive host tag.

            :exceptions: None.
        '''
        capturing = _CapturingLogListener()
        adapter = ServerLogAdapter(capturing)
        adapter.on_server_log('Server started on port 8888')
        self.assertEqual(len(capturing.messages), 1)
        self.assertEqual(capturing.messages[0], ('Server started on port 8888', 'host'))

    def test_on_server_log_error(self) -> None:
        '''
            Verifies messages containing error emoji receive err tag.

            :exceptions: None.
        '''
        capturing = _CapturingLogListener()
        adapter = ServerLogAdapter(capturing)
        adapter.on_server_log('❌ Connection refused')
        self.assertEqual(len(capturing.messages), 1)
        self.assertEqual(capturing.messages[0], ('❌ Connection refused', 'err'))

    def test_get_version(self) -> None:
        '''
            Verifies version retrieval.

            :exceptions: None.
        '''
        adapter = ServerLogAdapter(_CapturingLogListener())
        self.assertEqual(adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
