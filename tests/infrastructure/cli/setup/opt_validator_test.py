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
    Unit tests for CLIBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from scaraemu.infrastructure.cli.setup.options import CLIBundleOptions


class TestCLIBundleOptionsValidator(TestCase):
    '''
        Test cases verifying CLIBundleOptionsValidator.

        It defines:

            :methods:
                | test_valid_options - Verifies validation of valid options.
                | test_invalid_options - Verifies rejection of invalid options.
    '''

    def test_valid_options(self) -> None:
        '''
            Verifies validation of valid options.

            :exceptions: None.
        '''
        opts: CLIBundleOptions = {
            'parser': MagicMock(spec=IOptionManager),
            'launcher': MagicMock(spec=IGUI),
        }
        self.assertTrue(CLIBundleOptionsValidator.is_valid(opts))

    def test_invalid_options(self) -> None:
        '''
            Verifies rejection of invalid options.

            :exceptions: None.
        '''
        self.assertFalse(CLIBundleOptionsValidator.is_valid([]))  # type: ignore


if __name__ == '__main__':
    unittest_main()
