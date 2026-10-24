# -*- coding: UTF-8 -*-

'''
Module
    ilog_listener_test.py
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
    Unit tests for ILogListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyLogListener:
    '''
        Dummy implementation for ILogListener protocol conformance.
    '''

    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.logs: list[tuple[str, str]] = []

    def append_log(self, message: str, tag: str) -> None:
        '''
            Tests append log.

            :param message: Input message.
            :param tag: Input tag.
            :exceptions: None.
        '''
        self.logs.append((message, tag))

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestLogListener(TestCase):
    '''
        Test cases verifying ILogListener protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy satisfies ILogListener protocol.
                | test_append_log - Verifies appending log messages with tags and version inquiry.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy satisfies ILogListener protocol.

            :exceptions: None.
        '''
        listener = _DummyLogListener()
        self.assertIsInstance(listener, ILogListener)

    def test_append_log(self) -> None:
        '''
            Verifies appending log messages with tags and version inquiry.

            :exceptions: None.
        '''
        listener = _DummyLogListener()
        listener.append_log('Connecting to port...', 'info')
        listener.append_log('OK', 'rx')

        self.assertEqual(
            listener.logs,
            [('Connecting to port...', 'info'), ('OK', 'rx')]
        )
        self.assertEqual(listener.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
