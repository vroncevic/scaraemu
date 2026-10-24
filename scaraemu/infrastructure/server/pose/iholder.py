# -*- coding: UTF-8 -*-

'''
Module
    iholder.py
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
    Interface protocol for planned target pose caching state containers.
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
class IVirtualPlannedPoseHolder(Protocol):
    '''
        Structural interface protocol for planned target pose caching.

        It defines:

            :methods:
                | get_base_pose - Selects base pose according to active queue depth.
                | set_planned_pose - Updates cached planned pose.
                | reset - Clears cached planned pose.
                | get_version - Returns protocol version string.
    '''

    def get_base_pose(self, queue_depth: int, current_pose: ScaraPose) -> ScaraPose:
        '''
            Selects base pose according to active queue depth.

            :param queue_depth: Current trajectory queue depth count.
            :param current_pose: Live telemetry pose of robot arm.
            :return: Cached planned pose if valid and queued, otherwise current pose.
            :exceptions: None.
        '''

    def set_planned_pose(self, pose: ScaraPose) -> None:
        '''
            Updates cached planned target pose.

            :param pose: Target ScaraPose to record.
            :exceptions: None.
        '''

    def reset(self) -> None:
        '''
            Clears cached planned target pose.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
