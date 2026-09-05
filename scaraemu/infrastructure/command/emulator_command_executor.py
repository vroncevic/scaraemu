# -*- coding: UTF-8 -*-

'''
Module
    emulator_command_executor.py
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
    Defines EmulatorCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.utils.reflection import to_str

from scaraemu.infrastructure.command.icommand_definition import ICommandDefinition
from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorCommandExecutor:
    '''
        Command executor strategy for launching SCARAEmu emulator and visualizer GUI.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
                | gui - The GUI presentation adapter instance.
            :methods:
                | execute - Executes the emulator command.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns the EmulatorCommandExecutor as string representation.
    '''

    definition: ICommandDefinition
    gui: IGUI

    def __init__(self, definition: ICommandDefinition, gui: IGUI) -> None:
        '''
            Initializes the command executor.

            :param definition: The command definition metadata.
            :param gui: The GUI presentation adapter instance.
            :exceptions: None.
        '''
        self.definition = definition
        self.gui = gui

    def execute(self, *, params: Mapping[str, object], service: IService) -> Mapping[str, object]:
        '''
            Executes the subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Kinematics and emulator domain service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        if not self.gui.is_initialized() or not service.is_initialized():
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': 'emulator_command_executor::execute - gui or service not initialized'
            }

        try:
            file_path: object = params.get('file')
            if file_path is not None and isinstance(file_path, str) and file_path:
                self.gui.load_file(file_path)

            self.gui.run()
            return {'returncode': 0, 'stdout': 'Emulator closed successfully', 'stderr': ''}

        except Exception as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'emulator_command_executor::execute - {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns the EmulatorCommandExecutor as string representation.

            :return: The EmulatorCommandExecutor as string representation.
            :exceptions: None.
        '''
        return to_str(self)
