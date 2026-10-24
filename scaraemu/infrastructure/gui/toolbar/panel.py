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
    Top toolbar component for serial communication bridge configuration.
'''

from __future__ import annotations

from tkinter import Frame, Label, LEFT, RIGHT, Widget
from typing import Final

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate
from scaraemu.infrastructure.gui.toolbar.connection.section import ConnectionSection
from scaraemu.infrastructure.gui.toolbar.port.section import PortSelectorSection
from scaraemu.infrastructure.gui.toolbar.server.section import ServerToggleSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialBar(Frame):
    '''
        Toolbar composite assembling port selection, connection toggle, and virtual server.

        It defines:

            :attributes:
                | _port_section - Port scanner and baudrate selector subcomponent.
                | _connection_section - Hardware connection toggle and status subcomponent.
                | _server_section - Virtual TCP robot server toggle subcomponent.
            :methods:
                | __init__ - Configures and packs UI toolbar subcomponents.
                | set_connected_state - Updates connection section and port selection availability.
                | set_server_state - Updates virtual server button state in server section.
                | get_version - Returns toolbar component version string.
    '''

    _port_section: PortSelectorSection
    _connection_section: ConnectionSection
    _server_section: ServerToggleSection

    def __init__(
        self,
        parent: Widget,
        *,
        delegate: IActionDelegate,
        port_scanner: IPortScanner,
        preference_repository: ISerialPreferenceRepository,
    ) -> None:
        '''
            Initializes toolbar composite with port selector, connection, and server sections.

            :param parent: Parent Tkinter container.
            :param delegate: Action delegate handling connect and server events.
            :param port_scanner: Injected IPortScanner discovery port.
            :param preference_repository: Injected ISerialPreferenceRepository port.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER, height=42, padx=10, pady=5)

        lbl_title: Label = Label(
            self,
            text='SCARA EMU',
            bg=ThemeManager.BG_HEADER,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 11, 'bold'),
        )
        lbl_title.pack(side=LEFT, padx=(0, 15))

        self._port_section: Final[PortSelectorSection] = PortSelectorSection(
            self,
            port_scanner=port_scanner,
            preference_repository=preference_repository,
        )
        self._port_section.pack(side=LEFT)

        self._connection_section: Final[ConnectionSection] = ConnectionSection(
            self,
            port_provider=self._port_section,
            delegate=delegate,
        )
        self._connection_section.pack(side=LEFT)

        self._server_section: Final[ServerToggleSection] = ServerToggleSection(
            self,
            delegate=delegate,
        )
        self._server_section.pack(side=RIGHT)

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates button text and status label based on connection state.

            :param connected: True if connected, False otherwise.
            :exceptions: None.
        '''
        self._port_section.set_enabled(not connected)
        self._connection_section.set_connected_state(connected)

    def set_server_state(self, running: bool, port: int = 8888) -> None:
        '''
            Updates virtual server button appearance.

            :param running: True if server active, False otherwise.
            :param port: Listening TCP port number.
            :exceptions: None.
        '''
        self._server_section.set_server_state(running, port)

    def get_version(self) -> str:
        '''
            Returns toolbar component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
