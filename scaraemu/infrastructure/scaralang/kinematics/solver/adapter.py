# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating manipulator kinematics calculations to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

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


class KinematicsAdapter:
    '''
        Adapter implementing domain kinematics port via scaralang kinematics toolchain.

        It defines:

            :attributes:
                | _planar - Injected scaralang planar kinematics solver.
                | _converter - Injected scaralang joint step transmission converter.
            :methods:
                | __init__ - Initializes adapter with injected scaralang collaborators.
                | solve_fk - Computes Cartesian tool pose from joint angles.
                | solve_ik - Solves articulated joint angles for a Cartesian pose.
                | steps_to_joints - Converts discrete stepper counts to joint angles.
                | joints_to_steps - Converts continuous joint angles to stepper counts.
                | get_version - Returns adapter version string.
    '''

    _planar: IPlanarKinematicsSolver
    _converter: IJointStepTransmissionConverter

    def __init__(
        self,
        *,
        planar: IPlanarKinematicsSolver,
        converter: IJointStepTransmissionConverter,
    ) -> None:
        '''
            Initializes the kinematics adapter with injected scaralang services.

            :param planar: Injected IPlanarKinematicsSolver analytical solver.
            :param converter: Injected IJointStepTransmissionConverter step calculator.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = planar
        self._converter: Final[IJointStepTransmissionConverter] = converter

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Computes forward kinematics for the specified joint configuration.

            :param joints: Articulated joint positions.
            :return: Cartesian tool pose.
            :exceptions: None.
        '''
        point: Point2D = self._planar.solve_fk_2d(joints.theta1, joints.theta2)

        return ScaraPose(x=point.x, y=point.y, z=joints.z, phi=joints.theta4)

    def solve_ik(self, pose: ScaraPose, elbow_left: bool) -> ScaraJoints:
        '''
            Computes inverse kinematics for the target Cartesian pose.

            :param pose: Target Cartesian tool pose.
            :param elbow_left: True for elbow-left configuration, False for right.
            :return: Calculated joint positions and reachability flag.
            :exceptions: None.
        '''
        target_point: Point2D = Point2D(x=pose.x, y=pose.y)
        joints_2d: ScaraJoints2D = self._planar.solve_ik_2d(
            target_point, elbow_left=elbow_left
        )

        if not joints_2d.reachable:
            return ScaraJoints(
                theta1=0.0,
                theta2=0.0,
                z=pose.z,
                theta4=pose.phi,
                reachable=False,
            )

        return ScaraJoints(
            theta1=joints_2d.theta1,
            theta2=joints_2d.theta2,
            z=pose.z,
            theta4=pose.phi,
            reachable=True,
        )

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts motor step counts into articulated joint angles.

            :param steps: Discrete motor step coordinates.
            :return: Articulated joint positions.
            :exceptions: None.
        '''
        theta1, theta2, z, theta4 = self._converter.steps_to_angles(
            steps.j1_steps, steps.j2_steps, steps.z_steps, steps.j4_steps
        )

        return ScaraJoints(
            theta1=theta1,
            theta2=theta2,
            z=z,
            theta4=theta4,
            reachable=True,
        )

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts joint angles and vertical displacement into motor steps.

            :param joints: Articulated joint positions.
            :return: Discrete motor step coordinates.
            :exceptions: None.
        '''
        coords: JointStepCoordinates = self._converter.angles_to_steps(
            joints.theta1, joints.theta2, joints.z, joints.theta4
        )

        return ScaraStepCoords(
            j1_steps=coords.j1,
            j2_steps=coords.j2,
            z_steps=coords.z,
            j4_steps=coords.j4,
        )

    def get_version(self) -> str:
        '''
            Returns adapter version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
