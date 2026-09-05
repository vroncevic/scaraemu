# -*- coding: UTF-8 -*-

'''
Module
    test_bundle_factory.py
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

import unittest
from scaraemu.setup.factory import SCARAEmuBundleFactory
from scaraemu.setup.bundle import SCARAEmuBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBundleFactory(unittest.TestCase):
    '''Unit test cases for SCARAEmuBundleFactory.'''

    def test_factory_version(self) -> None:
        '''Tests version reporting.'''
        self.assertEqual(SCARAEmuBundleFactory.get_version(), '1.0.2')

    def test_resolve_geometry_defaults(self) -> None:
        '''Tests dynamic geometry resolution with options fallback.'''
        bundle = SCARAEmuBundleFactory.create_bundle(options={'l1': 160.0, 'l2': 110.0})
        geom = bundle.service.get_kinematics().get_geometry()
        self.assertEqual(geom.l1, 160.0)
        self.assertEqual(geom.l2, 110.0)

    def test_create_bundle(self) -> None:
        '''Tests creating full application bundle.'''
        bundle = SCARAEmuBundleFactory.create_bundle()
        self.assertIsInstance(bundle, SCARAEmuBundle)
        self.assertTrue(bundle.service.is_initialized())
        self.assertTrue(bundle.gui.is_initialized())
        self.assertTrue(bundle.cli.is_initialized())


if __name__ == '__main__':
    unittest.main()
