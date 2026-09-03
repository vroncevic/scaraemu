# -*- coding: UTF-8 -*-

'''
Module
    serial_bar.py
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
    Top toolbar component for serial communication bridge configuration.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from scaraemu.infrastructure.gui.theme import ThemeManager
from scaraemu.infrastructure.communication.serial_port_scanner import SerialPortScanner
from scaraemu.infrastructure.communication.serial_device_preferences import SerialDevicePreferences

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialBar(tk.Frame):
    '''
        Toolbar for scanning ports, selecting baudrate, and toggling hardware bridge connection.

        It defines:

            :attributes:
                | _port_combo - Port dropdown selection.
                | _baud_combo - Baudrate dropdown selection.
                | _btn_connect - Connect / Disconnect button.
                | _lbl_status - Connection status label.
                | _on_connect_toggle - Callback for connecting/disconnecting.
            :methods:
                | __init__ - Initializes toolbar widgets and layouts.
                | refresh_ports - Scans system for available serial ports.
                | set_connected_state - Updates button text and status label based on connection state.
    '''

    _port_combo: ttk.Combobox
    _baud_combo: ttk.Combobox
    _btn_connect: tk.Button
    _lbl_status: tk.Label
    _on_connect_toggle: Callable[[str, int], None] | None

    def __init__(
        self,
        parent: tk.Widget,
        on_connect_toggle: Callable[[str, int], None] | None = None
    ) -> None:
        '''
            Initializes toolbar widgets and layouts.

            :param parent: Parent Tkinter container.
            :param on_connect_toggle: Callback when connect/disconnect button is pressed.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER, height=42, padx=10, pady=5)
        self._on_connect_toggle = on_connect_toggle

        lbl_title: tk.Label = tk.Label(
            self,
            text='SCARA EMU',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 11, 'bold')
        )
        lbl_title.pack(side=tk.LEFT, padx=(0, 15))

        lbl_port: tk.Label = tk.Label(
            self,
            text='Port:',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9)
        )
        lbl_port.pack(side=tk.LEFT, padx=(0, 5))

        self._port_combo = ttk.Combobox(self, width=14, state='readonly')
        self._port_combo.pack(side=tk.LEFT, padx=(0, 5))
        self._port_combo.bind('<<ComboboxSelected>>', lambda e: self._save_active_pref())

        btn_refresh: tk.Button = tk.Button(
            self,
            text='↻',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_PRIMARY,
            activebackground=ThemeManager.BORDER_COLOR,
            relief=tk.FLAT,
            command=self.refresh_ports
        )
        btn_refresh.pack(side=tk.LEFT, padx=(0, 10))

        lbl_baud: tk.Label = tk.Label(
            self,
            text='Baud:',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9)
        )
        lbl_baud.pack(side=tk.LEFT, padx=(0, 5))

        self._baud_combo = ttk.Combobox(
            self,
            width=8,
            values=['9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600'],
            state='readonly'
        )
        self._baud_combo.set('115200')
        self._baud_combo.pack(side=tk.LEFT, padx=(0, 10))
        self._baud_combo.bind('<<ComboboxSelected>>', lambda e: self._save_active_pref())

        self._btn_connect = tk.Button(
            self,
            text='Connect',
            bg=ThemeManager.ACCENT_BLUE,
            fg='#11111b',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            command=self._handle_click
        )
        self._btn_connect.pack(side=tk.LEFT, padx=(0, 15))

        self._lbl_status = tk.Label(
            self,
            text='● Disconnected',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9)
        )
        self._lbl_status.pack(side=tk.LEFT)

        self.refresh_ports()

    def refresh_ports(self) -> None:
        '''
            Scans system for available serial ports.

            :exceptions: None.
        '''
        current_selection: str = self._port_combo.get()
        saved_port, saved_baud = SerialDevicePreferences.load_preference()

        ports = SerialPortScanner.list_ports()
        if not ports:
            ports = ['Virtual / None']
        self._port_combo['values'] = ports

        if current_selection in ports:
            self._port_combo.set(current_selection)
        elif saved_port and saved_port in ports:
            self._port_combo.set(saved_port)
        elif ports:
            self._port_combo.current(0)
        else:
            self._port_combo.set('')

        if saved_baud:
            self._baud_combo.set(str(saved_baud))

    def _save_active_pref(self) -> None:
        '''
            Persists selected port and baud rate to preferences.

            :exceptions: None.
        '''
        port: str = self._port_combo.get()
        try:
            baud: int = int(self._baud_combo.get())
        except ValueError:
            baud = 115200
        if port and port != 'Virtual / None':
            SerialDevicePreferences.save_preference(port, baud)

    def _handle_click(self) -> None:
        '''
            Handles click event for connecting or disconnecting.

            :exceptions: None.
        '''
        if self._on_connect_toggle is not None:
            port: str = self._port_combo.get()
            try:
                baud: int = int(self._baud_combo.get())
            except ValueError:
                baud = 115200
            self._save_active_pref()
            self._on_connect_toggle(port, baud)

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button text and status label based on connection state.

            :param connected: True if connected, False otherwise.
            :exceptions: None.
        '''
        if connected:
            self._btn_connect.config(text='Disconnect', bg=ThemeManager.ACCENT_RED, fg='#ffffff')
            self._lbl_status.config(text='● Connected (Bridge Active)', fg=ThemeManager.ACCENT_GREEN)
            self._port_combo.config(state='disabled')
            self._baud_combo.config(state='disabled')
        else:
            self._btn_connect.config(text='Connect', bg=ThemeManager.ACCENT_BLUE, fg='#11111b')
            self._lbl_status.config(text='● Disconnected', fg=ThemeManager.TEXT_SECONDARY)
            self._port_combo.config(state='readonly')
            self._baud_combo.config(state='readonly')
