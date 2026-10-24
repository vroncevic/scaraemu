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
    Structural protocol defining adapter port for workspace reach metrics.
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
class IWorkspaceReachAdapter(Protocol):
    '''
        Structural protocol defining adapter port for workspace reach metrics.

        It defines:

            :methods:
                | get_safe_r_min - Returns minimum safe annular reach radius in mm.
                | get_safe_r_max - Returns maximum safe reach radius considering singularity margin in mm.
                | calculate_home_pose - Calculates canonical default home Cartesian tool pose.
                | get_version - Returns adapter component version string.
    '''

    def get_safe_r_min(self) -> float:
        '''
            Returns minimum safe annular reach radius in mm.

            :return: Minimum reach radius in mm.
            :exceptions: None.
        '''

    def get_safe_r_max(self) -> float:
        '''
            Returns maximum safe reach radius considering singularity margin in mm.

            :return: Maximum reach radius in mm.
            :exceptions: None.
        '''

    def calculate_home_pose(self) -> ScaraPose:
        '''
            Calculates canonical default home Cartesian tool pose.

            :return: ScaraPose Cartesian tool pose instance.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
