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
    Adapter delegating manipulator workspace reach and safety bounds to scaralang kinematics.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.envelope.ihome import IHomePoseCalculator

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceReachAdapter:
    '''
        Adapter delegating manipulator workspace reach and safety bounds to scaralang kinematics.

        It defines:

            :attributes:
                | _envelope - Injected scaralang workspace envelope collaborator.
                | _home_calculator - Injected scaralang home pose calculator collaborator.
            :methods:
                | __init__ - Initializes reach adapter with scaralang envelope and home services.
                | get_safe_r_min - Returns minimum safe annular reach radius in mm from scaralang kinematics.
                | get_safe_r_max - Returns maximum safe reach radius from scaralang kinematics.
                | calculate_home_pose - Calculates canonical default home Cartesian tool pose.
                | get_version - Returns adapter version string.
    '''

    _envelope: IWorkspaceEnvelope
    _home_calculator: IHomePoseCalculator

    def __init__(
        self,
        envelope: IWorkspaceEnvelope,
        home_calculator: IHomePoseCalculator,
    ) -> None:
        '''
            Initializes reach adapter with scaralang workspace envelope and home services.

            :param envelope: Injected IWorkspaceEnvelope protocol collaborator.
            :param home_calculator: Injected IHomePoseCalculator protocol collaborator.
            :exceptions: None.
        '''
        self._envelope: Final[IWorkspaceEnvelope] = envelope
        self._home_calculator: Final[IHomePoseCalculator] = home_calculator

    def get_safe_r_min(self) -> float:
        '''
            Returns minimum safe annular reach radius in mm from scaralang kinematics.

            :return: Minimum reach radius in mm.
            :exceptions: None.
        '''
        return self._envelope.r_min

    def get_safe_r_max(self) -> float:
        '''
            Returns maximum safe reach radius from scaralang kinematics.

            :return: Maximum safe reach radius in mm.
            :exceptions: None.
        '''
        return self._envelope.safe_r_max

    def calculate_home_pose(self) -> ScaraPose:
        '''
            Calculates canonical default home Cartesian tool pose from scaralang.

            :return: ScaraPose Cartesian tool pose instance.
            :exceptions: None.
        '''
        pose: CartesianPose = self._home_calculator.calculate_home_pose()

        return ScaraPose(x=pose.x, y=pose.y, z=pose.z, phi=pose.phi)

    def get_version(self) -> str:
        '''
            Returns adapter version string.

            :return: Component semantic version string.
            :exceptions: None.
        '''
        return __version__
