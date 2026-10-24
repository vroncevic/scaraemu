# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for SCARAEmuBundle.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.factory import SCARAEmuBundleFactory
from scaraemu.setup.options import SCARAEmuBundleOptions


class TestSCARAEmuBundle(TestCase):
    '''
        Test cases verifying SCARAEmuBundle dataclass properties.

        It defines:

            :methods:
                | test_bundle_creation - Verifies bundle properties after default factory creation.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle properties after default factory creation.

            :exceptions: None.
        '''
        bundle: SCARAEmuBundle = SCARAEmuBundleFactory.create(SCARAEmuBundleOptions())
        self.assertIsInstance(bundle, SCARAEmuBundle)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.cli)
        self.assertIsNotNone(bundle.kinematics)
        self.assertIsNotNone(bundle.bounds)


if __name__ == '__main__':
    unittest_main()
