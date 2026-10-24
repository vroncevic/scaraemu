# -*- coding: UTF-8 -*-

'''
Module
    workspace_boundary_renderer_test.py
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
    Unit tests for WorkspaceBoundaryRenderer.
'''

from __future__ import annotations

from tkinter import Canvas
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.gui.canvas.viewport.viewport import Viewport
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.gui.canvas.renderer.workspace_boundary_renderer import WorkspaceBoundaryRenderer
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceBoundaryRenderer(TestCase):
    '''
        Test cases verifying WorkspaceBoundaryRenderer dead zone calculations and canvas rendering.

        It defines:

            :methods:
                | setUp - Sets up test fixture with mock canvas, viewport, transformer, and bounds.
                | test_get_version - Verifies get_version returns string.
                | test_render - Verifies complete canvas boundary overlay drawing and J1 delegation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with mock canvas, viewport, transformer, and bounds.

            :exceptions: None.
        '''
        self._canvas: MagicMock = MagicMock(spec=Canvas)
        self._viewport: MagicMock = MagicMock(spec=Viewport)
        self._transformer: MagicMock = MagicMock(spec=ICoordinateTransformer)
        self._transformer.world_to_screen.side_effect = lambda x, y: (x + 300.0, y + 300.0)
        self._viewport.get_dimensions.return_value = (600, 600)
        self._viewport.get_scale.return_value = 1.0

        self._bounds = ScaraBounds(
            links=LinkDimensions(l1=220.0, l2=160.0),
            vertical=VerticalBounds(z_min=5.0, z_max=120.0),
            speeds=SpeedLimits(
                min_speed=2.0,
                max_speed=400.0,
                default_speed=60.0,
                default_accel=120.0,
                max_accel=800.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.4,
                j1_max_rad=2.4,
                j2_min_rad=-2.5,
                j2_max_rad=2.5,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=4.0,
                singularity_inner_margin_mm=8.0,
                singularity_theta2_min_rad=0.06,
                deadzone_r_min=45.0,
            ),
        )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertIsInstance(WorkspaceBoundaryRenderer.get_version(), str)

    @patch('scaraemu.infrastructure.gui.canvas.renderer.workspace_boundary_renderer.J1BoundaryRenderer.render')
    def test_render(self, mock_j1_render: MagicMock) -> None:
        '''
            Verifies complete canvas boundary overlay drawing and J1 delegation.

            :param mock_j1_render: Input mock_j1_render.
            :exceptions: None.
        '''
        mock_reach_adapter = MagicMock(spec=IWorkspaceReachAdapter)
        mock_reach_adapter.get_safe_r_max.return_value = 345.0
        mock_reach_adapter.get_safe_r_min.return_value = 50.0
        mock_boundary_service = MagicMock(spec=IWorkspaceBoundaryService)

        WorkspaceBoundaryRenderer.render(
            self._canvas,
            self._bounds,
            self._viewport,
            self._transformer,
            mock_reach_adapter,
            mock_boundary_service,
        )

        self._canvas.create_rectangle.assert_called_once()
        self.assertEqual(self._canvas.create_oval.call_count, 2)
        self.assertEqual(self._canvas.create_text.call_count, 1)
        self.assertEqual(self._canvas.create_line.call_count, 2)
        mock_j1_render.assert_called_once_with(
            self._canvas,
            self._bounds,
            self._transformer,
            mock_reach_adapter,
            mock_boundary_service,
        )


if __name__ == '__main__':
    unittest_main()
