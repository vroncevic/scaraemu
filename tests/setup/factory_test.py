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
    Unit tests for SCARAEmuBundleFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.factory import SCARAEmuBundleFactory
from scaraemu.setup.options import SCARAEmuBundleOptions


class TestSCARAEmuBundleFactory(TestCase):
    '''
        Test cases verifying SCARAEmuBundleFactory methods.

        It defines:

            :methods:
                | test_factory_version - Verifies version string retrieval.
                | test_create_with_options - Verifies bundle creation with explicit options.
                | test_create_with_empty_options - Verifies creating full application bundle using default options.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(SCARAEmuBundleFactory.get_version(), '1.0.2')

    def test_create_with_options(self) -> None:
        '''
            Verifies bundle creation with explicit options.

            :exceptions: None.
        '''
        options: SCARAEmuBundleOptions = {'l1': 160.0, 'l2': 110.0}
        bundle = SCARAEmuBundleFactory.create(options=options)
        self.assertEqual(bundle.bounds.links.l1, 160.0)
        self.assertEqual(bundle.bounds.links.l2, 110.0)

    def test_create_with_empty_options(self) -> None:
        '''
            Verifies creating full application bundle using default options.

            :exceptions: None.
        '''
        bundle = SCARAEmuBundleFactory.create(options=SCARAEmuBundleOptions())
        self.assertIsInstance(bundle, SCARAEmuBundle)
        self.assertTrue(bundle.gui.is_initialized())
        self.assertTrue(bundle.cli.is_initialized())
        self.assertTrue(bundle.emulation_service.get_telemetry().motors_enabled)
        self.assertFalse(bundle.emulation_service.get_telemetry().estop_active)


if __name__ == '__main__':
    unittest_main()
