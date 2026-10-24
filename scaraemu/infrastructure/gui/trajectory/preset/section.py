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
    Preset autonomous demonstration trajectory button grid subcomponent.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, Widget
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPresetSection(Frame):
    '''
        Subcomponent grid for selecting predefined demo trajectory patterns.

        It defines:

            :attributes:
                | _delegate - Action delegate receiving demo preset selection.
            :methods:
                | __init__ - Initializes demo preset button grid.
                | select_preset - Dispatches demo preset selection to delegate.
                | get_version - Returns component version string.
    '''

    _delegate: ITrajectoryPresetDelegate

    def __init__(self, parent: Widget, delegate: ITrajectoryPresetDelegate) -> None:
        '''
            Initializes demo preset button grid.

            :param parent: Parent Tkinter widget container.
            :param delegate: Action delegate with handle_demo_select method.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._delegate: Final[ITrajectoryPresetDelegate] = delegate

        specs: tuple[tuple[str, str, int, int, int], ...] = (
            ('Circle', 'circle', 0, 0, 1),
            ('Square', 'square', 0, 1, 1),
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        for label, preset_name, r, c, span in specs:
            btn: Button = Button(
                self,
                text=label,
                bg='#45475a',
                fg=ThemeManager.TEXT_PRIMARY,
                font=(ThemeManager.FONT_FAMILY, 8),
                relief=FLAT,
                command=lambda p=preset_name: delegate.handle_demo_select(p),
            )
            btn.grid(row=r, column=c, columnspan=span, sticky='ew', padx=2, pady=2)

    def select_preset(self, preset_name: str) -> None:
        '''
            Dispatches demo preset selection to delegate.

            :param preset_name: Predefined demo trajectory pattern.
            :exceptions: None.
        '''
        self._delegate.handle_demo_select(preset_name)

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
