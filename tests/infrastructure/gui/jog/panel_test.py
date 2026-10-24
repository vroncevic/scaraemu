# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for JogPanel composite container component.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.jog.dpad.section import JogDpad
from scaraemu.infrastructure.gui.jog.panel import JogPanel
from scaraemu.infrastructure.gui.jog.step.section import JogStepSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockJogActionDelegate:
    '''
        Mock delegate tracking jog calls.
    '''

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Tests handle jog.

            :param dx: Input dx.
            :param dy: Input dy.
            :param dz: Input dz.
            :param dphi: Input dphi.
            :exceptions: None.
        '''
        _ = (dx, dy, dz, dphi)

    def handle_home(self, axis: str) -> None:
        '''
            Tests handle home.

            :param axis: Input axis.
            :exceptions: None.
        '''
        _ = axis

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestJogPanel(TestCase):
    '''
        Unit tests for JogPanel.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_jog_panel_initialization_and_properties - Tests panel initialization, properties, and version inquiry.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_jog_panel_initialization_and_properties(self) -> None:
        '''
            Tests panel initialization, properties, and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        jog_delegate = _MockJogActionDelegate()

        panel = JogPanel(
            self._root,
            jog_delegate=jog_delegate,
        )
        panel.pack()

        step_section, dpad = panel.get_sections()
        self.assertIsInstance(step_section, JogStepSection)
        self.assertIsInstance(dpad, JogDpad)
        self.assertEqual(panel.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
