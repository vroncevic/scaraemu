# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
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
    Unit tests for SCARAEmuBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.setup.opt_validator import SCARAEmuBundleOptionsValidator
from scaraemu.setup.options import SCARAEmuBundleOptions


class TestSCARAEmuBundleOptionsValidator(TestCase):
    '''
        Test cases verifying SCARAEmuBundleOptionsValidator validation logic.

        It defines:

            :methods:
                | test_valid_options - Verifies validation of valid options mapping.
                | test_invalid_options - Verifies rejection of invalid options.
    '''

    def test_valid_options(self) -> None:
        '''
            Verifies validation of valid options mapping.

            :exceptions: None.
        '''
        opts: SCARAEmuBundleOptions = {'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        self.assertTrue(SCARAEmuBundleOptionsValidator.is_valid(opts))

    def test_invalid_options(self) -> None:
        '''
            Verifies rejection of invalid options.

            :exceptions: None.
        '''
        self.assertFalse(SCARAEmuBundleOptionsValidator.is_valid([]))  # type: ignore


if __name__ == '__main__':
    unittest_main()
