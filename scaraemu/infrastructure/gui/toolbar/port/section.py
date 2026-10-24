# -*- coding: UTF-8 -*-

'''
Module
    section.py
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
    GUI subcomponent toolbar section for serial port and baud rate selection.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, Label, LEFT, Widget
from tkinter.ttk import Combobox
from typing import Final

from scaracom.transport.preference.preference import SerialPreference
from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortSelectorSection(Frame):
    '''
        Toolbar section for port scanning, dropdown selection, and baud rate configuration.

        It defines:

            :attributes:
                | _port_scanner - Hardware serial port scanning abstraction.
                | _preference_repository - Connection preference persistence repository.
                | _port_combo - Port dropdown selection combobox.
                | _baud_combo - Baudrate dropdown selection combobox.
                | _btn_refresh - Port refresh button.
            :methods:
                | __init__ - Configures and packs port selector widgets.
                | get_connection_parameters - Returns currently selected port path and baud rate.
                | refresh_ports - Scans serial ports and updates dropdown choices.
                | set_enabled - Enables or disables port and baud selectors.
                | get_version - Returns component version string.
    '''

    _port_scanner: IPortScanner
    _preference_repository: ISerialPreferenceRepository
    _port_combo: Combobox
    _baud_combo: Combobox
    _btn_refresh: Button

    def __init__(
        self,
        parent: Widget,
        *,
        port_scanner: IPortScanner,
        preference_repository: ISerialPreferenceRepository,
    ) -> None:
        '''
            Configures and packs port selector widgets.

            :param parent: Parent Tkinter widget container.
            :param port_scanner: Injected IPortScanner discovery port.
            :param preference_repository: Injected ISerialPreferenceRepository port.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER)
        self._port_scanner: Final[IPortScanner] = port_scanner
        self._preference_repository: Final[ISerialPreferenceRepository] = preference_repository

        lbl_port: Label = Label(
            self,
            text='Port:',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
        )
        lbl_port.pack(side=LEFT, padx=(0, 5))

        self._port_combo: Final[Combobox] = Combobox(self, width=16, state='readonly')
        self._port_combo.pack(side=LEFT, padx=(0, 10))

        lbl_baud: Label = Label(
            self,
            text='Baud:',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
        )
        lbl_baud.pack(side=LEFT, padx=(0, 5))

        self._baud_combo: Final[Combobox] = Combobox(self, width=9, state='readonly')
        self._baud_combo['values'] = ('9600', '19200', '38400', '57600', '115200', '250000')
        self._baud_combo.set('115200')
        self._baud_combo.pack(side=LEFT, padx=(0, 10))

        self._btn_refresh: Final[Button] = Button(
            self,
            text='🔄',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.refresh_ports,
        )
        self._btn_refresh.pack(side=LEFT, padx=(0, 8))

        self.refresh_ports()

    def get_connection_parameters(self) -> tuple[str, int]:
        '''
            Returns currently selected port path and baud rate.

            :return: Tuple of (port_path, baud_rate).
            :exceptions: None.
        '''
        port: str = str(self._port_combo.get())
        try:
            baud: int = int(self._baud_combo.get())

        except ValueError:
            baud = 115200

        return (port, baud)

    def refresh_ports(self) -> None:
        '''
            Scans serial ports and updates dropdown choices.

            :exceptions: None.
        '''
        ports = self._port_scanner.scan_ports()
        combo_values: list[str] = ['Virtual / None']

        for p in ports:
            combo_values.append(p if isinstance(p, str) else str(getattr(p, 'device', p)))

        self._port_combo['values'] = combo_values
        default_idx: int = 1 if len(combo_values) > 1 else 0

        if self._preference_repository.has_preference():
            try:
                pref: SerialPreference = self._preference_repository.load_preference()
                if pref.port in combo_values:
                    self._port_combo.set(pref.port)
                else:
                    self._port_combo.current(default_idx)

                if str(pref.baud) in self._baud_combo['values']:
                    self._baud_combo.set(str(pref.baud))

            except Exception:
                self._port_combo.current(default_idx)
        else:
            self._port_combo.current(default_idx)

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables port and baud selectors.

            :param enabled: True to enable, False to disable.
            :exceptions: None.
        '''
        state_str: str = 'readonly' if enabled else 'disabled'
        self._port_combo.config(state=state_str)
        self._baud_combo.config(state=state_str)
        self._btn_refresh.config(state='normal' if enabled else 'disabled')

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
