# -*- coding: UTF-8 -*-

'''
Module
    definition_test.py
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
    Unit tests for EmulatorCommandDefinition.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.command.definition import EmulatorCommandDefinition


class TestEmulatorCommandDefinition(TestCase):
    '''
        Test cases verifying EmulatorCommandDefinition properties.

        It defines:

            :methods:
                | test_command_metadata - Verifies command name, options, and help text.
                | test_str - Verifies string representation.
    '''

    def test_command_metadata(self) -> None:
        '''
            Verifies command name, options, and help text.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        self.assertEqual(defn.name, 'emulator')
        self.assertIn('SCARA', defn.help_text)
        self.assertGreater(len(defn.options), 0)

    def test_str(self) -> None:
        '''
            Verifies string representation.

            :exceptions: None.
        '''
        defn = EmulatorCommandDefinition()
        self.assertIn('EmulatorCommandDefinition', str(defn))


if __name__ == '__main__':
    unittest_main()
