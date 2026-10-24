# -*- coding: UTF-8 -*-

'''
Module
    coordinate_transformer.py
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
    Coordinate transformation between world millimeter space and canvas pixel space.
'''

from __future__ import annotations

from typing import Final

from scaraemu.infrastructure.gui.canvas.viewport.iviewport import IViewport

__author__ = 'Vladimir Roncevic'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CoordinateTransformer:
    '''
        Projects world Cartesian coordinates to and from 2D screen pixels.

        It defines:

            :attributes:
                | _viewport - Active canvas viewport metrics and scale provider.
            :methods:
                | __init__ - Initializes coordinate transformer with canvas viewport.
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts canvas screen pixels back into world mm coordinates.
                | get_version - Returns coordinate transformer component version string.
    '''

    _viewport: IViewport

    def __init__(self, viewport: IViewport) -> None:
        '''
            Initializes coordinate transformer with canvas viewport.

            :param viewport: Viewport providing dimensions and scaling factor.
            :exceptions: None.
        '''
        self._viewport: Final[IViewport] = viewport

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        '''
            Converts world millimeter coordinates to screen pixel coordinates.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :return: Tuple of (screen_x, screen_y) in pixels.
            :exceptions: None.
        '''
        width_px, height_px = self._viewport.get_dimensions()
        scale: float = self._viewport.get_scale()
        center_x: float = width_px / 2.0
        center_y: float = height_px / 2.0
        sx: float = center_x + x * scale
        sy: float = center_y - y * scale

        return sx, sy

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        '''
            Converts screen pixel coordinates back to world millimeter coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :return: Tuple of (world_x, world_y) in mm.
            :exceptions: None.
        '''
        width_px, height_px = self._viewport.get_dimensions()
        scale: float = self._viewport.get_scale()
        center_x: float = width_px / 2.0
        center_y: float = height_px / 2.0
        x: float = (sx - center_x) / max(0.001, scale)
        y: float = (center_y - sy) / max(0.001, scale)

        return x, y

    def get_version(self) -> str:
        '''
            Returns coordinate transformer component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
