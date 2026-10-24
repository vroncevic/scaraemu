# -*- coding: UTF-8 -*-

'''
Module
    z_renderer_test.py
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
    Unit test cases for ZRenderer.
'''

from __future__ import annotations

from tkinter import Canvas
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.renderer.z_render_context import ZRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper
from scaraemu.infrastructure.gui.canvas.renderer.z_renderer import ZRenderer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZRendererTestCase(TestCase):
    '''
        Test case verifying rendering behavior of ZRenderer.

        It defines:

            :methods:
                | setUp - Sets up test fixtures before each test method.
                | test_render_with_target - Verifies rendering creates lines, rectangle, oval, and text.
                | test_get_version - Verifies renderer returns valid version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.bounds = ScaraBounds(
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
        self.mapper = ZCoordinateMapper(self.bounds.vertical)
        self.canvas_mock = MagicMock(spec=Canvas)

    def test_render_with_target(self) -> None:
        '''
            Verifies rendering creates lines, rectangle, oval, and text.

            :exceptions: None.
        '''
        pose = ScaraPose(x=100.0, y=0.0, z=50.0, phi=0.0)
        target = ScaraPose(x=120.0, y=0.0, z=80.0, phi=0.0)
        context = ZRenderContext(
            bounds=self.bounds,
            coordinate_mapper=self.mapper,
            width_px=300.0,
            height_px=400.0,
        )
        ZRenderer.render(
            canvas=self.canvas_mock,
            context=context,
            pose=pose,
            current_target=target,
        )
        self.assertGreater(self.canvas_mock.create_line.call_count, 4)
        self.canvas_mock.create_rectangle.assert_called_once()
        self.canvas_mock.create_oval.assert_called_once()
        self.canvas_mock.create_text.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Verifies renderer returns valid version string.

            :exceptions: None.
        '''
        version = ZRenderer.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
