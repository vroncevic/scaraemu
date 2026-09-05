# -*- coding: UTF-8 -*-

'''
Module
    kinematics_config_dto.py
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
    Defines SCARA transmission and stepper motor hardware configuration DTO.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class KinematicsConfigDTO:
    '''
        Mechanical gearing, leadscrew, and stepper motor resolution specs.

        It defines:

            :attributes:
                | steps_per_rev - Full steps per motor revolution.
                | microstepping - Microstepping multiplier.
                | gear_ratio_j1 - Shoulder reduction ratio.
                | gear_ratio_j2 - Elbow reduction ratio.
                | gear_ratio_j4 - Wrist reduction ratio.
                | leadscrew_pitch_z - Leadscrew pitch for Z axis in mm/rev.
    '''

    steps_per_rev: float = 200.0
    microstepping: float = 16.0
    gear_ratio_j1: float = 4.0
    gear_ratio_j2: float = 4.0
    gear_ratio_j4: float = 1.0
    leadscrew_pitch_z: float = 8.0
