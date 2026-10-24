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
    Factory instantiating and assembling all scaralang subsystem adapters.
'''

from __future__ import annotations

from scaralang.core.service.kinematics.workspace.boundary.factory import BoundaryFactory

from scaraemu.infrastructure.scaralang.bypass.factory import DeadZoneBypassAdapterFactory
from scaraemu.infrastructure.scaralang.demo.factory import TrajectoryDemoAdapterFactory
from scaraemu.infrastructure.scaralang.dependencies import ScaralangDependencies
from scaraemu.infrastructure.scaralang.kinematics.linkage.factory import LinkageAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.factory import ProtocolFactory
from scaraemu.infrastructure.scaralang.provides import ScaralangProvides
from scaraemu.infrastructure.scaralang.reach.factory import WorkspaceReachAdapterFactory
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.scaralang.script.factory import ScriptLoaderAdapterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangFactory:
    '''
        Factory providing all scaralang infrastructure adapters bundled into ScaralangProvides.

        It defines:

            :methods:
                | create - Builds and bundles all scaralang adapters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ScaralangDependencies) -> ScaralangProvides:
        '''
            Builds and bundles all scaralang infrastructure adapters using supplied dependencies.

            :param dependencies: ScaralangDependencies containing manipulator bounds.
            :return: Immutable ScaralangProvides container.
            :exceptions: None.
        '''
        return ScaralangProvides(
            bypass=DeadZoneBypassAdapterFactory.create(bounds=dependencies.bounds),
            demo=TrajectoryDemoAdapterFactory.create(),
            linkage=LinkageAdapterFactory.create(bounds=dependencies.bounds),
            protocol=ProtocolFactory.create(),
            reach=WorkspaceReachAdapterFactory.create(bounds=dependencies.bounds),
            safety=MotionValidatorAdapterFactory.create(bounds=dependencies.bounds),
            script=ScriptLoaderAdapterFactory.create(),
            boundary=BoundaryFactory.create().service,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
