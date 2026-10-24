# -*- coding: UTF-8 -*-

'''
Module
    holder.py
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
    State container for caching planned target poses across chained move commands.
'''

from __future__ import annotations

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualPlannedPoseHolder:
    '''
        Maintains planned target pose state across chained move and jog commands.

        It defines:

            :attributes:
                | _planned_pose - Cached target pose for chained moves.
                | _has_planned_pose - Flag indicating whether planned pose is valid.
            :methods:
                | __init__ - Initializes planned pose state holder.
                | get_base_pose - Selects base pose according to active queue depth.
                | set_planned_pose - Updates cached planned pose.
                | reset - Clears cached planned pose.
                | get_version - Returns version string representation.
    '''

    _planned_pose: ScaraPose
    _has_planned_pose: bool

    def __init__(self) -> None:
        '''
            Initializes planned pose state holder.

            :exceptions: None.
        '''
        self._planned_pose = ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)
        self._has_planned_pose = False

    def get_base_pose(self, queue_depth: int, current_pose: ScaraPose) -> ScaraPose:
        '''
            Selects base pose according to active queue depth.

            :param queue_depth: Current trajectory queue depth count.
            :param current_pose: Live telemetry pose of robot arm.
            :return: Cached planned pose if valid and queued, otherwise current pose.
            :exceptions: None.
        '''
        if self._has_planned_pose and queue_depth > 0:
            return self._planned_pose

        return current_pose

    def set_planned_pose(self, pose: ScaraPose) -> None:
        '''
            Updates cached planned target pose.

            :param pose: Target ScaraPose to record.
            :exceptions: None.
        '''
        self._planned_pose = pose
        self._has_planned_pose = True

    def reset(self) -> None:
        '''
            Clears cached planned target pose.

            :exceptions: None.
        '''
        self._has_planned_pose = False

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
