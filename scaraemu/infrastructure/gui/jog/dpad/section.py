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
    D-pad direction buttons grid component for planar XY, vertical Z, and tool rotation.
'''

from __future__ import annotations

from collections.abc import Callable
from math import radians
from tkinter import Button, FLAT, Frame, Widget
from typing import Final

from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate
from scaraemu.infrastructure.gui.jog.step.iprovider import IJogStepProvider
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogDpad(Frame):
    '''
        Interactive D-pad button matrix for jogging robot axes.

        It defines:

            :attributes:
                | _step_provider - Supplier protocol returning active step size in mm.
                | _delegate - Action delegate receiving jog and homing commands.
            :methods:
                | __init__ - Initializes the D-pad button grid.
                | get_version - Returns component version string.
    '''

    _step_provider: IJogStepProvider
    _delegate: IJogActionDelegate

    def __init__(
        self,
        parent: Widget,
        *,
        step_provider: IJogStepProvider,
        delegate: IJogActionDelegate,
    ) -> None:
        '''
            Initializes the D-pad button grid.

            :param parent: Parent Tkinter widget container.
            :param step_provider: Provider returning active step distance in mm.
            :param delegate: Action delegate handling jog and homing commands.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._step_provider: Final[IJogStepProvider] = step_provider
        self._delegate: Final[IJogActionDelegate] = delegate

        specs: tuple[tuple[str, int, int, Callable[[], None], str, str], ...] = (
            ('Y+', 0, 1, lambda: delegate.handle_jog(0.0, step_provider.get_step(), 0.0, 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('X-', 1, 0, lambda: delegate.handle_jog(-step_provider.get_step(), 0.0, 0.0, 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('H_XY', 1, 1, lambda: delegate.handle_home('xy'), '#3e4451', ThemeManager.ACCENT_CYAN),
            ('X+', 1, 2, lambda: delegate.handle_jog(step_provider.get_step(), 0.0, 0.0, 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('Y-', 2, 1, lambda: delegate.handle_jog(0.0, -step_provider.get_step(), 0.0, 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('Z+', 0, 4, lambda: delegate.handle_jog(0.0, 0.0, step_provider.get_step(), 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('H_Z', 1, 4, lambda: delegate.handle_home('z'), '#3e4451', ThemeManager.ACCENT_CYAN),
            ('Z-', 2, 4, lambda: delegate.handle_jog(0.0, 0.0, -step_provider.get_step(), 0.0), '#313244', ThemeManager.TEXT_PRIMARY),
            ('Φ-', 1, 3, lambda: delegate.handle_jog(0.0, 0.0, 0.0, -radians(10.0)), '#313244', ThemeManager.TEXT_PRIMARY),
            ('Φ+', 1, 5, lambda: delegate.handle_jog(0.0, 0.0, 0.0, radians(10.0)), '#313244', ThemeManager.TEXT_PRIMARY),
        )

        for text, row, col, cmd, bg_color, fg_color in specs:
            btn: Button = Button(
                self,
                text=text,
                bg=bg_color,
                fg=fg_color,
                font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
                width=5,
                relief=FLAT,
                command=cmd,
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
