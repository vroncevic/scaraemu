# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for DelegatesDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.connection.provides import ConnectionProvides
from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.delegates.dependencies import DelegatesDependencies
from scaraemu.infrastructure.gui.services import GuiServicesBundle
from scaraemu.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DelegatesDependenciesTestCase(TestCase):
    '''
        Unit tests for DelegatesDependencies.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        mock_bounds = MagicMock(spec=ScaraBounds)
        mock_services = MagicMock(spec=GuiServicesBundle)
        mock_adapters = MagicMock(spec=BridgeProvides)
        mock_connection = MagicMock(spec=ConnectionProvides)
        mock_streaming = MagicMock(spec=StreamingProvides)

        bundle = DelegatesDependencies(
            bounds=mock_bounds,
            services=mock_services,
            adapters=mock_adapters,
            connection=mock_connection,
            streaming=mock_streaming,
        )

        self.assertIs(bundle.bounds, mock_bounds)
        self.assertIs(bundle.services, mock_services)
        self.assertIs(bundle.adapters, mock_adapters)
        self.assertIs(bundle.connection, mock_connection)
        self.assertIs(bundle.streaming, mock_streaming)


if __name__ == '__main__':
    unittest_main()
