# -*- coding: UTF-8 -*-

'''
Module
    kinematics_step_converter.py
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
    Converts between continuous joint angles/positions and discrete stepper motor steps.
'''

from __future__ import annotations

from math import pi
from typing import ClassVar

from scaraemu.core.model.kinematics.kinematics_config import KinematicsConfig
from scaraemu.core.model.kinematics.scara_joints import ScaraJoints
from scaraemu.core.model.kinematics.scara_step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsStepConverter:
    '''
        Bidirectional converter between continuous joint space and discrete motor step counts.

        It defines:

            :attributes:
                | TWO_PI - Constant 2 * PI.
                | _config - Mechanical gearing and motor configuration.
                | _steps_per_rad_j1 - Step resolution for Joint 1 in steps/rad.
                | _steps_per_rad_j2 - Step resolution for Joint 2 in steps/rad.
                | _steps_per_rad_j4 - Step resolution for Joint 4 in steps/rad.
                | _steps_per_mm_z - Step resolution for Z axis in steps/mm.
            :methods:
                | __init__ - Initializes step converter with mechanical transmission parameters.
                | update_config - Updates mechanical transmission configuration.
                | joints_to_steps - Converts joint positions to discrete motor steps.
                | steps_to_joints - Converts discrete motor steps back into joint positions.
    '''

    TWO_PI: ClassVar[float] = 2.0 * pi

    _config: KinematicsConfig
    _steps_per_rad_j1: float
    _steps_per_rad_j2: float
    _steps_per_rad_j4: float
    _steps_per_mm_z: float

    def __init__(self, config: KinematicsConfig | None = None) -> None:
        '''
            Initializes step converter with mechanical transmission specs.

            :param config: Mechanical transmission specs.
            :exceptions: None.
        '''
        self._config = config if config is not None else KinematicsConfig()
        self._recompute_constants()

    def update_config(self, config: KinematicsConfig) -> None:
        '''
            Updates transmission configuration and recalculates conversion factors.

            :param config: New mechanical transmission specs.
            :exceptions: None.
        '''
        self._config = config
        self._recompute_constants()

    def _recompute_constants(self) -> None:
        '''
            Recomputes step conversion scaling factors based on active transmission config.

            :exceptions: None.
        '''
        full_steps_j1: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j1
        )
        full_steps_j2: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j2
        )
        full_steps_j4: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j4
        )

        self._steps_per_rad_j1 = full_steps_j1 / self.TWO_PI
        self._steps_per_rad_j2 = full_steps_j2 / self.TWO_PI
        self._steps_per_rad_j4 = full_steps_j4 / self.TWO_PI
        self._steps_per_mm_z = (
            self._config.steps_per_rev * self._config.microstepping
        ) / max(0.001, self._config.leadscrew_pitch_z)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts radians and millimeters to discrete motor step counts.

            :param joints: Joint positions.
            :return: Discrete step coordinates.
            :exceptions: None.
        '''
        return ScaraStepCoords(
            j1_steps=round(joints.theta1 * self._steps_per_rad_j1),
            j2_steps=round(joints.theta2 * self._steps_per_rad_j2),
            z_steps=round(joints.z * self._steps_per_mm_z),
            j4_steps=round(joints.theta4 * self._steps_per_rad_j4)
        )

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts motor step counts back into joint angles.

            :param steps: Discrete step coordinates.
            :return: Joint positions.
            :exceptions: None.
        '''
        return ScaraJoints(
            theta1=steps.j1_steps / self._steps_per_rad_j1,
            theta2=steps.j2_steps / self._steps_per_rad_j2,
            z=steps.z_steps / self._steps_per_mm_z,
            theta4=steps.j4_steps / self._steps_per_rad_j4,
            reachable=True
        )
