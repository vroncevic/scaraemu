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
    Infrastructure adapter delegating motion safety and dead zone validation to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionValidatorAdapter:
    '''
        Adapter implementing motion safety validation via scaralang dead zone and kinematics toolchains.

        It defines:

            :attributes:
                | _validator - Injected scaralang dead zone validator service.
                | _workspace - Injected scaralang workspace bounds evaluator.
            :methods:
                | __init__ - Initializes adapter with injected scaralang collaborators.
                | is_pose_valid - Checks whether Cartesian pose avoids dead zone and workspace limits.
                | is_segment_valid - Checks whether straight motion segment avoids dead zone.
                | get_version - Returns adapter component version string.
    '''

    _validator: IDeadZoneValidator
    _workspace: IWorkspaceBoundsEvaluator

    def __init__(
        self,
        *,
        validator: IDeadZoneValidator,
        workspace: IWorkspaceBoundsEvaluator,
    ) -> None:
        '''
            Initializes the motion validator adapter with injected scaralang services.

            :param validator: Injected IDeadZoneValidator instance.
            :param workspace: Injected IWorkspaceBoundsEvaluator instance.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = validator
        self._workspace: Final[IWorkspaceBoundsEvaluator] = workspace

    def is_pose_valid(self, pose: ScaraPose) -> bool:
        '''
            Checks whether Cartesian pose avoids the dead zone and falls within reachable envelope.

            :param pose: Target Cartesian tool pose.
            :return: True if pose is valid and reachable, False otherwise.
            :exceptions: None.
        '''
        if self._validator.is_point_in_dead_zone(pose.x, pose.y):
            return False

        in_bounds, _ = self._workspace.is_in_workspace(
            Point3D(x=pose.x, y=pose.y, z=pose.z)
        )

        return in_bounds

    def is_segment_valid(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Determines whether linear segment between poses avoids traversing the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: True if segment is safe and valid, False otherwise.
            :exceptions: None.
        '''
        if not self.is_pose_valid(start_pose):
            return False

        if not self.is_pose_valid(end_pose):
            return False

        p1 = Point2D(x=start_pose.x, y=start_pose.y)
        p2 = Point2D(x=end_pose.x, y=end_pose.y)

        return not self._validator.is_segment_crossing_dead_zone(p1, p2)

    def get_version(self) -> str:
        '''
            Returns adapter component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
