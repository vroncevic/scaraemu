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
    Factory instantiating KinematicsAdapter instances.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

from scaraemu.infrastructure.scaralang.kinematics.solver.adapter import KinematicsAdapter
from scaraemu.infrastructure.scaralang.kinematics.solver.iadapter import IKinematicsAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsAdapterFactory:
    '''
        Factory providing KinematicsAdapter instances.

        It defines:

            :methods:
                | create - Builds an adapter from bounds and transmission models.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        bounds: ScaraBounds,
        transmission: TransmissionParameters,
    ) -> IKinematicsAdapter:
        '''
            Builds and returns a KinematicsAdapter instance from bounds and transmission.

            :param bounds: Robotic kinematic and workspace boundaries model.
            :param transmission: Motor transmission and step parameters model.
            :return: Configured IKinematicsAdapter instance.
            :exceptions: None.
        '''
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DlsConfig(),
            )
        )
        converter: IJointStepTransmissionConverter = (
            TransmissionFactory.create(transmission=transmission)
        )

        return KinematicsAdapter(
            planar=kinematics_provides.planar,
            converter=converter,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
