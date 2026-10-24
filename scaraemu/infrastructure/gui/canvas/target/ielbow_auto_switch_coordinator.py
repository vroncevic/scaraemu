# -*- coding: UTF-8 -*-

'''
Module
    ielbow_auto_switch_coordinator.py
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
    Interface protocol for elbow configuration auto-switching.
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
class IElbowAutoSwitchCoordinator(Protocol):
    '''
        Defines structural contract for automatic elbow configuration switching.

        It defines:

            :methods:
                | try_auto_switch - Attempts switching elbow mode for an unreachable target pose.
                | get_version - Returns protocol version string.
    '''

    def try_auto_switch(self, target_pose: ScaraPose) -> bool:
        '''
            Attempts switching elbow mode for an unreachable target pose.

            :param target_pose: Target pose to evaluate with alternative elbow.
            :return: True if switch succeeded and target is reachable, False otherwise.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
            :exceptions: None.
        '''
