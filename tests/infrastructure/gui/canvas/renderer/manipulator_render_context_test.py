# -*- coding: UTF-8 -*-

'''
Module
    manipulator_render_context_test.py
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
    Unit test cases for ManipulatorRenderContext parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.canvas.renderer.manipulator_render_context import ManipulatorRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorRenderContextTestCase(TestCase):
    '''
        Unit tests for ManipulatorRenderContext.

        It defines:

            :methods:
                | test_context_attributes - Verifies context attribute assignment.
    '''

    def test_context_attributes(self) -> None:
        '''
            Verifies context attribute assignment.

            :exceptions: None.
        '''
        mock_transformer = MagicMock(spec=ICoordinateTransformer)
        mock_adapter = MagicMock(spec=ILinkageAdapter)
        context = ManipulatorRenderContext(
            transformer=mock_transformer,
            manipulator_linkage_adapter=mock_adapter,
        )
        self.assertIs(context.transformer, mock_transformer)
        self.assertIs(context.manipulator_linkage_adapter, mock_adapter)


if __name__ == '__main__':
    unittest_main()
