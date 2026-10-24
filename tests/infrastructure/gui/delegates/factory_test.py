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
    Unit tests for GuiDelegatesFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaraemu.infrastructure.connection.provides import ConnectionProvides
from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.delegates.assembly import GuiDelegatesAssembly
from scaraemu.infrastructure.gui.delegates.dependencies import DelegatesDependencies
from scaraemu.infrastructure.gui.delegates.factory import GuiDelegatesFactory
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


class GuiDelegatesFactoryTestCase(TestCase):
    '''
        Unit tests for GuiDelegatesFactory.

        It defines:

            :methods:
                | test_create - Verifies GUI delegates assembly creation.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies GUI delegates assembly creation.

            :exceptions: None.
        '''
        bounds = ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=120.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0, max_speed=200.0, default_speed=50.0,
                default_accel=100.0, max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.6, j1_max_rad=2.6,
                j2_min_rad=-2.5, j2_max_rad=2.5,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=3.0,
                singularity_inner_margin_mm=3.0,
                singularity_theta2_min_rad=0.08,
                deadzone_r_min=20.0,
            ),
        )
        mock_services = MagicMock(spec=GuiServicesBundle)
        mock_adapters = MagicMock(spec=BridgeProvides)
        mock_connection = MagicMock(spec=ConnectionProvides)
        mock_streaming = MagicMock(spec=StreamingProvides)

        deps = DelegatesDependencies(
            bounds=bounds,
            services=mock_services,
            adapters=mock_adapters,
            connection=mock_connection,
            streaming=mock_streaming,
        )

        assembly = GuiDelegatesFactory.create(dependencies=deps)

        self.assertIsInstance(assembly, GuiDelegatesAssembly)
        self.assertIsNotNone(assembly.delegates)
        self.assertIsNotNone(assembly.target_click_coordinator)
        self.assertIsNotNone(assembly.server_manager)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(GuiDelegatesFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
