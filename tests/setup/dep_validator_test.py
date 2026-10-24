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
    Unit tests for SCARAEmuBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.dep_validator import SCARAEmuBundleDependenciesValidator
from scaraemu.setup.dependencies import SCARAEmuBundleDependencies
from scaraemu.setup.factory import SCARAEmuBundleFactory
from scaraemu.setup.options import SCARAEmuBundleOptions


class TestSCARAEmuBundleDependenciesValidator(TestCase):
    '''
        Test cases verifying SCARAEmuBundleDependenciesValidator validation.

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
        self.assertFalse(SCARAEmuBundleDependenciesValidator.is_valid([]))  # type: ignore

    def test_valid_dependencies(self) -> None:
        '''
            Verifies acceptance of valid dependencies.

            :exceptions: None.
        '''
        bundle: SCARAEmuBundle = SCARAEmuBundleFactory.create(SCARAEmuBundleOptions())
        deps: SCARAEmuBundleDependencies = {
            'base': bundle.base,
            'bounds': bundle.bounds,
            'kinematics': bundle.kinematics,
            'emulation_service': bundle.emulation_service,
            'gui': bundle.gui,
            'cli': bundle.cli,
        }
        self.assertTrue(SCARAEmuBundleDependenciesValidator.is_valid(deps))


if __name__ == '__main__':
    unittest_main()
