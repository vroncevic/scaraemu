# -*- coding: UTF-8 -*-

'''
Module
    ihandler_test.py
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
    Unit tests for IResponseHandler protocol interface.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingResponseHandler:
    '''
        Stub satisfying IResponseHandler protocol structurally.
    '''

    def on_bytes(self, data: bytes) -> None:
        '''Handles bytes.'''
        _ = data

    def on_log(self, message: str) -> None:
        '''Handles log message.'''
        _ = message

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _NonConformingResponseHandler:
    '''
        Stub failing IResponseHandler protocol.
    '''

    def dummy_method(self) -> None:
        '''Dummy method.'''

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class TestIResponseHandler(TestCase):
    '''
        Unit tests verifying IResponseHandler runtime checkability.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Tests that structurally compliant stub satisfies protocol.
        '''
        handler = _ConformingResponseHandler()
        self.assertIsInstance(handler, IResponseHandler)

    def test_protocol_non_conformance(self) -> None:
        '''
            Tests that incomplete stub fails protocol check.
        '''
        handler = _NonConformingResponseHandler()
        self.assertNotIsInstance(handler, IResponseHandler)


if __name__ == '__main__':
    unittest_main()
