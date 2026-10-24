# -*- coding: UTF-8 -*-

'''
Module
    buffer_actions_test.py
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
    Unit tests for BufferActions.
'''

from __future__ import annotations

from tkinter import END, TclError, Text, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.console.buffer_actions import BufferActions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBufferActions(TestCase):
    '''
        Unit tests for BufferActions.

        It defines:

            :methods:
                | setUp - Sets up root window and text widget.
                | tearDown - Cleans up Tk root window.
                | test_buffer_actions_lifecycle - Tests select_all, copy_log, clear_log, and version inquiry.
                | test_copy_log_without_selection - Tests copy_log when no text is selected.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window and text widget.

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

    def test_buffer_actions_lifecycle(self) -> None:
        '''
            Tests select_all, copy_log, clear_log, and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        text_widget = Text(self._root)
        text_widget.pack()
        text_widget.insert(END, 'Sample log content\nLine 2\n')

        actions = BufferActions(
            widget=self._root,
            text_widget=text_widget,
        )

        self.assertEqual(actions.get_version(), '1.0.2')

        actions.select_all()
        actions.copy_log()

        actions.clear_log()
        cleared_content = text_widget.get('1.0', END).strip()
        self.assertEqual(cleared_content, '')

    def test_copy_log_without_selection(self) -> None:
        '''
            Tests copy_log when no text is selected.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        text_widget = Text(self._root)
        text_widget.pack()
        text_widget.insert(END, 'Sample log content')

        actions = BufferActions(
            widget=self._root,
            text_widget=text_widget,
        )

        try:
            actions.copy_log()

        except TclError:
            self.fail('copy_log raised TclError unexpectedly')


if __name__ == '__main__':
    unittest_main()
