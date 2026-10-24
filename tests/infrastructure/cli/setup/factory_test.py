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
    Unit tests for CLIBundleFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.cli.setup.factory import CLIBundleFactory
from scaraemu.infrastructure.cli.setup.options import CLIBundleOptions


class TestCLIBundleFactory(TestCase):
    '''
        Test cases verifying CLIBundleFactory.

        It defines:

            :methods:
                | test_create - Verifies creation of CLIBundle.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies creation of CLIBundle.

            :exceptions: None.
        '''
        opts: CLIBundleOptions = {
            'parser': MagicMock(spec=IOptionManager),
            'launcher': MagicMock(spec=IGUI),
        }
        bundle = CLIBundleFactory.create(opts)
        self.assertIsNotNone(bundle)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(CLIBundleFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
