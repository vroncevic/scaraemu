# -*- coding: UTF-8 -*-

'''
Module
    viewport_test.py
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
    Unit tests for Viewport.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaraemu.infrastructure.gui.canvas.viewport.iviewport import IViewport
from scaraemu.infrastructure.gui.canvas.viewport.viewport import Viewport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestViewport(TestCase):
    '''
        Test cases verifying Viewport sizing, scaling, and dimensions.

        It defines:

            :methods:
                | setUp - Sets up test fixture with baseline LinkDimensions and viewport.
                | test_protocol_compliance - Verifies structural compliance with IViewport protocol.
                | test_dimensions_and_scaling - Verifies dimensions and scale reporting and updating.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with baseline LinkDimensions and viewport.

            :exceptions: None.
        '''
        dims = LinkDimensions(l1=200.0, l2=150.0)
        self._viewport = Viewport(dims, 600, 400)

    def test_protocol_compliance(self) -> None:
        '''
            Verifies structural compliance with IViewport protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._viewport, IViewport)

    def test_dimensions_and_scaling(self) -> None:
        '''
            Verifies dimensions and scale reporting and updating.

            :exceptions: None.
        '''
        self.assertEqual(self._viewport.get_dimensions(), (600, 400))
        self.assertGreater(self._viewport.get_scale(), 0.0)

        self._viewport.update_size(800, 600)
        self.assertEqual(self._viewport.get_dimensions(), (800, 600))
        self.assertGreater(self._viewport.get_scale(), 0.0)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        self.assertEqual(self._viewport.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
