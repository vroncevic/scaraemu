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
    Unit tests for PreferencesDependencies dataclass.
'''

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main as unittest_main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.infrastructure.preferences.dependencies import PreferencesDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPreferencesDependencies(TestCase):
    '''
        Unit tests for PreferencesDependencies.

        It defines:

            :methods:
                | test_default_dependencies - Tests initializing dependencies with default paths.
                | test_explicit_dependencies - Tests initializing dependencies with custom paths.
    '''

    def test_default_dependencies(self) -> None:
        '''
            Tests initializing dependencies with default paths.

            :exceptions: None.
        '''
        context: ContextBundle = ContextBundleFactory.create_bundle()
        deps = PreferencesDependencies(context_bundle=context)
        self.assertIs(deps.context_bundle, context)
        self.assertTrue(str(deps.serial_config_file).endswith('serial_device.json'))
        self.assertTrue(str(deps.server_config_file).endswith('server_config.json'))

    def test_explicit_dependencies(self) -> None:
        '''
            Tests initializing dependencies with custom paths.

            :exceptions: None.
        '''
        context: ContextBundle = ContextBundleFactory.create_bundle()
        serial_path = Path('/tmp/custom_serial.json')
        server_path = Path('/tmp/custom_server.json')
        deps = PreferencesDependencies(
            context_bundle=context,
            serial_config_file=serial_path,
            server_config_file=server_path,
        )
        self.assertIs(deps.context_bundle, context)
        self.assertEqual(deps.serial_config_file, serial_path)
        self.assertEqual(deps.server_config_file, server_path)


if __name__ == '__main__':
    unittest_main()
