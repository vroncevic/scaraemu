# -*- coding: UTF-8 -*-

'''
Module
    scara_geometry.py
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
    Defines SCARA physical link lengths and workspace geometric boundaries.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ScaraGeometry:
    '''
        SCARA physical link lengths and annular workspace geometric dimensions.

        It defines:

            :attributes:
                | l1 - Primary arm link length (mm).
                | l2 - Secondary arm link length (mm).
                | z_min - Minimum vertical height limit (mm).
                | z_max - Maximum vertical height limit (mm).
                | min_speed - Minimum allowable feedrate speed (mm/s).
                | max_speed - Maximum allowable feedrate speed (mm/s).
                | j1_min_rad - Joint 1 (shoulder) minimum angle limit (rad).
                | j1_max_rad - Joint 1 (shoulder) maximum angle limit (rad).
                | j2_min_rad - Joint 2 (elbow) minimum angle limit (rad).
                | j2_max_rad - Joint 2 (elbow) maximum angle limit (rad).
                | singularity_outer_margin_mm - Safety margin from outer reach limit (mm).
                | singularity_inner_margin_mm - Safety margin from inner reach limit (mm).
                | singularity_theta2_min_rad - Minimum elbow angle threshold (rad).
            :methods:
                | r_min - Inner radius of reachable annular workspace (mm).
                | r_max - Outer radius of reachable annular workspace (mm).
                | safe_r_min - Inner safe radius avoiding folded arm singularity (mm).
                | safe_r_max - Outer safe radius avoiding fully extended arm singularity (mm).
    '''

    l1: float = 150.0
    l2: float = 120.0
    z_min: float = 0.0
    z_max: float = 100.0
    min_speed: float = 1.0
    max_speed: float = 100.0
    j1_min_rad: float = -2.617994
    j1_max_rad: float = 2.617994
    j2_min_rad: float = -2.530727
    j2_max_rad: float = 2.530727
    singularity_outer_margin_mm: float = 3.0
    singularity_inner_margin_mm: float = 3.0
    singularity_theta2_min_rad: float = 0.087266

    @property
    def r_min(self) -> float:
        '''
            Inner radius of reachable annular workspace.

            :return: Minimum radial boundary in mm.
            :exceptions: None.
        '''
        return abs(self.l1 - self.l2)

    @property
    def r_max(self) -> float:
        '''
            Outer radius of reachable annular workspace.

            :return: Maximum radial boundary in mm.
            :exceptions: None.
        '''
        return self.l1 + self.l2

    @property
    def safe_r_min(self) -> float:
        '''
            Inner safe radius avoiding folded arm singularity.

            :return: Minimum safe radial distance in mm.
            :exceptions: None.
        '''
        return self.r_min + self.singularity_inner_margin_mm

    @property
    def safe_r_max(self) -> float:
        '''
            Outer safe radius avoiding fully extended arm singularity.

            :return: Maximum safe radial distance in mm.
            :exceptions: None.
        '''
        return self.r_max - self.singularity_outer_margin_mm
