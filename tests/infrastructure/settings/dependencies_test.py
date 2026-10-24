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
    Unit test cases for SettingsDependencies.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.settings.dependencies import SettingsDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SettingsDependenciesTestCase(TestCase):
    '''
        Test cases verifying SettingsDependencies behavior.

        It defines:

            :methods:
                | test_dataclass_initialization - Tests initializing dependencies with valid arguments.
                | test_dataclass_immutability - Tests dataclass immutability.
    '''

    def test_dataclass_initialization(self) -> None:
        '''
            Tests initializing dependencies with valid arguments.

            :exceptions: None.
        '''
        mock_context = MagicMock()
        deps = SettingsDependencies(context_bundle=mock_context)
        self.assertIs(deps.context_bundle, mock_context)

    def test_dataclass_immutability(self) -> None:
        '''
            Tests dataclass immutability.

            :exceptions: None.
        '''
        mock_context = MagicMock()
        deps = SettingsDependencies(context_bundle=mock_context)
        with self.assertRaises(FrozenInstanceError):
            deps.context_bundle = MagicMock()


if __name__ == '__main__':
    unittest_main()
