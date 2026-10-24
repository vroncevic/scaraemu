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
    Factory constructing and wiring the settings subsystem components.
'''

from __future__ import annotations

from scaraemu.infrastructure.settings.dependencies import SettingsDependencies
from scaraemu.infrastructure.settings.geometry.factory import GeometryLoaderFactory
from scaraemu.infrastructure.settings.geometry.loader import GeometryLoader
from scaraemu.infrastructure.settings.provides import SettingsProvides
from scaraemu.infrastructure.settings.transmission.factory import TransmissionLoaderFactory
from scaraemu.infrastructure.settings.transmission.loader import TransmissionLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SettingsFactory:
    '''
        Factory constructing and wiring the settings subsystem components.

        It defines:

            :methods:
                | create - Instantiates and connects settings loaders.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: SettingsDependencies) -> SettingsProvides:
        '''
            Instantiates and connects settings loaders.

            :param dependencies: Settings subsystem dependencies bundle.
            :return: SettingsProvides bundle with wired loaders.
            :exceptions: None.
        '''
        geometry_loader: GeometryLoader = GeometryLoaderFactory.create(
            context_bundle=dependencies.context_bundle
        )
        transmission_loader: TransmissionLoader = TransmissionLoaderFactory.create(
            context_bundle=dependencies.context_bundle
        )

        return SettingsProvides(
            geometry_loader=geometry_loader,
            transmission_loader=transmission_loader,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
