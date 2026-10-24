# -*- coding: UTF-8 -*-

'''
Module
    idefinition_test.py
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
    Unit tests for ICommandDefinition structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.command.definition import EmulatorCommandDefinition
from scaraemu.infrastructure.command.idefinition import ICommandDefinition


class _InvalidCommandDefinition:
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


class TestICommandDefinition(TestCase):
    '''
        Test cases verifying ICommandDefinition structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies EmulatorCommandDefinition satisfies ICommandDefinition structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy ICommandDefinition.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies EmulatorCommandDefinition satisfies ICommandDefinition structurally.

            :exceptions: None.
        '''
        definition = EmulatorCommandDefinition()
        self.assertIsInstance(definition, ICommandDefinition)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy ICommandDefinition.

            :exceptions: None.
        '''
        invalid = _InvalidCommandDefinition()
        self.assertNotIsInstance(invalid, ICommandDefinition)


if __name__ == '__main__':
    unittest_main()
