# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines CLI class implementing inbound CLI port for SCARAEmu.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.exceptions import ATSRuntimeError, ATSValueError, ATSTypeError
from ats_utilities.utils.reflection import to_str

from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.infrastructure.cli.setup.validator import CLIBundleValidator
from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.command.icommand_definition import ICommandDefinition
from scaraemu.infrastructure.command.icommand_executor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLI(ICLI):
    '''
        Adapter that implements CLI commands for the SCARA emulator and visualizer.

        It defines:

            :attributes:
                | _service - Kinematics and emulator simulation service.
                | _parser - Argument parser for parsing CLI command args.
                | _executors - Map of command names to command executor instances.
            :methods:
                | __init__ - Initializes the CLI with service, parser and commands list.
                | run - Parses command line arguments and runs selected command strategy.
                | is_initialized - Checks if the CLI is initialized.
                | __str__ - Returns the CLI as string representation.
    '''

    _service: IService
    _parser: IOptionManager
    _executors: Mapping[str, ICommandExecutor[ICommandDefinition, object, object, object]]

    def __init__(self, bundle: CLIBundle) -> None:
        '''
            Initializes the CLI with service, parser and commands list.

            :param bundle: Bundle containing CLI adapters.
            :exceptions:
                | ATSValueError: The CLI bundle must be provided and have proper values.
                | ATSTypeError: The CLI bundle must match types.
        '''
        CLIBundleValidator.validate(bundle)
        self._service = bundle.service
        self._parser = bundle.parser
        self._executors = {pair.definition.name: pair.executor for pair in bundle.commands}
        self._parser.register_commands([pair.definition for pair in bundle.commands])

    def run(self) -> Mapping[str, object]:
        '''
            Parses command line arguments and runs selected command strategy.

            :return: The execution result (return code, stdout, and stderr).
            :exceptions: None.
        '''
        try:
            command_name, params = self._parser.parse_command()
            executor: ICommandExecutor[ICommandDefinition, object, object, object] | None = self._executors.get(command_name)

            return executor.execute(params=params, service=self._service) if executor else {
                'returncode': 1, 'stdout': '', 'stderr': 'cli::run - command not found'
            }

        except (ATSRuntimeError, ATSValueError, ATSTypeError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'cli::run - {exc}'}

    def is_initialized(self) -> bool:
        '''
            Checks if the CLI is initialized.

            :return: True if CLI is initialized, False otherwise.
            :exceptions: None.
        '''
        return True

    def __str__(self) -> str:
        '''
            Returns the CLI as string representation.

            :return: The CLI as string representation.
            :exceptions: None.
        '''
        return to_str(self)
