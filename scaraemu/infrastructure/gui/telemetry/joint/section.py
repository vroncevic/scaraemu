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
    GUI subcomponent for rendering joint angle telemetry readouts.
'''

from __future__ import annotations

from math import degrees
from tkinter import Frame, Label, Widget
from typing import Final

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointSection(Frame):
    '''
        Subcomponent grid displaying robot joint angles Theta1, Theta2, and Theta4.

        It defines:

            :attributes:
                | _val_q1 - Shoulder Theta1 angle readout label.
                | _val_q2 - Elbow Theta2 angle readout label.
                | _val_q4 - Wrist Theta4 angle readout label.
            :methods:
                | __init__ - Initializes joint angle readout labels.
                | update_joints - Updates displayed angles from ScaraJoints model.
                | get_readouts - Returns current formatted joint readout strings.
                | get_version - Returns component version string.
    '''

    _val_q1: Label
    _val_q2: Label
    _val_q4: Label

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes joint angle readout labels.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        lbl_q1: Label = Label(
            self,
            text='J1 (Theta1):',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_q1.grid(row=0, column=0, sticky='w', pady=2)
        self._val_q1: Final[Label] = Label(
            self,
            text='0.00°',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_BLUE,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_q1.grid(row=0, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_q2: Label = Label(
            self,
            text='J2 (Theta2):',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_q2.grid(row=1, column=0, sticky='w', pady=2)
        self._val_q2: Final[Label] = Label(
            self,
            text='0.00°',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_BLUE,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_q2.grid(row=1, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_q4: Label = Label(
            self,
            text='J4 (Theta4):',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_q4.grid(row=2, column=0, sticky='w', pady=2)
        self._val_q4: Final[Label] = Label(
            self,
            text='0.00°',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_BLUE,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_q4.grid(row=2, column=1, sticky='e', padx=(15, 0), pady=2)

    def update_joints(self, joints: ScaraJoints) -> None:
        '''
            Updates displayed angles from ScaraJoints model.

            :param joints: Current joint angles snapshot.
            :exceptions: None.
        '''
        self._val_q1.config(text=f'{degrees(joints.theta1):.2f}°')
        self._val_q2.config(text=f'{degrees(joints.theta2):.2f}°')
        self._val_q4.config(text=f'{degrees(joints.theta4):.2f}°')

    def get_readouts(self) -> tuple[str, str, str]:
        '''
            Returns current formatted joint readout strings.

            :return: Tuple containing (q1, q2, q4) text values.
            :exceptions: None.
        '''
        return (
            self._val_q1.cget('text'),
            self._val_q2.cget('text'),
            self._val_q4.cget('text'),
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
