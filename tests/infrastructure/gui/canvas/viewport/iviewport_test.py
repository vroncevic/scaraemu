# -*- coding: UTF-8 -*-

'''
Module
    iviewport_test.py
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
    Unit tests for IViewport protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.canvas.viewport.iviewport import IViewport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyViewport:
    '''
        Dummy viewport implementing IViewport structurally.
    '''

    def update_size(self, width: int, height: int) -> None:
        '''
            Tests update size.

            :param width: Input width.
            :param height: Input height.
            :exceptions: None.
        '''
        _ = (width, height)

    def get_scale(self) -> float:
        '''
            Tests get scale.

            :exceptions: None.
        '''
        return 1.0

    def get_dimensions(self) -> tuple[float, float]:
        '''
            Tests get dimensions.

            :exceptions: None.
        '''
        return (480.0, 480.0)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestIViewport(TestCase):
    '''
        Unit tests for IViewport protocol.

        It defines:

            :methods:
                | test_protocol_compliance - Tests that dummy viewport satisfies IViewport runtime check.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Tests that dummy viewport satisfies IViewport runtime check.

            :exceptions: None.
        '''
        viewport = _DummyViewport()
        self.assertIsInstance(viewport, IViewport)


if __name__ == '__main__':
    unittest_main()
