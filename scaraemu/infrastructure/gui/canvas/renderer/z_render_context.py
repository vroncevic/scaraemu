# -*- coding: UTF-8 -*-

'''
Module
    z_render_context.py
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
    Parameter bundle dataclass for Z-axis canvas rendering context.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ZRenderContext:
    '''
        Parameter bundle dataclass for Z-axis canvas rendering context.

        It defines:

            :attributes:
                | bounds - SCARA kinematics bounds and operational limits.
                | coordinate_mapper - Z coordinate to pixel translator.
                | width_px - Active canvas pixel width.
                | height_px - Active canvas pixel height.
    '''

    bounds: ScaraBounds
    coordinate_mapper: ZCoordinateMapper
    width_px: float
    height_px: float
