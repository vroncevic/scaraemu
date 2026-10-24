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
    Unit tests for JogStepSection subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.jog.step.section import JogStepSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogStepSection(TestCase):
    '''
        Unit tests for JogStepSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_step_section_and_version - Tests section initialization and version inquiry.
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

    def test_step_section_and_version(self) -> None:
        '''
            Tests section initialization and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        section = JogStepSection(self._root)
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')
        self.assertEqual(section.get_step(), 5.0)


if __name__ == '__main__':
    unittest_main()
