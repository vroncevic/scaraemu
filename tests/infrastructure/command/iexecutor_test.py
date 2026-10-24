# -*- coding: UTF-8 -*-

'''
Module
    iexecutor_test.py
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
    Unit tests for ICommandExecutor structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.command.iexecutor import ICommandExecutor


class _DummyCommandExecutor:
    '''
        Dummy class conforming to ICommandExecutor structurally.

        It defines:

            :methods:
                | execute - Executes this command strategy.
                | get_definition - Returns the command definition metadata.
    '''

    def execute(self, *, params: dict[str, str]) -> int:
        '''
            Executes this command strategy.

            :param params: Command parameters.
            :return: Result integer.
            :exceptions: None.
        '''
        _ = params
        return 0

    def get_definition(self) -> str:
        '''
            Returns the command definition metadata.

            :return: Command definition string.
            :exceptions: None.
        '''
        return 'dummy'


class _InvalidCommandExecutor:
    '''
        Dummy class missing required protocol methods.

        It defines:

            :methods:
                | dummy_action - Dummy placeholder action.
                | get_status - Returns dummy status.
    '''

    def dummy_action(self) -> None:
        '''
            Performs dummy action.

            :exceptions: None.
        '''

    def get_status(self) -> str:
        '''
            Returns dummy status.

            :return: Status string.
            :exceptions: None.
        '''
        return 'invalid'


class TestICommandExecutor(TestCase):
    '''
        Test cases verifying ICommandExecutor structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy conforming class satisfies ICommandExecutor structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy ICommandExecutor.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies ICommandExecutor structurally.

            :exceptions: None.
        '''
        executor = _DummyCommandExecutor()
        self.assertIsInstance(executor, ICommandExecutor)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy ICommandExecutor.

            :exceptions: None.
        '''
        invalid = _InvalidCommandExecutor()
        self.assertNotIsInstance(invalid, ICommandExecutor)


if __name__ == '__main__':
    unittest_main()
