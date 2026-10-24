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
    Unit tests for LayoutBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.gui.layout.builder.builder import LayoutBuilder
from scaraemu.infrastructure.gui.layout.builder.dependencies import LayoutDependencies
from scaraemu.infrastructure.gui.layout.builder.factory import LayoutBuilderFactory
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLayoutBuilderFactory(TestCase):
    '''
        Test cases verifying LayoutBuilderFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory creation wiring adapters from dependencies.
                | test_get_version - Verifies version query.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creation wiring adapters from dependencies.

            :exceptions: None.
        '''
        mock_scanner = MagicMock(spec=IPortScanner)
        mock_pref = MagicMock(spec=ISerialPreferenceRepository)
        mock_linkage = MagicMock(spec=ILinkageAdapter)
        mock_reach = MagicMock(spec=IWorkspaceReachAdapter)
        mock_boundary = MagicMock(spec=IWorkspaceBoundaryService)
        deps = LayoutDependencies(
            port_scanner=mock_scanner,
            preference_repository=mock_pref,
            manipulator_linkage_adapter=mock_linkage,
            reach_adapter=mock_reach,
            boundary_service=mock_boundary,
        )
        builder = LayoutBuilderFactory.create(dependencies=deps)
        self.assertIsInstance(builder, LayoutBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies version query.

            :exceptions: None.
        '''
        self.assertEqual(LayoutBuilderFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
