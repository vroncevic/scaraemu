# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit test cases for BridgeProvides value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.gui.toolbar.connection.istatus_view import IConnectionStatusView
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.manager.ilistener import IServerStateListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BridgeProvidesTestCase(TestCase):
    '''
        Unit tests for BridgeProvides.

        It defines:

            :methods:
                | test_provides_attributes - Verifies provides attribute assignment.
    '''

    def test_provides_attributes(self) -> None:
        '''
            Verifies provides attribute assignment.

            :exceptions: None.
        '''
        mock_log = MagicMock(spec=ILogListener)
        mock_status = MagicMock(spec=IConnectionStatusView)
        mock_server_state = MagicMock(spec=IServerStateListener)
        mock_server_log = MagicMock(spec=IServerLogListener)
        mock_bridge = MagicMock(spec=IBridgeSynchronizer)

        provides = BridgeProvides(
            log_listener=mock_log,
            status_view=mock_status,
            server_state_listener=mock_server_state,
            server_log_listener=mock_server_log,
            bridge_synchronizer=mock_bridge,
        )

        self.assertIs(provides.log_listener, mock_log)
        self.assertIs(provides.status_view, mock_status)
        self.assertIs(provides.server_state_listener, mock_server_state)
        self.assertIs(provides.server_log_listener, mock_server_log)
        self.assertIs(provides.bridge_synchronizer, mock_bridge)


if __name__ == '__main__':
    unittest_main()
