# -*- coding: UTF-8 -*-

'''
Module
    viewport.py
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
    Viewport metrics and scale factor calculation for 2D planar canvas.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.profile.link import LinkDimensions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Viewport:
    '''
        Calculates screen dimensions and scale factors for robot Cartesian workspace.

        It defines:

            :attributes:
                | _dimensions - Active LinkDimensions model.
                | _scale - Millimeters to canvas pixels scaling factor.
                | _width_px - Canvas pixel width.
                | _height_px - Canvas pixel height.
            :methods:
                | __init__ - Initializes viewport metrics and scaling factor.
                | update_size - Updates canvas dimensions upon window resize.
                | get_scale - Returns active scale multiplier.
                | get_dimensions - Returns current pixel dimensions.
                | get_version - Returns viewport component version string.
    '''

    _dimensions: LinkDimensions
    _scale: float
    _width_px: float
    _height_px: float

    def __init__(
        self,
        dimensions: LinkDimensions,
        width: int = 480,
        height: int = 480,
    ) -> None:
        '''
            Initializes viewport metrics and scaling factor.

            :param dimensions: SCARA physical link lengths.
            :param width: Initial canvas pixel width.
            :param height: Initial canvas pixel height.
            :exceptions: None.
        '''
        self._dimensions: Final[LinkDimensions] = dimensions
        self._scale = 0.72
        self._width_px = float(width)
        self._height_px = float(height)

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
            min_dim: float = min(self._width_px, self._height_px)
            r_max: float = self._dimensions.l1 + self._dimensions.l2
            self._scale = (min_dim * 0.42) / max(1.0, r_max)

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

    def get_version(self) -> str:
        '''
            Returns viewport component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
