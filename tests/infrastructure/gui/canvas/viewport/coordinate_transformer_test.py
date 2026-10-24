# -*- coding: UTF-8 -*-

'''
Module
    coordinate_transformer_test.py
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
    Unit tests for CoordinateTransformer.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaraemu.infrastructure.gui.canvas.viewport.coordinate_transformer import CoordinateTransformer
from scaraemu.infrastructure.gui.canvas.viewport.viewport import Viewport
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCoordinateTransformer(TestCase):
    '''
        Test cases verifying CoordinateTransformer world-to-screen conversions.

        It defines:

            :methods:
                | setUp - Sets up test fixture with viewport and coordinate transformer.
                | test_protocol_conformance - Verifies transformer satisfies ICoordinateTransformer protocol.
                | test_bidirectional_transformation - Verifies roundtrip coordinate mapping between world mm and screen px.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with viewport and coordinate transformer.

            :exceptions: None.
        '''
        dims = LinkDimensions(l1=200.0, l2=150.0)
        viewport = Viewport(dims, 600, 400)
        self._transformer = CoordinateTransformer(viewport)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies transformer satisfies ICoordinateTransformer protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._transformer, ICoordinateTransformer)

    def test_bidirectional_transformation(self) -> None:
        '''
            Verifies roundtrip coordinate mapping between world mm and screen px.

            :exceptions: None.
        '''
        world_x: float = 120.5
        world_y: float = -85.2
        sx, sy = self._transformer.world_to_screen(world_x, world_y)
        wx_calc, wy_calc = self._transformer.screen_to_world(sx, sy)

        self.assertAlmostEqual(world_x, wx_calc, places=4)
        self.assertAlmostEqual(world_y, wy_calc, places=4)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        self.assertEqual(self._transformer.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
