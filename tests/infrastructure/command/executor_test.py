# -*- coding: UTF-8 -*-

'''
Module
    executor_test.py
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
    Unit tests for EmulatorCommandExecutor.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.command.definition import EmulatorCommandDefinition
from scaraemu.infrastructure.command.executor import EmulatorCommandExecutor
from scaraemu.infrastructure.gui.igui import IGUI


class TestEmulatorCommandExecutor(TestCase):
    '''
        Test cases verifying EmulatorCommandExecutor execution.

        It defines:

            :methods:
                | test_execution - Verifies execution of emulator command with mock launcher.
                | test_get_definition - Verifies definition retrieval.
                | test_execute_uninitialized - Verifies execution fails when launcher is not initialized.
                | test_execute_with_file - Verifies execution loads file when parameter is provided.
                | test_execute_exception - Verifies execution handles exceptions during run.
    '''

    def test_execution(self) -> None:
        '''
            Verifies execution of emulator command with mock launcher.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        mock_launcher = MagicMock(spec=IGUI)
        executor = EmulatorCommandExecutor(definition=defn, launcher=mock_launcher)

        result = executor.execute(params={})
        self.assertEqual(result.get('returncode'), 0)
        self.assertTrue(mock_launcher.run.called)

    def test_get_definition(self) -> None:
        '''
            Verifies definition retrieval.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        mock_launcher = MagicMock(spec=IGUI)
        executor = EmulatorCommandExecutor(definition=defn, launcher=mock_launcher)
        self.assertEqual(executor.get_definition(), defn)
        self.assertIn('EmulatorCommandExecutor', str(executor))

    def test_execute_uninitialized(self) -> None:
        '''
            Verifies execution fails when launcher is not initialized.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        mock_launcher = MagicMock(spec=IGUI)
        mock_launcher.is_initialized.return_value = False
        executor = EmulatorCommandExecutor(definition=defn, launcher=mock_launcher)

        result = executor.execute(params={})
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('launcher not initialized', str(result.get('stderr')))

    def test_execute_with_file(self) -> None:
        '''
            Verifies execution loads file when parameter is provided.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        mock_launcher = MagicMock(spec=IGUI)
        mock_launcher.is_initialized.return_value = True
        executor = EmulatorCommandExecutor(definition=defn, launcher=mock_launcher)

        result = executor.execute(params={'file': '/tmp/test.scara'})
        self.assertEqual(result.get('returncode'), 0)
        mock_launcher.load_file.assert_called_once_with('/tmp/test.scara')
        mock_launcher.run.assert_called_once()

    def test_execute_exception(self) -> None:
        '''
            Verifies execution handles exceptions during run.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        mock_launcher = MagicMock(spec=IGUI)
        mock_launcher.is_initialized.return_value = True
        mock_launcher.run.side_effect = RuntimeError('Launcher crash')
        executor = EmulatorCommandExecutor(definition=defn, launcher=mock_launcher)

        result = executor.execute(params={})
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('Launcher crash', str(result.get('stderr')))


if __name__ == '__main__':
    unittest_main()
