# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
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
    Unit tests for CLIBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from scaraemu.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator
from scaraemu.infrastructure.cli.setup.dependencies import CLIBundleDependencies


class TestCLIBundleDependenciesValidator(TestCase):
    '''
        Test cases verifying CLIBundleDependenciesValidator.

        It defines:

            :methods:
                | test_invalid_dependencies - Verifies rejection of invalid dependency types.
                | test_valid_dependencies - Verifies acceptance of valid dependencies.
    '''

    def test_invalid_dependencies(self) -> None:
        '''
            Verifies rejection of invalid dependency types.

            :exceptions: None.
        '''
        self.assertFalse(CLIBundleDependenciesValidator.is_valid([]))  # type: ignore

    def test_valid_dependencies(self) -> None:
        '''
            Verifies acceptance of valid dependencies.

            :exceptions: None.
        '''
        deps: CLIBundleDependencies = {
            'parser': MagicMock(spec=IOptionManager),
            'commands': [],
        }
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(deps))


if __name__ == '__main__':
    unittest_main()
