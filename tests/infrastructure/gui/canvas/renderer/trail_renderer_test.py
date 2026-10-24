# -*- coding: UTF-8 -*-

'''
Module
    trail_renderer_test.py
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
    Unit tests for TrailRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.renderer.trail_renderer import TrailRenderer


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


class TestTrailRenderer(TestCase):
    '''
        Test cases verifying TrailRenderer path trail and target drawing.

        It defines:

            :methods:
                | test_render_with_trail - Verifies trail line and target crosshair drawing.
                | test_render_without_trail - Verifies target crosshair drawing when trail is empty.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_render_with_trail(self) -> None:
        '''
            Verifies trail line and target crosshair drawing.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        transformer = _MockTransformer()
        trail_points = ((0.0, 0.0), (10.0, 10.0), (20.0, 20.0))
        target = ScaraPose(x=30.0, y=30.0, z=5.0, phi=0.0)

        TrailRenderer.render(mock_canvas, transformer, trail_points, target)

        self.assertGreaterEqual(mock_canvas.create_line.call_count, 3)

    def test_render_without_trail(self) -> None:
        '''
            Verifies target crosshair drawing when trail is empty.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        transformer = _MockTransformer()
        trail_points = ()
        target = ScaraPose(x=30.0, y=30.0, z=5.0, phi=0.0)

        TrailRenderer.render(mock_canvas, transformer, trail_points, target)

        self.assertGreaterEqual(mock_canvas.create_line.call_count, 2)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(TrailRenderer.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
