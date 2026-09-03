# -*- coding: UTF-8 -*-

'''
Module
    telemetry_dto.py
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
    Defines SCARA live telemetry state Data Transfer Object.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.core.model.scara_step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class TelemetryDTO:
    '''
        Snapshot of full kinematic, Cartesian, and step telemetry data.

        It defines:

            :attributes:
                | pose - Cartesian ScaraPose.
                | joints - Joint angle ScaraJoints.
                | steps - Stepper pulse ScaraStepCoords.
                | is_hardware_connected - Hardware bridge active status flag.
                | motors_enabled - Stepper driver power enable status.
                | estop_active - Emergency stop active status flag.
                | hold_active - Feed-hold pause active status flag.
    '''

    pose: ScaraPose
    joints: ScaraJoints
    steps: ScaraStepCoords
    is_hardware_connected: bool = False
    motors_enabled: bool = True
    estop_active: bool = False
    hold_active: bool = False
