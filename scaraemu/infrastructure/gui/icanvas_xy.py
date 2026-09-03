# -*- coding: UTF-8 -*-

'''
Module
    icanvas_xy.py
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
    Defines interface for top planar XY workspace canvas.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable, Callable
from collections.abc import Sequence

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasXY(Protocol):
    '''
        Interface for top-down XY planar robot workspace canvas.

        It defines:

            :methods:
                | redraw - Renders robot links, reach boundaries, and path trail.
                | set_on_target_click - Registers click/drag callback for commanding XY coordinates.
    '''

    def redraw(
        self,
        pose: ScaraPose,
        joints: ScaraJoints,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose | None = None
    ) -> None:
        '''
            Renders robot links, reach boundaries, and path trail.

            :param pose: Current Cartesian pose.
            :param joints: Current articulated joint angles.
            :param trail_points: Sequence of historical trail points.
            :param current_target: Optional active target pose.
            :exceptions: None.
        '''
        ...

    def set_on_target_click(self, callback: Callable[[float, float], None]) -> None:
        '''
            Registers click/drag callback for commanding XY coordinates.

            :param callback: Callback accepting (x, y) coordinates in mm.
            :exceptions: None.
        '''
        ...
