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
    GUI subcomponent toolbar section for virtual robot TCP server toggling.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, RIGHT, Widget
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerToggleSection(Frame):
    '''
        Toolbar section for toggling virtual robot server and displaying its state.

        It defines:

            :attributes:
                | _delegate - Action delegate handling server toggle events.
                | _btn_server - Virtual robot server toggle button.
            :methods:
                | __init__ - Configures and packs virtual server toggle controls.
                | set_server_state - Updates button appearance and text based on server state.
                | get_button - Returns server toggle button for inspection and interactions.
                | get_version - Returns component version string.
    '''

    _delegate: IActionDelegate
    _btn_server: Button

    def __init__(self, parent: Widget, *, delegate: IActionDelegate) -> None:
        '''
            Configures and packs virtual server toggle controls.

            :param parent: Parent Tkinter widget container.
            :param delegate: Action delegate handling server toggle.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_HEADER)
        self._delegate: Final[IActionDelegate] = delegate

        self._btn_server: Final[Button] = Button(
            self,
            text='🌐 Virtual Server: OFF',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            relief=FLAT,
            command=delegate.handle_server_toggle,
        )
        self._btn_server.pack(side=RIGHT, padx=(10, 0))

    def set_server_state(self, running: bool, port: int = 8888) -> None:
        '''
            Updates virtual server button appearance.

            :param running: True if server active, False otherwise.
            :param port: Listening TCP port number.
            :exceptions: None.
        '''
        if running:
            self._btn_server.config(
                text=f'🌐 Virtual Server: :{port}',
                bg=ThemeManager.ACCENT_GREEN,
                fg='#11111b',
            )
        else:
            self._btn_server.config(
                text='🌐 Virtual Server: OFF',
                bg='#45475a',
                fg=ThemeManager.TEXT_PRIMARY,
            )

    def get_button(self) -> Button:
        '''
            Returns server toggle button for inspection and interactions.

            :return: Button widget instance.
            :exceptions: None.
        '''
        return self._btn_server

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
