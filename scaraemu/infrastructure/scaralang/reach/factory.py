# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating WorkspaceReachAdapter with scaralang kinematics service.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.envelope.home import HomePoseCalculator
from scaralang.core.service.kinematics.envelope.home_factory import HomePoseCalculatorFactory
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.provides import KinematicsProvides

from scaraemu.infrastructure.scaralang.reach.adapter import WorkspaceReachAdapter
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceReachAdapterFactory:
    '''
        Factory instantiating WorkspaceReachAdapter with scaralang kinematics service.

        It defines:

            :methods:
                | create - Creates WorkspaceReachAdapter from active robot geometry bounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, bounds: ScaraBounds) -> IWorkspaceReachAdapter:
        '''
            Creates WorkspaceReachAdapter from active robot geometry bounds.

            :param bounds: Kinematic limits and geometry bounds model.
            :return: Instantiated IWorkspaceReachAdapter.
            :exceptions: None.
        '''
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DlsConfig(),
            )
        )
        home_calc: HomePoseCalculator = HomePoseCalculatorFactory.create(bounds=bounds)

        return WorkspaceReachAdapter(
            envelope=kinematics_provides.envelope,
            home_calculator=home_calc,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Component semantic version string.
            :exceptions: None.
        '''
        return __version__
