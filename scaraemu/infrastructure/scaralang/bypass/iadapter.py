# -*- coding: UTF-8 -*-

'''
Module
    iadapter.py
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
    Structural protocol defining adapter port for scaralang dead zone bypass services.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDeadZoneBypassAdapter(Protocol):
    '''
        Structural protocol defining adapter port for scaralang dead zone bypass services.

        It defines:

            :methods:
                | plan_bypass - Computes bypass trajectory waypoints around dead zone.
                | is_segment_crossing_dead_zone - Checks if straight motion crosses dead zone.
                | get_version - Returns adapter component version string.
    '''

    def plan_bypass(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> list[ScaraPose]:
        '''
            Computes a collision-free bypass trajectory sequence around the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: Sequence of intermediate and destination ScaraPose waypoints.
            :exceptions: None.
        '''

    def is_segment_crossing_dead_zone(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Checks whether direct line segment crosses through inner central dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: True if straight line intersects dead zone, False otherwise.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
