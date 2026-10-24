# -*- coding: UTF-8 -*-

'''
Module
    stepper.py
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
    Emulation motion step interpolator.
'''

from __future__ import annotations

from math import sqrt
from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationStepper:
    '''
        Computes Cartesian linear motion step interpolation for emulation.

        It defines:

            :attributes:
                | _speed_mm_per_sec - Feedrate speed in mm per second.
            :methods:
                | __init__ - Initializes the emulation stepper.
                | step_towards - Advances pose towards target pose by dt seconds.
                | get_version - Returns stepper version string.
    '''

    _speed_mm_per_sec: float

    def __init__(self, speed_mm_per_sec: float = 100.0) -> None:
        '''
            Initializes the emulation stepper.

            :param speed_mm_per_sec: Feedrate speed in mm per second.
            :exceptions: None.
        '''
        self._speed_mm_per_sec: Final[float] = speed_mm_per_sec

    def step_towards(
        self, current_pose: ScaraPose, target_pose: ScaraPose, dt: float
    ) -> tuple[ScaraPose, bool]:
        '''
            Advances pose towards target pose by dt seconds.

            :param current_pose: Current starting Cartesian pose.
            :param target_pose: Destination target Cartesian pose.
            :param dt: Time delta in seconds.
            :return: Tuple of resulting pose and boolean indicating arrival.
            :exceptions: None.
        '''
        dx: float = target_pose.x - current_pose.x
        dy: float = target_pose.y - current_pose.y
        dz: float = target_pose.z - current_pose.z
        dphi: float = target_pose.phi - current_pose.phi
        dist: float = sqrt(dx * dx + dy * dy + dz * dz)
        max_step: float = self._speed_mm_per_sec * dt

        if dist <= max_step or dist < 1e-6:
            return target_pose, True

        ratio: float = max_step / dist
        next_pose = ScaraPose(
            x=current_pose.x + dx * ratio,
            y=current_pose.y + dy * ratio,
            z=current_pose.z + dz * ratio,
            phi=current_pose.phi + dphi * ratio,
        )

        return next_pose, False

    def get_version(self) -> str:
        '''
            Returns stepper version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
