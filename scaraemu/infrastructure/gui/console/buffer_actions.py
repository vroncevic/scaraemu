# -*- coding: UTF-8 -*-

'''
Module
    buffer_actions.py
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
    Buffer manipulation actions for console log viewer (select, copy, clear).
'''

from __future__ import annotations

from tkinter import END, INSERT, SEL, SEL_FIRST, SEL_LAST, TclError, Text, Widget
from typing import Final

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BufferActions:
    '''
        Buffer actions manager handling clipboard copy, text selection, and log clearing.

        It defines:

            :attributes:
                | _widget - Owner widget providing clipboard access.
                | _text_widget - Target Text widget containing log buffer.
            :methods:
                | __init__ - Initializes buffer actions with widget references.
                | select_all - Selects all text content in the log buffer.
                | copy_log - Copies selected or entire log content to clipboard.
                | clear_log - Clears log text buffer.
                | get_version - Returns buffer actions component version.
    '''

    _widget: Widget
    _text_widget: Text

    def __init__(self, *, widget: Widget, text_widget: Text) -> None:
        '''
            Initializes buffer actions with widget references.

            :param widget: Container widget providing clipboard operations.
            :param text_widget: Text widget buffer to operate on.
            :exceptions: None.
        '''
        self._widget: Final[Widget] = widget
        self._text_widget: Final[Text] = text_widget

    def select_all(self) -> None:
        '''
            Selects all text content in the console log buffer.

            :exceptions: None.
        '''
        self._text_widget.tag_add(SEL, '1.0', END)
        self._text_widget.mark_set(INSERT, '1.0')
        self._text_widget.see(INSERT)
        self._text_widget.focus_set()

    def copy_log(self) -> None:
        '''
            Copies selected or entire console log content to clipboard.

            :exceptions: None.
        '''
        try:
            content: str = self._text_widget.get(SEL_FIRST, SEL_LAST)

        except TclError:
            content = self._text_widget.get('1.0', END).strip()

        if content:
            self._widget.clipboard_clear()
            self._widget.clipboard_append(content)

    def clear_log(self) -> None:
        '''
            Clears console text buffer.

            :exceptions: None.
        '''
        self._text_widget.config(state='normal')
        self._text_widget.delete('1.0', END)
        self._text_widget.config(state='disabled')

    def get_version(self) -> str:
        '''
            Returns buffer actions component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
