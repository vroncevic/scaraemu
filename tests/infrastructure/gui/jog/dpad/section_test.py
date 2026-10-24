# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for JogDpad directional button grid component.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.jog.dpad.section import JogDpad

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockJogStepProvider:
    '''
        Mock step provider.
    '''

    def get_step(self) -> float:
        '''
            Tests get step.

            :exceptions: None.
        '''
        return 5.0

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockJogActionDelegate:
    '''
        Mock delegate tracking jog and homing calls.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.jog_calls: list[tuple[float, float, float, float]] = []
        self.home_calls: list[str] = []

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Tests handle jog.

            :param dx: Input dx.
            :param dy: Input dy.
            :param dz: Input dz.
            :param dphi: Input dphi.
            :exceptions: None.
        '''
        self.jog_calls.append((dx, dy, dz, dphi))

    def handle_home(self, axis: str) -> None:
        '''
            Tests handle home.

            :param axis: Input axis.
            :exceptions: None.
        '''
        self.home_calls.append(axis)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestJogDpad(TestCase):
    '''
        Unit tests for JogDpad.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_dpad_initialization_and_version - Tests D-pad initialization and version inquiry.
                | test_delegate_actions - Tests direct delegate action dispatch.
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

    def test_dpad_initialization_and_version(self) -> None:
        '''
            Tests D-pad initialization and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        step_provider = _MockJogStepProvider()
        delegate = _MockJogActionDelegate()
        dpad = JogDpad(
            self._root,
            step_provider=step_provider,
            delegate=delegate,
        )
        dpad.pack()

        self.assertEqual(dpad.get_version(), '1.0.2')

    def test_delegate_actions(self) -> None:
        '''
            Tests direct delegate action dispatch.

            :exceptions: None.
        '''
        delegate = _MockJogActionDelegate()
        delegate.handle_jog(1.0, 0.0, 0.0, 0.0)
        delegate.handle_home('xy')

        self.assertEqual(delegate.jog_calls, [(1.0, 0.0, 0.0, 0.0)])
        self.assertEqual(delegate.home_calls, ['xy'])


if __name__ == '__main__':
    unittest_main()
