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
    GUI subcomponent toolbar section for hardware connection toggle and status.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, Label, LEFT, Widget
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate
from scaraemu.infrastructure.gui.toolbar.port.iprovider import IConnectionParameterProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionSection(Frame):
    '''
        Toolbar section providing connect/disconnect toggle button and status label.

        It defines:

            :attributes:
                | _port_provider - Parameter provider returning port and baud rate.
                | _delegate - Action delegate handling connection toggle.
                | _btn_connect - Hardware connect/disconnect toggle button.
                | _lbl_status - Connection state indicator label.
            :methods:
                | __init__ - Configures and packs connection controls.
                | set_connected_state - Updates button appearance and status text.
                | get_button - Returns connect/disconnect button for inspection and interactions.
                | get_version - Returns component version string.
    '''

    _port_provider: IConnectionParameterProvider
    _delegate: IActionDelegate
    _btn_connect: Button
    _lbl_status: Label

    def __init__(
        self,
        parent: Widget,
        *,
        port_provider: IConnectionParameterProvider,
        delegate: IActionDelegate,
    ) -> None:
        '''
            Configures and packs connection controls.

            :param parent: Parent Tkinter widget container.
            :param port_provider: Provider returning selected port and baud.
            :param delegate: Action delegate handling connect toggle.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER)
        self._port_provider: Final[IConnectionParameterProvider] = port_provider
        self._delegate: Final[IActionDelegate] = delegate

        self._btn_connect: Final[Button] = Button(
            self,
            text='Connect',
            bg=ThemeManager.ACCENT_BLUE,
            fg='#11111b',
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            relief=FLAT,
            command=lambda: delegate.handle_connect_toggle(
                *port_provider.get_connection_parameters(),
            ),
        )
        self._btn_connect.pack(side=LEFT, padx=(0, 15))

        self._lbl_status: Final[Label] = Label(
            self,
            text='● Disconnected',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
        )
        self._lbl_status.pack(side=LEFT, padx=(0, 15))

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button appearance and status text based on connection state.

            :param connected: True if connected, False otherwise.
            :exceptions: None.
        '''
        if connected:
            self._btn_connect.config(text='Disconnect', bg=ThemeManager.ACCENT_RED, fg='#ffffff')
            self._lbl_status.config(text='● Connected (Bridge Active)', fg=ThemeManager.ACCENT_GREEN)
        else:
            self._btn_connect.config(text='Connect', bg=ThemeManager.ACCENT_BLUE, fg='#11111b')
            self._lbl_status.config(text='● Disconnected', fg=ThemeManager.TEXT_SECONDARY)

    def get_button(self) -> Button:
        '''
            Returns connect/disconnect button for inspection and interactions.

            :return: Button widget instance.
            :exceptions: None.
        '''
        return self._btn_connect

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
