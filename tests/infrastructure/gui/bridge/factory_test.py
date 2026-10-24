# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit test cases for BridgeFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.bridge.factory import BridgeFactory
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.server.logger.holder import ServerLogListenerHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BridgeFactoryTestCase(TestCase):
    '''
        Unit tests for BridgeFactory.

        It defines:

            :methods:
                | test_create - Verifies GUI bridge adapters creation and registration.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies GUI bridge adapters creation and registration.

            :exceptions: None.
        '''
        mock_layout = MagicMock(spec=ILayoutBuilder)
        mock_holder = MagicMock(spec=ServerLogListenerHolder)

        bundle = BridgeFactory.create(
            layout_builder=mock_layout,
            server_log_holder=mock_holder,
        )

        self.assertIsInstance(bundle, BridgeProvides)
        mock_holder.set_listener.assert_called_once_with(bundle.server_log_listener)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(BridgeFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
