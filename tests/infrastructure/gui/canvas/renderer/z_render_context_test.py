# -*- coding: UTF-8 -*-

'''
Module
    z_render_context_test.py
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
    Unit test cases for ZRenderContext parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.renderer.z_render_context import ZRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZRenderContextTestCase(TestCase):
    '''
        Unit tests for ZRenderContext.

        It defines:

            :methods:
                | test_context_attributes - Verifies context attribute assignment.
    '''

    def test_context_attributes(self) -> None:
        '''
            Verifies context attribute assignment.

            :exceptions: None.
        '''
        mock_bounds = MagicMock(spec=ScaraBounds)
        mock_mapper = MagicMock(spec=ZCoordinateMapper)
        context = ZRenderContext(
            bounds=mock_bounds,
            coordinate_mapper=mock_mapper,
            width_px=320.0,
            height_px=240.0,
        )
        self.assertIs(context.bounds, mock_bounds)
        self.assertIs(context.coordinate_mapper, mock_mapper)
        self.assertEqual(context.width_px, 320.0)
        self.assertEqual(context.height_px, 240.0)


if __name__ == '__main__':
    unittest_main()
