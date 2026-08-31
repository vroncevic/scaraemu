# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the CLI bundle.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar
from types import MappingProxyType

from ats_utilities.option.imanager import IOptionManager

from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleKeys:
    '''
        Runtime components and interface constraints for the CLI bundle.

        It defines:

            :attributes:
                | DEPENDENCY_SERVICE - The service interface constant of the CLI bundle.
                | DEPENDENCY_PARSER - The parser interface constant of the CLI bundle.
                | DEPENDENCY_COMMANDS - The commands constant of the CLI bundle.
                | OPTION_SERVICE - The service option constant of the CLI bundle.
                | OPTION_PARSER - The parser option constant of the CLI bundle.
                | OPTION_GUI - The GUI option constant of the CLI bundle.
            :methods:
                | get_dependency_to_type - Returns mapping of CLI dependencies to types.
                | get_option_to_type - Returns mapping of CLI options to types.
    '''

    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_PARSER: ClassVar[str] = 'parser'
    DEPENDENCY_COMMANDS: ClassVar[str] = 'commands'

    OPTION_SERVICE: ClassVar[str] = 'service'
    OPTION_PARSER: ClassVar[str] = 'parser'
    OPTION_GUI: ClassVar[str] = 'gui'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the CLI bundle dependencies to their types.

            :return: The mapping of the CLI bundle dependencies to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_PARSER: IOptionManager,
            cls.DEPENDENCY_COMMANDS: Sequence,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of the CLI bundle options to their types.

            :return: The mapping of the CLI bundle options to their types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_SERVICE: IService,
            cls.OPTION_PARSER: IOptionManager,
            cls.OPTION_GUI: IGUI,
        })
