# -*- coding: UTF-8 -*-

'''
Module
    state_adapter_test.py
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
    Unit tests for ServerAdapter and IServerStateListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.bridge.server.state_adapter import ServerAdapter
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.server.manager.ilistener import IServerStateListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerAdapterTestCase(TestCase):
    '''
        Unit tests for ServerAdapter operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies ServerAdapter satisfies IServerStateListener.
                | test_on_server_state - Verifies server state propagates to layout builder.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies ServerAdapter satisfies IServerStateListener.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = ServerAdapter(layout_builder=mock_builder)
        self.assertIsInstance(adapter, IServerStateListener)
        self.assertEqual(adapter.get_version(), '1.0.2')

    def test_on_server_state(self) -> None:
        '''
            Verifies server state propagates to layout builder.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = ServerAdapter(layout_builder=mock_builder)
        adapter.on_server_state(True, 8888)
        mock_builder.set_server_state.assert_called_once_with(True, 8888)


if __name__ == '__main__':
    unittest_main()
