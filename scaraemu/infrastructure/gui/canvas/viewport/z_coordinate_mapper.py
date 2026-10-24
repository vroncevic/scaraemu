# -*- coding: UTF-8 -*-

'''
Module
    z_coordinate_mapper.py
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
    Translates vertical Z coordinates between world mm and screen pixels.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZCoordinateMapper:
    '''
        Translates vertical Z coordinates between physical world mm and screen pixels.

        It defines:

            :attributes:
                | _bounds - Vertical bounds specification.
            :methods:
                | __init__ - Initializes mapper with vertical bounds.
                | z_to_screen_y - Converts physical Z height to screen pixel coordinate.
                | screen_y_to_z - Converts screen pixel coordinate to physical Z height.
                | get_version - Returns coordinate mapper component version.
    '''

    _bounds: VerticalBounds

    def __init__(self, bounds: VerticalBounds) -> None:
        '''
            Initializes coordinate mapper with vertical bounds.

            :param bounds: Injected VerticalBounds instance.
            :exceptions: None.
        '''
        self._bounds: Final[VerticalBounds] = bounds

    def z_to_screen_y(self, z: float, bottom_y: float, top_y: float) -> float:
        '''
            Maps physical Z in mm to canvas screen Y in pixels.

            :param z: Z elevation in mm.
            :param bottom_y: Bottom pixel coordinate (Z=0).
            :param top_y: Top pixel coordinate (Z=Zmax).
            :return: Screen Y coordinate.
            :exceptions: None.
        '''
        z_min: float = self._bounds.z_min
        z_max: float = self._bounds.z_max
        z_clamped: float = max(z_min, min(z_max, z))
        span_z: float = max(1.0, z_max - z_min)
        ratio: float = (z_clamped - z_min) / span_z
        return bottom_y - ratio * (bottom_y - top_y)

    def screen_y_to_z(self, sy: float, bottom_y: float, top_y: float) -> float:
        '''
            Maps screen Y pixel coordinate back to physical Z in mm.

            :param sy: Screen Y coordinate in pixels.
            :param bottom_y: Bottom pixel coordinate (Z=0).
            :param top_y: Top pixel coordinate (Z=Zmax).
            :return: Clamped Z elevation in mm.
            :exceptions: None.
        '''
        z_min: float = self._bounds.z_min
        z_max: float = self._bounds.z_max
        ratio: float = (bottom_y - sy) / max(1.0, bottom_y - top_y)
        z: float = z_min + ratio * (z_max - z_min)
        return max(z_min, min(z_max, z))

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
