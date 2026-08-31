# -*- coding: UTF-8 -*-

'''
Module
    ikinematics_service.py
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
    Defines interface for analytical forward and inverse SCARA kinematics solver.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.scara_geometry import ScaraGeometry
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


@runtime_checkable
class IKinematicsService(Protocol):
    '''
        Interface for SCARA forward/inverse kinematics and transmission conversions.

        It defines:

            :methods:
                | get_geometry - Returns active ScaraGeometry model.
                | update_geometry - Updates geometry parameters.
                | is_reachable - Validates Cartesian horizontal coordinates.
                | solve_ik - Computes inverse kinematics angles from pose.
                | solve_fk - Computes forward kinematics pose from joints.
                | joints_to_steps - Converts continuous joints to discrete motor step counts.
                | steps_to_joints - Converts motor step counts to continuous joint angles.
                | interpolate_linear - Generates fine linear Cartesian waypoints.
    '''

    def get_geometry(self) -> ScaraGeometry:
        '''
            Returns active ScaraGeometry model.

            :return: ScaraGeometry instance.
            :exceptions: None.
        '''

    def update_geometry(self, geometry: ScaraGeometry) -> None:
        '''
            Updates geometry parameters.

            :param geometry: New ScaraGeometry instance.
            :exceptions: None.
        '''

    def is_reachable(self, x: float, y: float) -> bool:
        '''
            Validates Cartesian horizontal coordinates.

            :param x: Target X coordinate in mm.
            :param y: Target Y coordinate in mm.
            :return: True if reachable, False otherwise.
            :exceptions: None.
        '''

    def solve_ik(self, pose: ScaraPose, elbow_left: bool = False) -> ScaraJoints:
        '''
            Computes inverse kinematics angles from pose.

            :param pose: Target Cartesian pose.
            :param elbow_left: True for Lefty mode, False for Righty mode.
            :return: ScaraJoints solution.
            :exceptions: None.
        '''

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Computes forward kinematics pose from joints.

            :param joints: ScaraJoints position.
            :return: Computed Cartesian ScaraPose.
            :exceptions: None.
        '''

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts continuous joints to discrete motor step counts.

            :param joints: ScaraJoints position.
            :return: ScaraStepCoords instance.
            :exceptions: None.
        '''

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts motor step counts to continuous joint angles.

            :param steps: ScaraStepCoords instance.
            :return: ScaraJoints position.
            :exceptions: None.
        '''

    def interpolate_linear(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
        segment_len_mm: float = 0.5
    ) -> list[ScaraPose]:
        '''
            Generates fine linear Cartesian waypoints.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Ending Cartesian pose.
            :param segment_len_mm: Maximum segment resolution in mm.
            :return: List of interpolated intermediate ScaraPose instances.
            :exceptions: None.
        '''
