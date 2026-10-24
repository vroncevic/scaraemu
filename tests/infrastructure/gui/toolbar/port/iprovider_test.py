# -*- coding: UTF-8 -*-

'''
Module
    iprovider_test.py
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
    Unit tests for IConnectionParameterProvider protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.toolbar.port.iprovider import IConnectionParameterProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyConnectionParameterProvider:
    '''
        Dummy provider for protocol conformance verification.
    '''

    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 115200) -> None:
        '''
            Tests init.

            :param port: Input port.
            :param baud: Input baud.
            :exceptions: None.
        '''
        self._port = port
        self._baud = baud

    def get_connection_parameters(self) -> tuple[str, int]:
        '''
            Tests get connection parameters.

            :exceptions: None.
        '''
        return (self._port, self._baud)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestConnectionParameterProvider(TestCase):
    '''
        Test cases verifying IConnectionParameterProvider protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy provider satisfies IConnectionParameterProvider protocol.
                | test_parameter_query - Verifies parameter queries and version inquiry.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy provider satisfies IConnectionParameterProvider protocol.

            :exceptions: None.
        '''
        provider = _DummyConnectionParameterProvider()
        self.assertIsInstance(provider, IConnectionParameterProvider)

    def test_parameter_query(self) -> None:
        '''
            Verifies parameter queries and version inquiry.

            :exceptions: None.
        '''
        provider = _DummyConnectionParameterProvider(port='/dev/ttyACM0', baud=9600)
        self.assertEqual(provider.get_connection_parameters(), ('/dev/ttyACM0', 9600))
        self.assertEqual(provider.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
