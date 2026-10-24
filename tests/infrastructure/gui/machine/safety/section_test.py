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
    Unit tests for SafetySection subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate
from scaraemu.infrastructure.gui.machine.safety.section import SafetySection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSafetySection(TestCase):
    '''
        Unit tests for SafetySection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_buttons_invoke_delegates - Tests HOLD and ESTOP buttons invoke delegate.
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

    def test_buttons_invoke_delegates(self) -> None:
        '''
            Tests HOLD and ESTOP buttons invoke delegate.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        safety_delegate = MagicMock(spec=ISafetyDelegate)
        section = SafetySection(
            self._root,
            safety_delegate=safety_delegate,
        )
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')

        btn_hold, btn_estop = section.get_buttons()
        btn_hold.invoke()
        safety_delegate.handle_toggle_hold.assert_called_once()

        btn_estop.invoke()
        safety_delegate.handle_estop.assert_called_once()


if __name__ == '__main__':
    unittest_main()
