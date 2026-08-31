# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines CLIBundle container holding CLI adapters and commands.
'''

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.utils.reflection import instance_to_dict

from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.command.command import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class CLIBundle:
    '''
        Container holding all CLI components for SCARAEmu.

        It defines:

            :attributes:
                | service - Core kinematics and emulator simulation service.
                | parser - Option manager for command line options.
                | commands - Sequence of registered command bundles.
            :methods:
                | to_dict - Converts the bundle to a dictionary.
    '''

    service: IService
    parser: IOptionManager
    commands: Sequence[CommandBundle]

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of the bundle.
            :exceptions: None.
        '''
        return instance_to_dict(self)
