# -*- coding: UTF-8 -*-

'''
Module
    imanipulator.py
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
    Defines abstract port protocol for SCARA manipulator kinematics operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IManipulatorKinematics(Protocol):
    '''
        Domain port protocol for SCARA manipulator forward/inverse kinematics and transmission.

        It defines:

            :methods:
                | solve_fk - Computes Cartesian tool pose from joint angles.
                | solve_ik - Solves articulated joint angles for a Cartesian pose.
                | steps_to_joints - Converts discrete stepper counts to joint angles.
                | joints_to_steps - Converts continuous joint angles to stepper counts.
    '''

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Computes forward kinematics for the specified joint configuration.

            :param joints: Articulated joint positions.
            :return: Cartesian tool pose.
        '''

    def solve_ik(self, pose: ScaraPose, elbow_left: bool) -> ScaraJoints:
        '''
            Computes inverse kinematics for the target Cartesian pose.

            :param pose: Target Cartesian tool pose.
            :param elbow_left: True for elbow-left configuration, False for right.
            :return: Calculated joint positions and reachability flag.
        '''

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts motor step counts into articulated joint angles.

            :param steps: Discrete motor step coordinates.
            :return: Articulated joint positions.
        '''

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts joint angles and vertical displacement into motor steps.

            :param joints: Articulated joint positions.
            :return: Discrete motor step coordinates.
        '''
