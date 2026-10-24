# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for CLI adapter engine.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from ats_utilities.exceptions.ats_value_error import ATSValueError
from ats_utilities.option.imanager import IOptionManager

from scaraemu.infrastructure.cli.engine import CLI
from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.infrastructure.command.bundle import CommandBundle
from scaraemu.infrastructure.command.idefinition import ICommandDefinition
from scaraemu.infrastructure.command.iexecutor import ICommandExecutor


class TestCLI(TestCase):
    '''
        Test cases verifying CLI adapter engine initialization and string representation.

        It defines:

            :methods:
                | test_initialization - Verifies initialization status.
                | test_str - Verifies string representation.
                | test_run_success - Verifies executing registered command strategy.
                | test_run_not_found - Verifies handling unregistered command.
                | test_run_exception - Verifies handling parse exceptions.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies initialization status.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        bundle = CLIBundle(parser=parser, commands=[])
        cli = CLI(bundle=bundle)
        self.assertTrue(cli.is_initialized())

    def test_str(self) -> None:
        '''
            Verifies string representation.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        bundle = CLIBundle(parser=parser, commands=[])
        cli = CLI(bundle=bundle)
        self.assertIn('CLI', str(cli))

    def test_run_success(self) -> None:
        '''
            Verifies executing registered command strategy.

            :exceptions: None.
        '''
        mock_def = MagicMock(spec=ICommandDefinition)
        mock_def.name = 'test_cmd'
        mock_exec = MagicMock(spec=ICommandExecutor)
        mock_exec.execute.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

        parser = MagicMock(spec=IOptionManager)
        parser.parse_command.return_value = ('test_cmd', {'foo': 'bar'})

        pair = CommandBundle(definition=mock_def, executor=mock_exec)
        bundle = CLIBundle(parser=parser, commands=[pair])
        cli = CLI(bundle=bundle)

        res = cli.run()
        self.assertEqual(res['returncode'], 0)
        mock_exec.execute.assert_called_once_with(params={'foo': 'bar'})

    def test_run_not_found(self) -> None:
        '''
            Verifies handling unregistered command.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        parser.parse_command.return_value = ('unknown', {})
        bundle = CLIBundle(parser=parser, commands=[])
        cli = CLI(bundle=bundle)

        res = cli.run()
        self.assertEqual(res['returncode'], 1)
        self.assertIn('command not found', str(res['stderr']))

    def test_run_exception(self) -> None:
        '''
            Verifies handling parse exceptions.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        parser.parse_command.side_effect = ATSValueError('Invalid arg')
        bundle = CLIBundle(parser=parser, commands=[])
        cli = CLI(bundle=bundle)

        res = cli.run()
        self.assertEqual(res['returncode'], 1)
        self.assertIn('Invalid arg', str(res['stderr']))


if __name__ == '__main__':
    unittest_main()
