# -*- coding: UTF-8 -*-

'''
Module
    istatus_view_test.py
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
    Unit tests for IConnectionStatusView protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.toolbar.connection.istatus_view import IConnectionStatusView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyConnectionStatusView:
    '''
        Dummy implementation for IConnectionStatusView protocol conformance.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.states: list[bool] = []

    def set_connected_state(self, connected: bool) -> None:
        '''
            Tests set connected state.

            :param connected: Input connected.
            :exceptions: None.
        '''
        self.states.append(connected)

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestConnectionStatusView(TestCase):
    '''
        Test cases verifying IConnectionStatusView protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy satisfies IConnectionStatusView protocol.
                | test_set_connected_state - Verifies updating connection state and version inquiry.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy satisfies IConnectionStatusView protocol.

            :exceptions: None.
        '''
        view = _DummyConnectionStatusView()
        self.assertIsInstance(view, IConnectionStatusView)

    def test_set_connected_state(self) -> None:
        '''
            Verifies updating connection state and version inquiry.

            :exceptions: None.
        '''
        view = _DummyConnectionStatusView()
        view.set_connected_state(True)
        view.set_connected_state(False)

        self.assertEqual(view.states, [True, False])
        self.assertEqual(view.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
