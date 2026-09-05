# -*- coding: UTF-8 -*-

'''
Module
    test_setup_validators.py
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
    Unit tests for setup options and dependencies validators.
'''

from __future__ import annotations

import unittest
from scaraemu.setup.options import SCARAEmuBundleOptions
from scaraemu.setup.opt_validator import SCARAEmuBundleOptionsValidator
from scaraemu.setup.dep_validator import SCARAEmuBundleDependenciesValidator
from scaraemu.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from scaraemu.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSetupValidators(unittest.TestCase):
    '''Unit test cases for options and dependencies validators.'''

    def test_bundle_options_validator(self) -> None:
        '''Tests validation of bundle options.'''
        valid_opts: SCARAEmuBundleOptions = {
            'l1': 150.0,
            'l2': 120.0,
            'z_min': 0.0,
            'z_max': 100.0
        }
        self.assertTrue(SCARAEmuBundleOptionsValidator.is_valid(valid_opts))

    def test_cli_bundle_options_validator_invalid(self) -> None:
        '''Tests that non-mapping or invalid options fail validation.'''
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore
        self.assertFalse(SCARAEmuBundleDependenciesValidator.is_valid(None))  # type: ignore


if __name__ == '__main__':
    unittest.main()
