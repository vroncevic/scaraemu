# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Interactive serial communication console panel for diagnostic logging.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    END,
    FLAT,
    LEFT,
    RIGHT,
    X,
    Y,
    Button,
    Frame,
    LabelFrame,
    Scrollbar,
    Text,
    Widget,
)
from typing import Final

from scaraemu.infrastructure.gui.console.buffer_actions import BufferActions
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConsolePanel(LabelFrame):
    '''
        Console log display panel with toolbar actions and styled text buffer.

        It defines:

            :attributes:
                | _text_log - Target Text widget containing log buffer.
                | _buffer_actions - Buffer actions manager for select, copy, and clear.
            :methods:
                | __init__ - Configures and packs console panel widgets.
                | append_log - Appends formatted log entry to the console.
                | clear_log - Clears console text buffer.
                | get_log_content - Returns current text content from log buffer.
                | get_version - Returns component version string.
    '''

    _text_log: Text
    _buffer_actions: BufferActions

    def __init__(self, parent: Widget) -> None:
        '''
            Configures and packs console panel widgets and color tags.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Serial Communication Console  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8,
        )

        log_frame: Frame = Frame(self, bg=ThemeManager.BG_CANVAS)
        log_frame.pack(fill=BOTH, expand=True, pady=(0, 6))

        scroll: Scrollbar = Scrollbar(log_frame)
        scroll.pack(side=RIGHT, fill=Y)

        self._text_log: Final[Text] = Text(
            log_frame,
            height=6,
            bg=ThemeManager.BG_CANVAS,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_MONO, 8),
            state='disabled',
            wrap='word',
            yscrollcommand=scroll.set,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0,
        )
        self._text_log.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.config(command=self._text_log.yview)

        self._text_log.tag_config('tx', foreground=ThemeManager.ACCENT_BLUE)
        self._text_log.tag_config('rx', foreground=ThemeManager.ACCENT_GREEN)
        self._text_log.tag_config('err', foreground=ThemeManager.ACCENT_RED)
        self._text_log.tag_config('host', foreground=ThemeManager.ACCENT_YELLOW)

        self._buffer_actions: Final[BufferActions] = BufferActions(
            widget=self,
            text_widget=self._text_log,
        )

        top_bar: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        top_bar.pack(fill=X, pady=(0, 4))

        btn_select_all: Button = Button(
            top_bar,
            text='Select All',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._buffer_actions.select_all,
        )
        btn_select_all.pack(side=LEFT, padx=(0, 5))

        btn_copy: Button = Button(
            top_bar,
            text='Copy',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._buffer_actions.copy_log,
        )
        btn_copy.pack(side=LEFT, padx=(0, 5))

        btn_clear: Button = Button(
            top_bar,
            text='Clear',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.clear_log,
        )
        btn_clear.pack(side=LEFT)

    def append_log(self, message: str, tag: str = 'host') -> None:
        '''
            Appends formatted log entry to the console.

            :param message: Log message string.
            :param tag: Styling tag ('tx', 'rx', 'err', 'host').
            :exceptions: None.
        '''
        self._text_log.config(state='normal')
        self._text_log.insert(END, f'{message}\n', tag)
        self._text_log.see(END)
        self._text_log.config(state='disabled')

    def clear_log(self) -> None:
        '''
            Clears console text buffer.

            :exceptions: None.
        '''
        self._buffer_actions.clear_log()

    def get_log_content(self) -> str:
        '''
            Returns current text content from log buffer.

            :return: Stripped text content from the log buffer.
            :exceptions: None.
        '''
        return self._text_log.get('1.0', END).strip()

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
