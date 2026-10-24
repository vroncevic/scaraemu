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
    Infrastructure adapter delegating dead zone bypass planning to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
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


class DeadZoneBypassAdapter:
    '''
        Adapter implementing dead zone bypass port via scaralang avoidance toolchain.

        It defines:

            :attributes:
                | _planner - Injected scaralang dead zone bypass planner service.
                | _validator - Injected scaralang dead zone validator service.
            :methods:
                | __init__ - Initializes adapter with injected scaralang collaborators.
                | plan_bypass - Computes bypass trajectory waypoints around dead zone.
                | is_segment_crossing_dead_zone - Checks if direct line traverses dead zone.
                | get_version - Returns adapter component version string.
    '''

    _planner: IDeadZoneBypassPlanner
    _validator: IDeadZoneValidator

    def __init__(
        self,
        *,
        planner: IDeadZoneBypassPlanner,
        validator: IDeadZoneValidator,
    ) -> None:
        '''
            Initializes the dead zone bypass adapter with injected scaralang services.

            :param planner: Injected IDeadZoneBypassPlanner instance.
            :param validator: Injected IDeadZoneValidator instance.
            :exceptions: None.
        '''
        self._planner: Final[IDeadZoneBypassPlanner] = planner
        self._validator: Final[IDeadZoneValidator] = validator

    def plan_bypass(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> list[ScaraPose]:
        '''
            Computes a collision-free bypass trajectory sequence around the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: Ordered list of intermediate Cartesian poses to destination.
            :exceptions: None.
        '''
        p1 = Point2D(x=start_pose.x, y=start_pose.y)
        p2 = Point2D(x=end_pose.x, y=end_pose.y)

        waypoints: list[Waypoint] = self._planner.plan_bypass(
            start_pt=p1,
            end_pt=p2,
            z=end_pose.z,
            speed=100.0,
        )

        return [
            ScaraPose(x=wp.x, y=wp.y, z=wp.z, phi=end_pose.phi)
            for wp in waypoints
        ]

    def is_segment_crossing_dead_zone(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Determines whether the direct line between poses traverses the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: True if segment crosses dead zone, False otherwise.
            :exceptions: None.
        '''
        p1 = Point2D(x=start_pose.x, y=start_pose.y)
        p2 = Point2D(x=end_pose.x, y=end_pose.y)

        return self._validator.is_segment_crossing_dead_zone(p1, p2)

    def get_version(self) -> str:
        '''
            Returns adapter component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
