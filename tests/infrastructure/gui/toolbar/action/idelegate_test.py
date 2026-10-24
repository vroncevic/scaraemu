# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for IActionDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyActionDelegate:
    '''
        Dummy delegate for IActionDelegate protocol conformance.
    '''

    def __init__(self) -> None:
        '''
            Initializes delegate tracking variables.

            :exceptions: None.
        '''
        self.connect_calls: list[tuple[str, int]] = []
        self.server_toggle_count: int = 0

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Records connect toggle event.

            :param port: Selected port path.
            :param baudrate: Transmission baud rate.
            :exceptions: None.
        '''
        self.connect_calls.append((port, baudrate))

    def handle_server_toggle(self) -> None:
        '''
            Records server toggle event.

            :exceptions: None.
        '''
        self.server_toggle_count += 1

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestActionDelegate(TestCase):
    '''
        Test cases verifying IActionDelegate protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy delegate satisfies IActionDelegate protocol.
                | test_delegation_actions - Verifies invocation of connect, server toggle, and version.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy delegate satisfies IActionDelegate protocol.

            :exceptions: None.
        '''
        delegate = _DummyActionDelegate()
        self.assertIsInstance(delegate, IActionDelegate)

    def test_delegation_actions(self) -> None:
        '''
            Verifies invocation of connect, server toggle, and version.

            :exceptions: None.
        '''
        delegate = _DummyActionDelegate()
        delegate.handle_connect_toggle('/dev/ttyUSB0', 115200)
        delegate.handle_server_toggle()

        self.assertEqual(delegate.connect_calls, [('/dev/ttyUSB0', 115200)])
        self.assertEqual(delegate.server_toggle_count, 1)
        self.assertEqual(delegate.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
