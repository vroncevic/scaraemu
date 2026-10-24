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
    Structural protocol defining adapter port for motion safety and dead zone validation.
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
class IMotionValidatorAdapter(Protocol):
    '''
        Structural protocol defining adapter port for motion safety and dead zone validation.

        It defines:

            :methods:
                | is_pose_valid - Checks whether Cartesian pose avoids dead zone and workspace limits.
                | is_segment_valid - Checks whether straight motion segment traverses dead zone.
                | get_version - Returns adapter component version string.
    '''

    def is_pose_valid(self, pose: ScaraPose) -> bool:
        '''
            Checks whether Cartesian pose avoids the dead zone and falls within reachable envelope.

            :param pose: Target Cartesian tool pose.
            :return: True if pose is valid and reachable, False otherwise.
            :exceptions: None.
        '''

    def is_segment_valid(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Checks whether direct line segment traverses the dead zone or breaches limits.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: True if segment does not intersect dead zone, False otherwise.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
