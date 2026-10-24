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
    Unit tests for SettingsFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.infrastructure.settings.dependencies import SettingsDependencies
from scaraemu.infrastructure.settings.factory import SettingsFactory
from scaraemu.infrastructure.settings.geometry.iloader import IGeometryLoader
from scaraemu.infrastructure.settings.provides import SettingsProvides
from scaraemu.infrastructure.settings.transmission.iloader import ITransmissionLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSettingsFactory(TestCase):
    '''
        Unit tests for SettingsFactory.

        It defines:

            :methods:
                | test_create - Verifies create returns SettingsProvides with conforming loaders.
                | test_get_version - Verifies get_version returns valid version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns SettingsProvides with conforming loaders.

            :exceptions: None.
        '''
        context = ContextBundleFactory.create_bundle()
        deps = SettingsDependencies(context_bundle=context)
        provides: SettingsProvides = SettingsFactory.create(dependencies=deps)

        self.assertIsInstance(provides, SettingsProvides)
        self.assertIsInstance(provides.geometry_loader, IGeometryLoader)
        self.assertIsInstance(provides.transmission_loader, ITransmissionLoader)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        version = SettingsFactory.get_version()
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
