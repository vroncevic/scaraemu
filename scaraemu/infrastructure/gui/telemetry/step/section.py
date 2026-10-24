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
    GUI subcomponent for rendering stepper motor step count telemetry readouts.
'''

from __future__ import annotations

from tkinter import Frame, Label, Widget
from typing import Final

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepSection(Frame):
    '''
        Subcomponent grid displaying stepper motor step counts J1, J2, Z, and J4.

        It defines:

            :attributes:
                | _val_s1 - Stepper J1 step count readout label.
                | _val_s2 - Stepper J2 step count readout label.
                | _val_sz - Stepper Z step count readout label.
                | _val_s4 - Stepper J4 step count readout label.
            :methods:
                | __init__ - Initializes step count readout labels.
                | update_steps - Updates displayed step counts from ScaraStepCoords model.
                | get_readouts - Returns current formatted step count readout strings.
                | get_version - Returns component version string.
    '''

    _val_s1: Label
    _val_s2: Label
    _val_sz: Label
    _val_s4: Label

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes step count readout labels.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        lbl_s1: Label = Label(
            self,
            text='Step J1:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_s1.grid(row=0, column=0, sticky='w', pady=2)
        self._val_s1: Final[Label] = Label(
            self,
            text='0',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_YELLOW,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_s1.grid(row=0, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_s2: Label = Label(
            self,
            text='Step J2:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_s2.grid(row=1, column=0, sticky='w', pady=2)
        self._val_s2: Final[Label] = Label(
            self,
            text='0',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_YELLOW,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_s2.grid(row=1, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_sz: Label = Label(
            self,
            text='Step Z:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_sz.grid(row=2, column=0, sticky='w', pady=2)
        self._val_sz: Final[Label] = Label(
            self,
            text='0',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_YELLOW,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_sz.grid(row=2, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_s4: Label = Label(
            self,
            text='Step J4:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_s4.grid(row=3, column=0, sticky='w', pady=2)
        self._val_s4: Final[Label] = Label(
            self,
            text='0',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_YELLOW,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_s4.grid(row=3, column=1, sticky='e', padx=(15, 0), pady=2)

    def update_steps(self, steps: ScaraStepCoords) -> None:
        '''
            Updates displayed step counts from ScaraStepCoords model.

            :param steps: Current stepper step counts snapshot.
            :exceptions: None.
        '''
        self._val_s1.config(text=f'{steps.j1_steps:,}')
        self._val_s2.config(text=f'{steps.j2_steps:,}')
        self._val_sz.config(text=f'{steps.z_steps:,}')
        self._val_s4.config(text=f'{steps.j4_steps:,}')

    def get_readouts(self) -> tuple[str, str, str, str]:
        '''
            Returns current formatted step count readout strings.

            :return: Tuple containing (s1, s2, sz, s4) text values.
            :exceptions: None.
        '''
        return (
            self._val_s1.cget('text'),
            self._val_s2.cget('text'),
            self._val_sz.cget('text'),
            self._val_s4.cget('text'),
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
