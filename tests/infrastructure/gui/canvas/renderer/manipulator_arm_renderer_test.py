# -*- coding: UTF-8 -*-

'''
Module
    manipulator_arm_renderer_test.py
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
    Unit tests for ManipulatorArmRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.pose.point_2d import Point2D

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.renderer.manipulator_render_context import ManipulatorRenderContext
from scaraemu.infrastructure.gui.canvas.renderer.manipulator_arm_renderer import ManipulatorArmRenderer
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter


class _MockTransformer:
    '''
        Mock coordinate transformer converting world to screen coordinates.
    '''

    def world_to_screen(self, wx: float, wy: float) -> tuple[float, float]:
        '''
            Transforms world coordinates to screen pixel coordinates.

            :param wx: Input wx.
            :param wy: Input wy.
            :exceptions: None.
        '''
        return wx + 100.0, wy + 100.0

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        '''
            Transforms screen coordinates to world coordinates.

            :param sx: Input sx.
            :param sy: Input sy.
            :exceptions: None.
        '''
        return sx - 100.0, sy - 100.0

    def get_version(self) -> str:
        '''
            Returns component version string.

            :exceptions: None.
        '''
        return '1.0.2'


class TestManipulatorArmRenderer(TestCase):
    '''
        Test cases verifying ManipulatorArmRenderer drawing and versioning.

        It defines:

            :methods:
                | test_render - Verifies lines and joint ovals are drawn on canvas.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_render(self) -> None:
        '''
            Verifies lines and joint ovals are drawn on canvas.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        transformer = _MockTransformer()
        pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        joints = ScaraJoints(
            theta1=0.5, theta2=0.3, z=10.0, theta4=0.8, reachable=True
        )

        mock_adapter = MagicMock(spec=ILinkageAdapter)
        mock_adapter.solve_fk_pose.return_value = (
            Point2D(x=100.0, y=0.0), Point2D(x=150.0, y=50.0)
        )
        context = ManipulatorRenderContext(
            transformer=transformer,
            manipulator_linkage_adapter=mock_adapter,
        )
        ManipulatorArmRenderer.render(
            mock_canvas, context, pose, joints
        )

        self.assertGreaterEqual(mock_canvas.create_line.call_count, 3)
        self.assertGreaterEqual(mock_canvas.create_oval.call_count, 3)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(ManipulatorArmRenderer.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
