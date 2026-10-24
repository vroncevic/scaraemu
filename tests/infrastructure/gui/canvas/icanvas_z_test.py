# -*- coding: UTF-8 -*-

'''
Module
    icanvas_z_test.py
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
    Unit tests for ICanvasZ protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyCanvasZ:
    '''
        Dummy vertical canvas implementing ICanvasZ structurally.

        It defines:

            :methods:
                | redraw - Tests redraw.
                | clear - Tests clear.
    '''

    def redraw(self, pose: ScaraPose, current_target: ScaraPose) -> None:
        '''
            Tests redraw.

            :param pose: Input pose.
            :param current_target: Input current_target.
            :exceptions: None.
        '''
        _ = (pose, current_target)

    def clear(self) -> None:
        '''
            Tests clear.

            :exceptions: None.
        '''
        _ = self


class TestICanvasZ(TestCase):
    '''
        Unit tests for ICanvasZ protocol.

        It defines:

            :methods:
                | test_protocol_compliance - Tests that dummy canvas satisfies ICanvasZ runtime check.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Tests that dummy canvas satisfies ICanvasZ runtime check.

            :exceptions: None.
        '''
        canvas = _DummyCanvasZ()
        self.assertIsInstance(canvas, ICanvasZ)


if __name__ == '__main__':
    unittest_main()
