# -*- coding: UTF-8 -*-

'''
Module
    icoordinate_transformer.py
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
    Structural protocol for 2D world-to-screen and screen-to-world coordinate transformations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICoordinateTransformer(Protocol):
    '''
        Structural protocol defining 2D canvas coordinate projections.

        It defines:

            :methods:
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts canvas screen pixels back into world mm coordinates.
                | get_version - Returns coordinate transformer protocol version string.
    '''

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        '''
            Converts world millimeter coordinates to screen pixel coordinates.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :return: Tuple of (screen_x, screen_y) in pixels.
            :exceptions: None.
        '''

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        '''
            Converts screen pixel coordinates back to world millimeter coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :return: Tuple of (world_x, world_y) in mm.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns coordinate transformer protocol version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
