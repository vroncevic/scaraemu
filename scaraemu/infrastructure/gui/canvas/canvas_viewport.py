# -*- coding: UTF-8 -*-

'''
Module
    canvas_viewport.py
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
    Coordinate transformation and scaling viewport for 2D planar canvas.
'''

from __future__ import annotations

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewport:
    '''
        Calculates screen pixel projections and scaling for robot Cartesian workspace.

        It defines:

            :attributes:
                | _geometry - Active ScaraGeometry model.
                | _scale - Millimeters to canvas pixels scaling factor.
                | _center_x - Canvas origin center X pixel coordinate.
                | _center_y - Canvas origin center Y pixel coordinate.
                | _width_px - Canvas pixel width.
                | _height_px - Canvas pixel height.
            :methods:
                | __init__ - Initializes viewport metrics and scaling factor.
                | update_size - Updates canvas dimensions upon window resize.
                | world_to_screen - Converts world mm coordinates to canvas pixels.
                | screen_to_world - Converts canvas pixels back into world mm coordinates.
                | get_scale - Returns active scale multiplier.
                | get_dimensions - Returns current pixel dimensions.
                | get_center - Returns current center pixel coordinates.
    '''

    _geometry: ScaraGeometry
    _scale: float
    _center_x: float
    _center_y: float
    _width_px: float
    _height_px: float

    def __init__(
        self,
        geometry: ScaraGeometry,
        width: int = 480,
        height: int = 480
    ) -> None:
        '''
            Initializes viewport metrics and scaling factor.

            :param geometry: SCARA physical link lengths.
            :param width: Initial canvas pixel width.
            :param height: Initial canvas pixel height.
            :exceptions: None.
        '''
        self._geometry = geometry
        self._scale = 0.72
        self._width_px = float(width)
        self._height_px = float(height)
        self._center_x = width / 2.0
        self._center_y = height / 2.0

    def update_size(self, width: int, height: int) -> None:
        '''
            Updates canvas dimensions upon window resize and recalculates scaling.

            :param width: New width in pixels.
            :param height: New height in pixels.
            :exceptions: None.
        '''
        if width > 10 and height > 10:
            self._width_px = float(width)
            self._height_px = float(height)
            self._center_x = self._width_px / 2.0
            self._center_y = self._height_px / 2.0
            min_dim: float = min(self._width_px, self._height_px)
            self._scale = (min_dim * 0.42) / max(1.0, self._geometry.r_max)

    def world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        '''
            Converts world millimeter coordinates to screen pixel coordinates.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :return: Tuple of (screen_x, screen_y) in pixels.
            :exceptions: None.
        '''
        sx: float = self._center_x + x * self._scale
        sy: float = self._center_y - y * self._scale
        return sx, sy

    def screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        '''
            Converts screen pixel coordinates back to world millimeter coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :return: Tuple of (world_x, world_y) in mm.
            :exceptions: None.
        '''
        x: float = (sx - self._center_x) / max(0.001, self._scale)
        y: float = (self._center_y - sy) / max(0.001, self._scale)
        return x, y

    def get_scale(self) -> float:
        '''
            Returns active scale multiplier.

            :return: Scale factor.
            :exceptions: None.
        '''
        return self._scale

    def get_dimensions(self) -> tuple[float, float]:
        '''
            Returns current pixel dimensions (width, height).

            :return: Tuple of (width, height).
            :exceptions: None.
        '''
        return self._width_px, self._height_px

    def get_center(self) -> tuple[float, float]:
        '''
            Returns current center pixel coordinates (center_x, center_y).

            :return: Tuple of (center_x, center_y).
            :exceptions: None.
        '''
        return self._center_x, self._center_y
