# -*- coding: UTF-8 -*-

'''
Module
    icanvas_xy_test.py
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
    Unit tests for ICanvasXY protocol compliance.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyCanvasXY:
    '''
        Dummy planar canvas implementing ICanvasXY structurally.

        It defines:

            :methods:
                | redraw - Renders robot links and joints.
                | flash_unreachable - Flashes unreachable indicator.
    '''

    def redraw(
        self,
        pose: ScaraPose,
        joints: ScaraJoints,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose,
        planned_path: Sequence[tuple[float, float]] = (),
    ) -> None:
        '''
            Renders robot links and joints.

            :param pose: Current Cartesian pose.
            :param joints: Current articulated joint angles.
            :param trail_points: Sequence of historical trail points.
            :param current_target: Active target pose.
            :param planned_path: Sequence of planned trajectory (x, y) coordinates.
            :exceptions: None.
        '''
        _ = (pose, joints, trail_points, current_target, planned_path)

    def flash_unreachable(self, x: float, y: float) -> None:
        '''
            Flashes unreachable indicator.

            :param x: Target X Cartesian coordinate in mm.
            :param y: Target Y Cartesian coordinate in mm.
            :exceptions: None.
        '''
        _ = (x, y)


class TestICanvasXY(TestCase):
    '''
        Unit tests for ICanvasXY protocol.

        It defines:

            :methods:
                | test_protocol_compliance - Tests that dummy canvas satisfies ICanvasXY runtime check.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Tests that dummy canvas satisfies ICanvasXY runtime check.

            :exceptions: None.
        '''
        canvas = _DummyCanvasXY()
        self.assertIsInstance(canvas, ICanvasXY)


if __name__ == '__main__':
    unittest_main()
