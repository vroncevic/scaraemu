# -*- coding: UTF-8 -*-

'''
Module
    icoordinate_transformer_test.py
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
    Unit tests for ICoordinateTransformer protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyCoordinateTransformer:
    '''
        Dummy transformer implementing ICoordinateTransformer structurally.
    '''

    def world_to_screen(
        self, world_x: float, world_y: float
    ) -> tuple[float, float]:
        '''
            Transforms world to screen coordinates.

            :param world_x: World X coordinate.
            :param world_y: World Y coordinate.
            :return: Tuple of screen (x, y) coordinates.
            :exceptions: None.
        '''
        return (world_x, world_y)

    def screen_to_world(
        self, screen_x: float, screen_y: float
    ) -> tuple[float, float]:
        '''
            Transforms screen to world coordinates.

            :param screen_x: Screen X coordinate.
            :param screen_y: Screen Y coordinate.
            :return: Tuple of world (x, y) coordinates.
            :exceptions: None.
        '''
        return (screen_x, screen_y)

    def get_version(self) -> str:
        '''
            Returns version string.

            :exceptions: None.
        '''
        return '1.0.2'


class TestICoordinateTransformer(TestCase):
    '''
        Unit tests for ICoordinateTransformer protocol.

        It defines:

            :methods:
                | test_protocol_compliance - Tests that dummy transformer satisfies ICoordinateTransformer runtime check.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Tests that dummy transformer satisfies ICoordinateTransformer runtime check.

            :exceptions: None.
        '''
        transformer = _DummyCoordinateTransformer()
        self.assertIsInstance(transformer, ICoordinateTransformer)


if __name__ == '__main__':
    unittest_main()
