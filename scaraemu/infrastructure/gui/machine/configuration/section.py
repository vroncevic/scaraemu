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
    GUI subcomponent providing machine kinematic and actuator configuration buttons.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, LEFT, Widget, X
from typing import Final

from scaraemu.infrastructure.gui.machine.configuration.idelegate import IConfigurationDelegate
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigurationSection(Frame):
    '''
        Subcomponent toolbar providing elbow configuration and motor power toggle controls.

        It defines:

            :attributes:
                | _config_delegate - Action delegate for machine orientation and power toggling.
            :methods:
                | __init__ - Initializes configuration toolbar buttons.
                | get_buttons - Returns child configuration action buttons tuple.
                | get_version - Returns component version string.
    '''

    _config_delegate: IConfigurationDelegate
    _btn_elbow: Button
    _btn_motors: Button

    def __init__(
        self,
        parent: Widget,
        *,
        config_delegate: IConfigurationDelegate,
    ) -> None:
        '''
            Initializes configuration toolbar buttons.

            :param parent: Parent Tkinter widget container.
            :param config_delegate: Delegate for elbow and motor power actions.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._config_delegate: Final[IConfigurationDelegate] = config_delegate

        self._btn_elbow: Final[Button] = Button(
            self,
            text='Toggle Lefty/Righty',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=config_delegate.handle_toggle_elbow,
        )
        self._btn_elbow.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))

        self._btn_motors: Final[Button] = Button(
            self,
            text='Toggle Motors',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=config_delegate.handle_toggle_motors,
        )
        self._btn_motors.pack(side=LEFT, expand=True, fill=X)

    def get_buttons(self) -> tuple[Button, Button]:
        '''
            Returns child configuration action buttons tuple.

            :return: Tuple containing (elbow_button, motors_button).
            :exceptions: None.
        '''
        return (self._btn_elbow, self._btn_motors)

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
