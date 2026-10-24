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
    Factory creating ServerPreferenceRepository instances.
'''

from __future__ import annotations

from pathlib import Path
from typing import Final

from ats_utilities.context.bundle import ContextBundle

from scaraemu.infrastructure.preferences.server.repository import ServerPreferenceRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerPreferenceRepositoryFactory:
    '''
        Factory providing creational methods for ServerPreferenceRepository.

        It defines:

            :methods:
                | create - Creates repository with explicit configuration path and context bundle.
                | get_version - Returns factory version string.
    '''

    DEFAULT_CONFIG_FILE: Final[Path] = Path.home() / '.config' / 'scara' / 'server_config.json'

    @classmethod
    def create(
        cls,
        config_file: Path,
        context_bundle: ContextBundle,
    ) -> ServerPreferenceRepository:
        '''
            Creates server preferences repository with explicit storage path and context bundle.

            :param config_file: Explicit configuration file storage path.
            :param context_bundle: ATS context bundle for configuration I/O operations.
            :return: Configured ServerPreferenceRepository instance.
            :exceptions: None.
        '''
        return ServerPreferenceRepository(config_file, context_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
