# -*- coding: UTF-8 -*-

'''
Module
    icanvas_z.py
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
    Defines interface for vertical Z elevation and reach canvas.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable, Callable

from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasZ(Protocol):
    '''
        Interface for vertical Z elevation and radial distance canvas.

        It defines:

            :methods:
                | redraw - Renders lead screw tower, carriage position, and vertical elevation.
                | set_on_target_click - Registers click/drag callback for commanding Z coordinate.
    '''

    def redraw(self, pose: ScaraPose, current_target: ScaraPose | None = None) -> None:
        '''
            Renders lead screw tower, carriage position, and vertical elevation.

            :param pose: Current Cartesian pose.
            :param current_target: Optional active target pose.
            :exceptions: None.
        '''
        ...

    def set_on_target_click(self, callback: Callable[[float], None]) -> None:
        '''
            Registers click/drag callback for commanding Z coordinate.

            :param callback: Callback accepting target Z height in mm.
            :exceptions: None.
        '''
        ...
