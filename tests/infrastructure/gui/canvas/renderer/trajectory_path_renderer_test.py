# -*- coding: UTF-8 -*-

'''
Module
    trajectory_path_renderer_test.py
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
    Unit tests for TrajectoryPathRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.canvas.renderer.trajectory_path_renderer import TrajectoryPathRenderer


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


class TestTrajectoryPathRenderer(TestCase):
    '''
        Test case for TrajectoryPathRenderer methods.

        It defines:

            :methods:
                | setUp - Initializes test mocks.
                | test_render_empty_path - Tests rendering empty trajectory path.
                | test_render_single_point - Tests rendering trajectory with single point.
                | test_render_multiple_points - Tests rendering trajectory with multiple points.
                | test_get_version - Tests component version query.
    '''

    def setUp(self) -> None:
        '''
            Initializes test mocks.

            :exceptions: None.
        '''
        self.canvas = MagicMock()
        self.transformer = _MockTransformer()

    def test_render_empty_path(self) -> None:
        '''
            Tests rendering empty trajectory path.

            :exceptions: None.
        '''
        TrajectoryPathRenderer.render(self.canvas, self.transformer, ())
        self.canvas.create_line.assert_not_called()
        self.canvas.create_oval.assert_not_called()

    def test_render_single_point(self) -> None:
        '''
            Tests rendering trajectory with single point.

            :exceptions: None.
        '''
        TrajectoryPathRenderer.render(self.canvas, self.transformer, ((10.0, 20.0),))
        self.canvas.create_line.assert_not_called()
        self.canvas.create_oval.assert_called_once()
        self.canvas.create_text.assert_called_once()

    def test_render_multiple_points(self) -> None:
        '''
            Tests rendering trajectory with multiple points.

            :exceptions: None.
        '''
        path = ((10.0, 20.0), (30.0, 40.0), (50.0, 60.0))
        TrajectoryPathRenderer.render(self.canvas, self.transformer, path)
        self.canvas.create_line.assert_called_once()
        self.assertEqual(self.canvas.create_oval.call_count, 3)
        self.assertEqual(self.canvas.create_text.call_count, 3)

    def test_get_version(self) -> None:
        '''
            Tests component version query.

            :exceptions: None.
        '''
        version = TrajectoryPathRenderer.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    unittest_main()
