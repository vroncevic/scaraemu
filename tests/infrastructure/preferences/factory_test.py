# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for PreferencesFactory.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main as unittest_main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaracom.transport.preference.irepository import ISerialPreferenceRepository

from scaraemu.infrastructure.preferences.dependencies import PreferencesDependencies
from scaraemu.infrastructure.preferences.factory import PreferencesFactory
from scaraemu.infrastructure.preferences.provides import PreferencesProvides
from scaraemu.infrastructure.preferences.server.irepository import IServerPreferenceRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPreferencesFactory(TestCase):
    '''
        Unit tests for PreferencesFactory.

        It defines:

            :methods:
                | test_create - Tests instantiating PreferencesProvides bundle.
                | test_get_version - Tests factory version query.
    '''

    def test_create(self) -> None:
        '''
            Tests instantiating PreferencesProvides bundle.

            :exceptions: None.
        '''
        with TemporaryDirectory() as temp_dir:
            serial_path = Path(temp_dir) / 'serial.json'
            server_path = Path(temp_dir) / 'server.json'
            context: ContextBundle = ContextBundleFactory.create_bundle()
            deps = PreferencesDependencies(
                context_bundle=context,
                serial_config_file=serial_path,
                server_config_file=server_path,
            )
            provides: PreferencesProvides = PreferencesFactory.create(deps)
            self.assertIsInstance(provides.serial, ISerialPreferenceRepository)
            self.assertIsInstance(provides.server, IServerPreferenceRepository)

    def test_get_version(self) -> None:
        '''
            Tests factory version query.

            :exceptions: None.
        '''
        self.assertEqual(PreferencesFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
