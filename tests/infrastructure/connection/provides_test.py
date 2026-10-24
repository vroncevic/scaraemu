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
    Unit test cases for ConnectionProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.connection.coordinator.icoordinator import IConnectionCoordinator
from scaraemu.infrastructure.connection.provides import ConnectionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionProvidesTestCase(TestCase):
    '''
        Test cases verifying ConnectionProvides container behavior.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores and exposes attributes.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle correctly stores and exposes attributes.
        '''
        mock_coordinator = MagicMock(spec=IConnectionCoordinator)
        mock_dispatcher = MagicMock(spec=ICommandDispatcher)

        bundle = ConnectionProvides(
            coordinator=mock_coordinator,
            command_dispatcher=mock_dispatcher,
        )

        self.assertIs(bundle.coordinator, mock_coordinator)
        self.assertIs(bundle.command_dispatcher, mock_dispatcher)


if __name__ == '__main__':
    unittest_main()
