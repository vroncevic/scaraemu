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
    Factory for instantiating SystemHandler.
'''

from __future__ import annotations

from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies
from scaraemu.infrastructure.server.handler.system.handler import SystemHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SystemHandlerFactory:
    '''
        Factory providing instantiation of SystemHandler instances.

        It defines:

            :methods:
                | create - Builds and returns a SystemHandler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: SystemHandlerDependencies,
    ) -> SystemHandler:
        '''
            Builds and returns a SystemHandler instance.

            :param dependencies: Injected SystemHandlerDependencies instance.
            :return: SystemHandler instance.
            :exceptions: None.
        '''
        return SystemHandler(dependencies=dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
