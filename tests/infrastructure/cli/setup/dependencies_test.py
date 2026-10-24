# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for CLIBundleDependencies type definition.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.cli.setup.dependencies import CLIBundleDependencies


class TestCLIBundleDependencies(TestCase):
    '''
        Test cases verifying CLIBundleDependencies TypedDict.

        It defines:

            :methods:
                | test_type_definition - Verifies dictionary inheritance.
    '''

    def test_type_definition(self) -> None:
        '''
            Verifies dictionary inheritance.

            :exceptions: None.
        '''
        self.assertTrue(issubclass(CLIBundleDependencies, dict))


if __name__ == '__main__':
    unittest_main()
