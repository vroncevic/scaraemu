# -*- coding: UTF-8 -*-

'''
Module
    emulator_command_definition.py
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
    Defines EmulatorCommandDefinition class.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorCommandDefinition:
    '''
        CLI subcommand metadata definition for SCARA Robot Emulator and Visualizer.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
            :exceptions: None.
        '''
        return 'emulator'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
            :exceptions: None.
        '''
        return 'Run SCARA Robot Emulator and 2D/3D Kinematic Visualizer'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
            :exceptions: None.
        '''
        return [
            OptionData(
                name='--port',
                help_text='Serial port device path (e.g. /dev/ttyACM0)',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--baud',
                help_text='Serial communication baudrate',
                action=None,
                default=115200,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--file',
                help_text='Path to initial trajectory plan file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--verbose',
                help_text='Enable verbose logging output',
                action='store_true',
                default=False,
                required=False,
                choices=None,
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: The command definition as string representation.
            :exceptions: None.
        '''
        return to_str(self)
