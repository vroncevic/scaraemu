# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for ScaraEmuGUI presentation engine.
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

from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.engine import ScaraEmuGUI
from scaraemu.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraEmuGUITestCase(TestCase):
    '''
        Unit tests verifying ScaraEmuGUI presentation engine.

        It defines:

            :methods:
                | setUp - Initializes test environment and collaborators.
                | test_initialization_status - Verifies is_initialized logic.
                | test_load_file - Verifies file loading delegation.
                | test_run_with_initial_parameters - Verifies run triggers server, script, and runner.
                | test_structural_protocol_typing - Verifies ScaraEmuGUI satisfies IGUI.
                | test_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Initializes test environment and collaborators.
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
        self.mock_script_delegate = MagicMock()
        self.mock_server_manager = MagicMock()
        self.mock_lifecycle_runner = MagicMock()

        delegates = GuiDelegatesBundle(
            jog=MagicMock(),
            config=MagicMock(),
            safety=MagicMock(),
            preset=MagicMock(),
            script=self.mock_script_delegate,
            serial_bar=MagicMock(),
            queue=MagicMock(),
        )
        self.gui = ScaraEmuGUI(
            bounds=bounds,
            target_click_listener=MagicMock(),
            delegates=delegates,
            server_manager=self.mock_server_manager,
            layout_builder=MagicMock(),
            lifecycle_runner=self.mock_lifecycle_runner,
            initial_script='/path/to/test.scara',
        )

    def test_initialization_status(self) -> None:
        '''
            Verifies is_initialized returns True when all components are configured.
        '''
        self.assertTrue(self.gui.is_initialized())

    def test_load_file(self) -> None:
        '''
            Verifies load_file delegates to event handler.
        '''
        self.gui.load_file('/demo/sample.scara')
        self.mock_script_delegate.handle_load_script.assert_called_once_with(
            '/demo/sample.scara'
        )

    def test_run_with_initial_parameters(self) -> None:
        '''
            Verifies run executes startup triggers and lifecycle runner.
        '''
        self.gui.run()
        self.mock_script_delegate.handle_load_script.assert_called_once_with(
            '/path/to/test.scara'
        )
        self.mock_lifecycle_runner.run_lifecycle.assert_called_once()

    def test_structural_protocol_typing(self) -> None:
        '''
            Verifies ScaraEmuGUI satisfies IGUI protocol structurally.
        '''
        self.assertIsInstance(self.gui, IGUI)

    def test_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.
        '''
        self.assertIsInstance(self.gui.get_version(), str)


if __name__ == '__main__':
    unittest_main()
