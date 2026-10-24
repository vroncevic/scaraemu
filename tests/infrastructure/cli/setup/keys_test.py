# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
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
    Unit tests for CLIBundleKeys.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.cli.setup.keys import CLIBundleKeys


class TestCLIBundleKeys(TestCase):
    '''
        Test cases verifying CLIBundleKeys constants.

        It defines:

            :methods:
                | test_keys_attributes - Verifies key constants.
    '''

    def test_keys_attributes(self) -> None:
        '''
            Verifies key constants.

            :exceptions: None.
        '''
        self.assertEqual(CLIBundleKeys.DEPENDENCY_PARSER, 'parser')
        self.assertEqual(CLIBundleKeys.DEPENDENCY_COMMANDS, 'commands')


if __name__ == '__main__':
    unittest_main()
