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
    Factory constructing and wiring the preferences subsystem components.
'''

from __future__ import annotations

from scaraemu.infrastructure.preferences.dependencies import PreferencesDependencies
from scaraemu.infrastructure.preferences.provides import PreferencesProvides
from scaraemu.infrastructure.preferences.serial.factory import SerialPreferenceRepositoryFactory
from scaraemu.infrastructure.preferences.serial.repository import SerialPreferenceRepository
from scaraemu.infrastructure.preferences.server.factory import ServerPreferenceRepositoryFactory
from scaraemu.infrastructure.preferences.server.repository import ServerPreferenceRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferencesFactory:
    '''
        Factory constructing and wiring the preferences subsystem components.

        It defines:

            :methods:
                | create - Instantiates and connects preferences repositories.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: PreferencesDependencies) -> PreferencesProvides:
        '''
            Instantiates and connects preferences repositories.

            :param dependencies: Preferences subsystem dependencies bundle.
            :return: PreferencesProvides bundle with wired repositories.
            :exceptions: None.
        '''
        serial_repo: SerialPreferenceRepository = (
            SerialPreferenceRepositoryFactory.create(
                config_file=dependencies.serial_config_file,
                context_bundle=dependencies.context_bundle,
            )
        )
        server_repo: ServerPreferenceRepository = (
            ServerPreferenceRepositoryFactory.create(
                config_file=dependencies.server_config_file,
                context_bundle=dependencies.context_bundle,
            )
        )

        return PreferencesProvides(
            serial=serial_repo,
            server=server_repo,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
