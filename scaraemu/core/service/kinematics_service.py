# -*- coding: UTF-8 -*-

'''
Module
    kinematics_service.py
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
    Analytical Forward and Inverse Kinematics solver implementation for 4-DOF SCARA robot.
'''

from __future__ import annotations

import math
from typing import ClassVar

from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.core.model.scara_step_coords import ScaraStepCoords
from scaraemu.core.model.kinematics_config_dto import KinematicsConfigDTO
from scaraemu.core.service.ikinematics_service import IKinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsService(IKinematicsService):
    '''
        Analytical Forward and Inverse Kinematics solver for 4-DOF SCARA robot.

        It defines:

            :attributes:
                | TWO_PI - Constant 2 * PI.
                | _geometry - Active ScaraGeometry model.
                | _config - Mechanical gearing and motor configuration.
                | _steps_per_rad_j1 - Step resolution for Joint 1 in steps/rad.
                | _steps_per_rad_j2 - Step resolution for Joint 2 in steps/rad.
                | _steps_per_rad_j4 - Step resolution for Joint 4 in steps/rad.
                | _steps_per_mm_z - Step resolution for Z axis in steps/mm.
            :methods:
                | __init__ - Initializes kinematic solver.
                | get_geometry - Returns active ScaraGeometry model.
                | update_geometry - Updates geometry parameters.
                | is_reachable - Validates Cartesian horizontal coordinates.
                | solve_ik - Computes inverse kinematics angles from pose.
                | solve_fk - Computes forward kinematics pose from joints.
                | joints_to_steps - Converts continuous joints to discrete motor step counts.
                | steps_to_joints - Converts motor step counts to continuous joint angles.
                | interpolate_linear - Generates fine linear Cartesian waypoints.
    '''

    TWO_PI: ClassVar[float] = 2.0 * math.pi

    _geometry: ScaraGeometry
    _config: KinematicsConfigDTO
    _steps_per_rad_j1: float
    _steps_per_rad_j2: float
    _steps_per_rad_j4: float
    _steps_per_mm_z: float

    def __init__(
        self,
        geometry: ScaraGeometry | None = None,
        config: KinematicsConfigDTO | None = None
    ) -> None:
        '''
            Initializes the kinematic solver with geometry and transmission specs.

            :param geometry: SCARA physical link lengths.
            :param config: Mechanical transmission specs.
            :exceptions: None.
        '''
        self._geometry = geometry if geometry is not None else ScaraGeometry()
        self._config = config if config is not None else KinematicsConfigDTO()
        self._recompute_constants()

    def _recompute_constants(self) -> None:
        '''
            Recomputes step conversion scaling factors based on active transmission config.

            :exceptions: None.
        '''
        full_steps_per_rev_j1: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j1
        )
        full_steps_per_rev_j2: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j2
        )
        full_steps_per_rev_j4: float = (
            self._config.steps_per_rev * self._config.microstepping * self._config.gear_ratio_j4
        )

        self._steps_per_rad_j1 = full_steps_per_rev_j1 / self.TWO_PI
        self._steps_per_rad_j2 = full_steps_per_rev_j2 / self.TWO_PI
        self._steps_per_rad_j4 = full_steps_per_rev_j4 / self.TWO_PI
        self._steps_per_mm_z = (
            self._config.steps_per_rev * self._config.microstepping
        ) / max(0.001, self._config.leadscrew_pitch_z)

    def get_geometry(self) -> ScaraGeometry:
        '''
            Returns active ScaraGeometry model.

            :return: ScaraGeometry instance.
            :exceptions: None.
        '''
        return self._geometry

    def update_geometry(self, geometry: ScaraGeometry) -> None:
        '''
            Updates geometry parameters.

            :param geometry: New ScaraGeometry instance.
            :exceptions: None.
        '''
        self._geometry = geometry

    def is_reachable(self, x: float, y: float) -> bool:
        '''
            Validates Cartesian horizontal coordinates.

            :param x: Target X coordinate in mm.
            :param y: Target Y coordinate in mm.
            :return: True if reachable, False otherwise.
            :exceptions: None.
        '''
        r: float = math.hypot(x, y)
        return self._geometry.r_min <= r <= self._geometry.r_max

    def solve_ik(self, pose: ScaraPose, elbow_left: bool = False) -> ScaraJoints:
        '''
            Computes analytical inverse kinematics for the SCARA arm.

            :param pose: Target Cartesian pose.
            :param elbow_left: True for Lefty / Elbow-Up, False for Righty / Elbow-Down.
            :return: Calculated joint angles and reachability flag.
            :exceptions: None.
        '''
        r_sq: float = pose.x * pose.x + pose.y * pose.y
        r: float = math.sqrt(r_sq)

        if r > self._geometry.r_max or r < self._geometry.r_min:
            return ScaraJoints(0.0, 0.0, pose.z, 0.0, reachable=False)

        l1: float = self._geometry.l1
        l2: float = self._geometry.l2

        cos_q2: float = (r_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
        cos_q2 = max(-1.0, min(1.0, cos_q2))

        sin_q2: float = math.sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
        if elbow_left:
            sin_q2 = -sin_q2

        theta2: float = math.atan2(sin_q2, cos_q2)

        k1: float = l1 + l2 * cos_q2
        k2: float = l2 * sin_q2
        theta1: float = math.atan2(pose.y, pose.x) - math.atan2(k2, k1)

        theta1 = self._normalize_angle(theta1)
        theta2 = self._normalize_angle(theta2)
        theta4: float = self._normalize_angle(pose.phi - (theta1 + theta2))

        return ScaraJoints(
            theta1=theta1,
            theta2=theta2,
            z=pose.z,
            theta4=theta4,
            reachable=True
        )

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Computes forward kinematics from joint positions to Cartesian pose.

            :param joints: Joint angles and positions.
            :return: Calculated Cartesian tool pose.
            :exceptions: None.
        '''
        q1: float = joints.theta1
        q2: float = joints.theta2
        l1: float = self._geometry.l1
        l2: float = self._geometry.l2

        x: float = l1 * math.cos(q1) + l2 * math.cos(q1 + q2)
        y: float = l1 * math.sin(q1) + l2 * math.sin(q1 + q2)
        phi: float = self._normalize_angle(q1 + q2 + joints.theta4)

        return ScaraPose(x=x, y=y, z=joints.z, phi=phi)

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

    def interpolate_linear(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
        segment_len_mm: float = 0.5
    ) -> list[ScaraPose]:
        '''
            Divides a straight Cartesian line into fine intermediate waypoints.

            :param start_pose: Start position.
            :param end_pose: End position.
            :param segment_len_mm: Maximum segment resolution in mm.
            :return: Ordered list of intermediate Cartesian waypoints.
            :exceptions: None.
        '''
        dx: float = end_pose.x - start_pose.x
        dy: float = end_pose.y - start_pose.y
        dz: float = end_pose.z - start_pose.z
        dphi: float = end_pose.phi - start_pose.phi

        distance: float = math.sqrt(dx * dx + dy * dy + dz * dz)
        if distance < 0.001 and abs(dphi) < 0.001:
            return [end_pose]

        num_segments: int = max(1, math.ceil(distance / max(0.01, segment_len_mm)))
        points: list[ScaraPose] = []

        for i in range(1, num_segments + 1):
            t: float = i / num_segments
            points.append(
                ScaraPose(
                    x=start_pose.x + dx * t,
                    y=start_pose.y + dy * t,
                    z=start_pose.z + dz * t,
                    phi=start_pose.phi + dphi * t
                )
            )

        return points

    def _normalize_angle(self, angle: float) -> float:
        '''
            Normalizes an angle to the [-pi, +pi] interval.

            :param angle: Input angle in radians.
            :return: Normalized angle in radians.
            :exceptions: None.
        '''
        while angle > math.pi:
            angle -= self.TWO_PI
        while angle < -math.pi:
            angle += self.TWO_PI
        return angle
