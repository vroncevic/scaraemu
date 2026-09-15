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

from math import pi, hypot, sqrt, atan2, cos, sin, degrees
from typing import ClassVar, Final

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.core.model.kinematics.scara_joints import ScaraJoints
from scaraemu.core.model.kinematics.scara_step_coords import ScaraStepCoords
from scaraemu.core.model.kinematics.kinematics_config import KinematicsConfig
from scaraemu.core.service.kinematics.kinematics_step_converter import KinematicsStepConverter
from scaraemu.core.service.kinematics.linear_path_interpolator import LinearPathInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsService:
    '''
        Analytical Forward and Inverse Kinematics solver for 4-DOF SCARA robot.

        It defines:

            :attributes:
                | TWO_PI - Constant 2 * PI.
                | _geometry - Active ScaraGeometry model.
                | _step_converter - KinematicsStepConverter for discrete step conversions.
            :methods:
                | __init__ - Initializes kinematic solver.
                | get_geometry - Returns active ScaraGeometry model.
                | update_geometry - Updates geometry parameters.
                | is_reachable - Validates Cartesian horizontal coordinates.
                | solve_ik - Computes inverse kinematics angles from pose.
                | diagnose_reachability - Diagnoses why a pose is reachable or unreachable.
                | solve_fk - Computes forward kinematics pose from joints.
                | joints_to_steps - Converts continuous joints to discrete motor step counts.
                | steps_to_joints - Converts motor step counts to continuous joint angles.
                | interpolate_linear - Generates fine linear Cartesian waypoints.
    '''

    TWO_PI: ClassVar[float] = 2.0 * pi

    _geometry: ScaraGeometry
    _step_converter: Final[KinematicsStepConverter]

    def __init__(
        self,
        geometry: ScaraGeometry | None = None,
        config: KinematicsConfig | None = None
    ) -> None:
        '''
            Initializes the kinematic solver with geometry and transmission specs.

            :param geometry: SCARA physical link lengths.
            :param config: Mechanical transmission specs.
            :exceptions: None.
        '''
        self._geometry = geometry if geometry is not None else ScaraGeometry()
        self._step_converter = KinematicsStepConverter(config=config)

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
            Validates Cartesian horizontal coordinates against safe reachable boundaries.

            :param x: Target X coordinate in mm.
            :param y: Target Y coordinate in mm.
            :return: True if reachable, False otherwise.
            :exceptions: None.
        '''
        r: float = hypot(x, y)
        return self._geometry.safe_r_min <= r <= self._geometry.safe_r_max

    def solve_ik(self, pose: ScaraPose, elbow_left: bool = False) -> ScaraJoints:
        '''
            Computes analytical inverse kinematics for the SCARA arm with safety boundaries.

            :param pose: Target Cartesian pose.
            :param elbow_left: True for Lefty / Elbow-Up, False for Righty / Elbow-Down.
            :return: Calculated joint angles and reachability flag.
            :exceptions: None.
        '''
        r_sq: float = pose.x * pose.x + pose.y * pose.y
        r: float = sqrt(r_sq)

        if (
            r > self._geometry.safe_r_max
            or r < self._geometry.safe_r_min
            or pose.z < self._geometry.z_min
            or pose.z > self._geometry.z_max
        ):
            return ScaraJoints(0.0, 0.0, pose.z, 0.0, reachable=False)

        l1: float = self._geometry.l1
        l2: float = self._geometry.l2

        cos_q2: float = (r_sq - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
        cos_q2 = max(-1.0, min(1.0, cos_q2))

        sin_q2: float = sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
        if elbow_left:
            sin_q2 = -sin_q2

        theta2: float = atan2(sin_q2, cos_q2)

        k1: float = l1 + l2 * cos_q2
        k2: float = l2 * sin_q2
        theta1: float = atan2(pose.y, pose.x) - atan2(k2, k1)

        theta1 = self._normalize_angle(theta1)
        theta2 = self._normalize_angle(theta2)
        theta4: float = self._normalize_angle(pose.phi - (theta1 + theta2))

        if (
            theta1 < self._geometry.j1_min_rad
            or theta1 > self._geometry.j1_max_rad
            or theta2 < self._geometry.j2_min_rad
            or theta2 > self._geometry.j2_max_rad
            or abs(theta2) < self._geometry.singularity_theta2_min_rad
            or abs(pi - abs(theta2)) < self._geometry.singularity_theta2_min_rad
        ):
            return ScaraJoints(theta1, theta2, pose.z, theta4, reachable=False)

        return ScaraJoints(
            theta1=theta1,
            theta2=theta2,
            z=pose.z,
            theta4=theta4,
            reachable=True
        )

    def diagnose_reachability(
        self, pose: ScaraPose, elbow_left: bool = False
    ) -> tuple[bool, str]:
        '''
            Diagnoses why a Cartesian pose is reachable or unreachable.

            :param pose: Target Cartesian pose.
            :param elbow_left: True for Lefty / Elbow-Up, False for Righty / Elbow-Down.
            :return: Tuple (is_reachable, detailed_reason).
            :exceptions: None.
        '''
        r: float = hypot(pose.x, pose.y)
        if r > self._geometry.safe_r_max:
            return (
                False,
                f'Radius R={r:.1f} mm exceeds outer limit R_max={self._geometry.safe_r_max:.1f} mm'
            )
        if r < self._geometry.safe_r_min:
            return (
                False,
                f'Radius R={r:.1f} mm is inside deadzone R_min={self._geometry.safe_r_min:.1f} mm'
            )
        if pose.z < self._geometry.z_min or pose.z > self._geometry.z_max:
            return (
                False,
                f'Elevation Z={pose.z:.1f} mm is out of range [{self._geometry.z_min:.1f}, {self._geometry.z_max:.1f}] mm'
            )

        joints: ScaraJoints = self.solve_ik(pose, elbow_left)
        if joints.reachable:
            return (True, 'Reachable')

        if (
            joints.theta1 < self._geometry.j1_min_rad
            or joints.theta1 > self._geometry.j1_max_rad
        ):
            deg1 = degrees(joints.theta1)
            min_deg = degrees(self._geometry.j1_min_rad)
            max_deg = degrees(self._geometry.j1_max_rad)
            return (
                False,
                f'Shoulder J1 angle {deg1:.1f}° exceeds limit [{min_deg:.1f}°, {max_deg:.1f}°]'
            )

        if (
            joints.theta2 < self._geometry.j2_min_rad
            or joints.theta2 > self._geometry.j2_max_rad
        ):
            deg2 = degrees(joints.theta2)
            min_deg = degrees(self._geometry.j2_min_rad)
            max_deg = degrees(self._geometry.j2_max_rad)
            return (
                False,
                f'Elbow J2 angle {deg2:.1f}° exceeds limit [{min_deg:.1f}°, {max_deg:.1f}°]'
            )

        if abs(joints.theta2) < self._geometry.singularity_theta2_min_rad:
            deg2 = degrees(abs(joints.theta2))
            min_deg = degrees(self._geometry.singularity_theta2_min_rad)
            return (
                False,
                f'Elbow J2 angle {deg2:.1f}° is in singularity deadband (< {min_deg:.1f}°)'
            )

        if abs(pi - abs(joints.theta2)) < self._geometry.singularity_theta2_min_rad:
            return (False, 'Arm is folded into boundary singularity')

        return (False, 'Unreachable kinematic configuration')

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

        x: float = l1 * cos(q1) + l2 * cos(q1 + q2)
        y: float = l1 * sin(q1) + l2 * sin(q1 + q2)
        phi: float = self._normalize_angle(q1 + q2 + joints.theta4)

        return ScaraPose(x=x, y=y, z=joints.z, phi=phi)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts radians and millimeters to discrete motor step counts.

            :param joints: Joint positions.
            :return: Discrete step coordinates.
            :exceptions: None.
        '''
        return self._step_converter.joints_to_steps(joints)

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts motor step counts back into joint angles.

            :param steps: Discrete step coordinates.
            :return: Joint positions.
            :exceptions: None.
        '''
        return self._step_converter.steps_to_joints(steps)

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
        return LinearPathInterpolator.interpolate(
            start_pose=start_pose,
            end_pose=end_pose,
            segment_len_mm=segment_len_mm
        )

    def _normalize_angle(self, angle: float) -> float:
        '''
            Normalizes an angle to the [-pi, +pi] interval.

            :param angle: Input angle in radians.
            :return: Normalized angle in radians.
            :exceptions: None.
        '''
        while angle > pi:
            angle -= self.TWO_PI
        while angle < -pi:
            angle += self.TWO_PI
        return angle
