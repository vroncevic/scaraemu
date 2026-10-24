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
    GUI subcomponent for rendering Cartesian tool pose coordinates.
'''

from __future__ import annotations

from math import degrees
from tkinter import Frame, Label, Widget
from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianSection(Frame):
    '''
        Subcomponent grid displaying Cartesian X, Y, Z coordinates and tool angle Phi.

        It defines:

            :attributes:
                | _val_x - Cartesian X readout label.
                | _val_y - Cartesian Y readout label.
                | _val_z - Cartesian Z height readout label.
                | _val_phi - Tool orientation Phi readout label.
            :methods:
                | __init__ - Initializes Cartesian readout labels.
                | update_pose - Updates displayed coordinates from ScaraPose model.
                | get_readouts - Returns current formatted Cartesian readout strings.
                | get_version - Returns component version string.
    '''

    _val_x: Label
    _val_y: Label
    _val_z: Label
    _val_phi: Label

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes Cartesian readout labels.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        lbl_x: Label = Label(
            self,
            text='X Pose:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_x.grid(row=0, column=0, sticky='w', pady=2)
        self._val_x: Final[Label] = Label(
            self,
            text='0.00 mm',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_x.grid(row=0, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_y: Label = Label(
            self,
            text='Y Pose:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_y.grid(row=1, column=0, sticky='w', pady=2)
        self._val_y: Final[Label] = Label(
            self,
            text='0.00 mm',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_y.grid(row=1, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_z: Label = Label(
            self,
            text='Z Height:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_z.grid(row=2, column=0, sticky='w', pady=2)
        self._val_z: Final[Label] = Label(
            self,
            text='0.00 mm',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_z.grid(row=2, column=1, sticky='e', padx=(15, 0), pady=2)

        lbl_phi: Label = Label(
            self,
            text='Tool Phi:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w',
        )
        lbl_phi.grid(row=3, column=0, sticky='w', pady=2)
        self._val_phi: Final[Label] = Label(
            self,
            text='0.00°',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e',
        )
        self._val_phi.grid(row=3, column=1, sticky='e', padx=(15, 0), pady=2)

    def update_pose(self, pose: ScaraPose) -> None:
        '''
            Updates displayed coordinates from ScaraPose model.

            :param pose: Current Cartesian pose snapshot.
            :exceptions: None.
        '''
        self._val_x.config(text=f'{pose.x:.2f} mm')
        self._val_y.config(text=f'{pose.y:.2f} mm')
        self._val_z.config(text=f'{pose.z:.2f} mm')
        self._val_phi.config(text=f'{degrees(pose.phi):.2f}°')

    def get_readouts(self) -> tuple[str, str, str, str]:
        '''
            Returns current formatted Cartesian readout strings.

            :return: Tuple containing (x, y, z, phi) text values.
            :exceptions: None.
        '''
        return (
            self._val_x.cget('text'),
            self._val_y.cget('text'),
            self._val_z.cget('text'),
            self._val_phi.cget('text'),
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
