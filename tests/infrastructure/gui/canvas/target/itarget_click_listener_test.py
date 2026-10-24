# -*- coding: UTF-8 -*-

'''
Module
    itarget_click_listener_test.py
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
    Unit tests for ITargetClickListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyTargetClickListener:
    '''
        Dummy click listener for protocol conformance verification.
    '''

    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.xy_clicks: list[tuple[float, float]] = []
        self.z_clicks: list[float] = []

    def handle_xy_click(self, x: float, y: float) -> bool:
        '''
            Tests handle xy click.

            :param x: Input x.
            :param y: Input y.
            :return: Dispatch success flag.
            :exceptions: None.
        '''
        self.xy_clicks.append((x, y))
        return True

    def handle_z_click(self, z: float) -> bool:
        '''
            Tests handle z click.

            :param z: Input z.
            :return: Dispatch success flag.
            :exceptions: None.
        '''
        self.z_clicks.append(z)
        return True

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestCanvasTargetClickListener(TestCase):
    '''
        Test cases verifying ITargetClickListener protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy listener satisfies ITargetClickListener protocol.
                | test_click_handling - Verifies coordinate dispatch and version string.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy listener satisfies ITargetClickListener protocol.

            :exceptions: None.
        '''
        listener = _DummyTargetClickListener()
        self.assertIsInstance(listener, ITargetClickListener)

    def test_click_handling(self) -> None:
        '''
            Verifies coordinate dispatch and version string.

            :exceptions: None.
        '''
        listener = _DummyTargetClickListener()
        listener.handle_xy_click(10.0, 20.0)
        listener.handle_z_click(30.0)
        self.assertEqual(listener.xy_clicks, [(10.0, 20.0)])
        self.assertEqual(listener.z_clicks, [30.0])
        self.assertEqual(listener.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
