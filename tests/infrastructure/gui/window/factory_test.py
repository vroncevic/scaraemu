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
    Unit tests for WindowConfiguratorFactory implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.window.configurator import WindowConfigurator
from scaraemu.infrastructure.gui.window.factory import WindowConfiguratorFactory
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWindowConfiguratorFactory(TestCase):
    '''
        Test cases verifying WindowConfiguratorFactory instantiation.

        It defines:

            :methods:
                | test_create - Verifies create returns a WindowConfigurator satisfying IWindowConfigurator.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns a WindowConfigurator satisfying IWindowConfigurator.

            :exceptions: None.
        '''
        instance = WindowConfiguratorFactory.create()
        self.assertIsInstance(instance, WindowConfigurator)
        self.assertIsInstance(instance, IWindowConfigurator)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertIsInstance(WindowConfiguratorFactory.get_version(), str)
        self.assertEqual(WindowConfiguratorFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
