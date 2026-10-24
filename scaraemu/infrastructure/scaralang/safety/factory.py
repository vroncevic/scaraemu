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
    Factory instantiating MotionValidatorAdapter instances.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory

from scaraemu.infrastructure.scaralang.safety.adapter import MotionValidatorAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionValidatorAdapterFactory:
    '''
        Factory providing configured IMotionValidatorAdapter instances.

        It defines:

            :methods:
                | create - Builds an adapter configured from ScaraBounds model.
                | get_version - Returns factory version string representation.
    '''

    @classmethod
    def create(cls, bounds: ScaraBounds) -> IMotionValidatorAdapter:
        '''
            Builds and returns an IMotionValidatorAdapter instance from ScaraBounds.

            :param bounds: Injected ScaraBounds kinematic model.
            :return: Configured IMotionValidatorAdapter instance.
            :exceptions: None.
        '''
        validation_dependencies = DefaultValidationDependencies(bounds=bounds)
        validator: IDeadZoneValidator = (
            DefaultValidationFactory.create(dependencies=validation_dependencies).validator
        )
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DlsConfig(),
            )
        )

        return MotionValidatorAdapter(
            validator=validator,
            workspace=kinematics_provides.workspace,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
