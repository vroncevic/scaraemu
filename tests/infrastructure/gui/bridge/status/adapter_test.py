# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for StatusAdapter and IConnectionStatusView protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.bridge.status.adapter import StatusAdapter
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.toolbar.connection.istatus_view import IConnectionStatusView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatusAdapterTestCase(TestCase):
    '''
        Unit tests for StatusAdapter operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies StatusAdapter satisfies IConnectionStatusView.
                | test_set_connected_state - Verifies connection state propagates to layout builder.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies StatusAdapter satisfies IConnectionStatusView.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = StatusAdapter(layout_builder=mock_builder)
        self.assertIsInstance(adapter, IConnectionStatusView)
        self.assertEqual(adapter.get_version(), '1.0.2')

    def test_set_connected_state(self) -> None:
        '''
            Verifies connection state propagates to layout builder.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = StatusAdapter(layout_builder=mock_builder)
        adapter.set_connected_state(True)
        mock_builder.set_connected_state.assert_called_once_with(True)
        adapter.set_connected_state(False)
        mock_builder.set_connected_state.assert_called_with(False)


if __name__ == '__main__':
    unittest_main()
