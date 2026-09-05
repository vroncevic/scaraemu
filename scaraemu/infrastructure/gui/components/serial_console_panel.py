# -*- coding: UTF-8 -*-

'''
Module
    serial_console_panel.py
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
    Interactive serial terminal console and telemetry logger component.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    END,
    FLAT,
    INSERT,
    LEFT,
    RIGHT,
    SEL,
    SEL_FIRST,
    SEL_LAST,
    X,
    Y,
    Button,
    Frame,
    LabelFrame,
    Scrollbar,
    TclError,
    Text,
    Widget,
)
from tkinter.ttk import Entry
from typing import Callable

from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsolePanel(LabelFrame):
    '''
        Serial packet console logger and manual command transmitter.

        It defines:

            :attributes:
                | _text_log - Scrolled text logging area.
                | _entry_cmd - Manual command text entry.
                | _on_send_cmd - Callback when user submits manual command string.
            :methods:
                | __init__ - Initializes console widgets and styling tags.
                | append_log - Appends formatted log entry to the console.
                | select_all - Selects all text content in the console log buffer.
                | copy_log - Copies selected or entire console log content to clipboard.
                | clear_log - Clears console text buffer.
    '''

    _text_log: Text
    _entry_cmd: Entry
    _on_send_cmd: Callable[[str], None] | None

    def __init__(
        self,
        parent: Widget,
        on_send_cmd: Callable[[str], None] | None = None
    ) -> None:
        '''
            Initializes console widgets and styling tags.

            :param parent: Parent Tkinter widget.
            :param on_send_cmd: Callback for transmitting manual command string.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Serial Communication Console  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8
        )
        self._on_send_cmd = on_send_cmd

        top_bar: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        top_bar.pack(fill=X, pady=(0, 5))

        btn_clear: Button = Button(
            top_bar,
            text='Clear Log',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.clear_log
        )
        btn_clear.pack(side=RIGHT, padx=(4, 0))

        btn_copy: Button = Button(
            top_bar,
            text='Copy',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.copy_log
        )
        btn_copy.pack(side=RIGHT, padx=(4, 0))

        btn_select_all: Button = Button(
            top_bar,
            text='Select All',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.select_all
        )
        btn_select_all.pack(side=RIGHT, padx=(4, 0))

        log_frame: Frame = Frame(self, bg=ThemeManager.BG_CANVAS)
        log_frame.pack(fill=BOTH, expand=True, pady=(0, 8))

        scroll: Scrollbar = Scrollbar(log_frame)
        scroll.pack(side=RIGHT, fill=Y)

        self._text_log = Text(
            log_frame,
            width=1,
            height=6,
            bg=ThemeManager.BG_CANVAS,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_MONO, 8),
            yscrollcommand=scroll.set,
            relief=FLAT,
            state='disabled'
        )
        self._text_log.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.config(command=self._text_log.yview)

        self._text_log.bind('<Control-a>', lambda e: (self.select_all(), 'break')[1])
        self._text_log.bind('<Control-c>', lambda e: (self.copy_log(), 'break')[1])

        self._text_log.tag_config('tx', foreground=ThemeManager.ACCENT_CYAN)
        self._text_log.tag_config('rx', foreground=ThemeManager.ACCENT_GREEN)
        self._text_log.tag_config('err', foreground=ThemeManager.ACCENT_RED)
        self._text_log.tag_config('host', foreground=ThemeManager.TEXT_SECONDARY)

        input_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        input_frame.pack(fill=X)

        self._entry_cmd = Entry(input_frame)
        self._entry_cmd.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        self._entry_cmd.bind('<Return>', lambda e: self._send())

        btn_send: Button = Button(
            input_frame,
            text='Send',
            bg=ThemeManager.ACCENT_BLUE,
            fg='#11111b',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=FLAT,
            command=self._send
        )
        btn_send.pack(side=RIGHT)

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

    def select_all(self) -> None:
        '''
            Selects all text content in the console log buffer.

            :exceptions: None.
        '''
        self._text_log.tag_add(SEL, '1.0', END)
        self._text_log.mark_set(INSERT, '1.0')
        self._text_log.see(INSERT)
        self._text_log.focus_set()

    def copy_log(self) -> None:
        '''
            Copies selected or entire console log content to clipboard.

            :exceptions: None.
        '''
        try:
            content: str = self._text_log.get(SEL_FIRST, SEL_LAST)
        except TclError:
            content = self._text_log.get('1.0', END).strip()

        if content:
            self.clipboard_clear()
            self.clipboard_append(content)

    def clear_log(self) -> None:
        '''
            Clears console text buffer.

            :exceptions: None.
        '''
        self._text_log.config(state='normal')
        self._text_log.delete('1.0', END)
        self._text_log.config(state='disabled')

    def _send(self) -> None:
        '''
            Handles submission of manual command.

            :exceptions: None.
        '''
        cmd = self._entry_cmd.get().strip()
        if cmd and self._on_send_cmd is not None:
            self._entry_cmd.delete(0, END)
            self._on_send_cmd(cmd)
