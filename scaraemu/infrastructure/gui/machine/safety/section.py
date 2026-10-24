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
    GUI subcomponent providing feed-hold pause and emergency stop safety controls.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, LEFT, Widget, X
from typing import Final

from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SafetySection(Frame):
    '''
        Subcomponent toolbar providing feed-hold pause and emergency stop buttons.

        It defines:

            :attributes:
                | _safety_delegate - Action delegate for safety and hold operations.
            :methods:
                | __init__ - Initializes safety override toolbar buttons.
                | get_buttons - Returns child safety action buttons tuple.
                | get_version - Returns component version string.
    '''

    _safety_delegate: ISafetyDelegate
    _btn_hold: Button
    _btn_estop: Button

    def __init__(
        self,
        parent: Widget,
        *,
        safety_delegate: ISafetyDelegate,
    ) -> None:
        '''
            Initializes safety override toolbar buttons.

            :param parent: Parent Tkinter widget container.
            :param safety_delegate: Delegate for hold and emergency stop actions.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._safety_delegate: Final[ISafetyDelegate] = safety_delegate

        self._btn_hold: Final[Button] = Button(
            self,
            text='HOLD',
            bg=ThemeManager.ACCENT_ORANGE,
            fg='#1e1e2e',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=FLAT,
            command=safety_delegate.handle_toggle_hold,
        )
        self._btn_hold.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))

        self._btn_estop: Final[Button] = Button(
            self,
            text='E-STOP',
            bg=ThemeManager.ACCENT_RED,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=FLAT,
            command=safety_delegate.handle_estop,
        )
        self._btn_estop.pack(side=LEFT, expand=True, fill=X)

    def get_buttons(self) -> tuple[Button, Button]:
        '''
            Returns child safety action buttons tuple.

            :return: Tuple containing (hold_button, estop_button).
            :exceptions: None.
        '''
        return (self._btn_hold, self._btn_estop)

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
