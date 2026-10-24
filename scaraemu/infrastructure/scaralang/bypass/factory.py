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
    Factory instantiating DeadZoneBypassAdapter instances.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies
from scaralang.infrastructure.trajectory.avoidance.bypass.factory import DefaultBypassFactory

from scaraemu.infrastructure.scaralang.bypass.adapter import DeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneBypassAdapterFactory:
    '''
        Factory providing configured IDeadZoneBypassAdapter instances.

        It defines:

            :methods:
                | create - Builds an adapter from ScaraBounds model.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        bounds: ScaraBounds,
    ) -> IDeadZoneBypassAdapter:
        '''
            Builds and returns an IDeadZoneBypassAdapter instance from ScaraBounds.

            :param bounds: Injected ScaraBounds kinematic model.
            :return: Configured IDeadZoneBypassAdapter instance.
            :exceptions: None.
        '''
        validation_dependencies = DefaultValidationDependencies(bounds=bounds)
        validator: IDeadZoneValidator = (
            DefaultValidationFactory.create(dependencies=validation_dependencies).validator
        )
        dependencies = DefaultBypassDependencies(
            validator=validator,
            safety_margin_mm=5.0,
        )
        planner: IDeadZoneBypassPlanner = (
            DefaultBypassFactory.create(dependencies=dependencies).planner
        )

        return DeadZoneBypassAdapter(
            planner=planner,
            validator=validator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
