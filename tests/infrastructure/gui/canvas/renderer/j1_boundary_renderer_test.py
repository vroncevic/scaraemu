# -*- coding: UTF-8 -*-

'''
Module
    j1_boundary_renderer_test.py
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
    Unit tests for J1BoundaryRenderer.
'''

from __future__ import annotations

from math import pi
from tkinter import Canvas
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService
from scaralang.core.service.kinematics.workspace.boundary.service import WorkspaceBoundaryService

from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.gui.canvas.renderer.j1_boundary_renderer import J1BoundaryRenderer
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJ1BoundaryRenderer(TestCase):
    '''
        Test cases verifying J1BoundaryRenderer limits check, polygon generation, and canvas rendering.

        It defines:

            :methods:
                | setUp - Sets up test fixture with mock canvas, transformer, and bounds.
                | test_is_j1_limited - Verifies is_j1_limited returns True when j1_max < pi and False when >= pi.
                | test_calculate_polygon_points - Verifies calculate_polygon_points produces expected coordinate vertices.
                | test_calculate_polygon_points_real_service - Verifies calculation with real boundary service.
                | test_render_when_limited - Verifies render draws polygon and text label when J1 limit is active.
                | test_render_when_unlimited - Verifies render skips drawing when J1 limit is at PI.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with mock canvas, transformer, and bounds.

            :exceptions: None.
        '''
        self._canvas: MagicMock = MagicMock(spec=Canvas)
        self._transformer: MagicMock = MagicMock(spec=ICoordinateTransformer)
        self._transformer.world_to_screen.side_effect = lambda x, y: (x + 300.0, y + 300.0)

        self._bounds_limited = ScaraBounds(
            links=LinkDimensions(l1=200.0, l2=150.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=500.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=1000.0
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.5,
                j1_max_rad=2.5,
                j2_min_rad=-2.6,
                j2_max_rad=2.6
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=10.0,
                singularity_theta2_min_rad=0.05,
                deadzone_r_min=50.0
            )
        )

        self._bounds_unlimited = ScaraBounds(
            links=LinkDimensions(l1=200.0, l2=150.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=500.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=1000.0
            ),
            joints=JointAngleBounds(
                j1_min_rad=-pi,
                j1_max_rad=pi,
                j2_min_rad=-pi,
                j2_max_rad=pi
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=10.0,
                singularity_theta2_min_rad=0.05,
                deadzone_r_min=50.0
            )
        )
        self._reach_adapter = MagicMock(spec=IWorkspaceReachAdapter)
        self._reach_adapter.get_safe_r_max.return_value = 345.0
        self._boundary_service = MagicMock(spec=IWorkspaceBoundaryService)
        self._boundary_service.calculate_forbidden_zone_polygon.return_value = (
            Point2D(x=100.0, y=50.0),
            Point2D(x=110.0, y=60.0),
            Point2D(x=120.0, y=70.0),
        )

    def test_is_j1_limited(self) -> None:
        '''
            Verifies is_j1_limited returns True when j1_max < pi and False when >= pi.

            :exceptions: None.
        '''
        self.assertTrue(J1BoundaryRenderer.is_j1_limited(self._bounds_limited))
        self.assertFalse(J1BoundaryRenderer.is_j1_limited(self._bounds_unlimited))

    def test_calculate_polygon_points(self) -> None:
        '''
            Verifies calculate_polygon_points produces expected coordinate vertices.

            :exceptions: None.
        '''
        pts = J1BoundaryRenderer.calculate_polygon_points(
            self._bounds_limited,
            self._transformer,
            self._boundary_service,
        )
        self.assertIsInstance(pts, list)
        self.assertEqual(pts, [400.0, 350.0, 410.0, 360.0, 420.0, 370.0])

    def test_calculate_polygon_points_real_service(self) -> None:
        '''
            Verifies calculate_polygon_points integration with real WorkspaceBoundaryService.

            :exceptions: None.
        '''
        real_service = WorkspaceBoundaryService()
        pts = J1BoundaryRenderer.calculate_polygon_points(
            self._bounds_limited,
            self._transformer,
            real_service,
        )
        self.assertIsInstance(pts, list)
        self.assertGreater(len(pts), 50)
        for val in pts:
            self.assertIsInstance(val, float)

    def test_render_when_limited(self) -> None:
        '''
            Verifies render draws polygon and text label when J1 limit is active.

            :exceptions: None.
        '''
        rendered: bool = J1BoundaryRenderer.render(
            self._canvas,
            self._bounds_limited,
            self._transformer,
            self._reach_adapter,
            self._boundary_service,
        )
        self.assertTrue(rendered)
        self._canvas.create_polygon.assert_called_once()
        self._canvas.create_text.assert_called_once()

    def test_render_when_unlimited(self) -> None:
        '''
            Verifies render skips drawing when J1 limit is at PI.

            :exceptions: None.
        '''
        rendered: bool = J1BoundaryRenderer.render(
            self._canvas,
            self._bounds_unlimited,
            self._transformer,
            self._reach_adapter,
            self._boundary_service,
        )
        self.assertFalse(rendered)
        self._canvas.create_polygon.assert_not_called()
        self._canvas.create_text.assert_not_called()

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertIsInstance(J1BoundaryRenderer.get_version(), str)


if __name__ == '__main__':
    unittest_main()
