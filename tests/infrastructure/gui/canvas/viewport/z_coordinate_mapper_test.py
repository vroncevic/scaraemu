# -*- coding: UTF-8 -*-

'''
Module
    z_coordinate_mapper_test.py
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
    Unit tests for ZCoordinateMapper.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZCoordinateMapper(TestCase):
    '''
        Test cases verifying ZCoordinateMapper coordinate conversions.

        It defines:

            :methods:
                | test_conversions - Verifies bidirectional mapping between mm and pixels.
                | test_get_version - Verifies component version string.
    '''

    def test_conversions(self) -> None:
        '''
            Verifies bidirectional mapping between mm and pixels.

            :exceptions: None.
        '''
        bounds = VerticalBounds(z_min=0.0, z_max=100.0)
        mapper = ZCoordinateMapper(bounds)

        bottom_y: float = 200.0
        top_y: float = 40.0

        sy_bottom: float = mapper.z_to_screen_y(0.0, bottom_y, top_y)
        self.assertAlmostEqual(sy_bottom, bottom_y)

        sy_top: float = mapper.z_to_screen_y(100.0, bottom_y, top_y)
        self.assertAlmostEqual(sy_top, top_y)

        z_calc: float = mapper.screen_y_to_z(sy_top, bottom_y, top_y)
        self.assertAlmostEqual(z_calc, 100.0)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        bounds = VerticalBounds(z_min=0.0, z_max=100.0)
        mapper = ZCoordinateMapper(bounds)
        self.assertEqual(mapper.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
