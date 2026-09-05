# -*- coding: UTF-8 -*-

'''
Module
    telemetry_panel.py
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
    Real-time telemetry readout and hardware status monitor panel.
'''

from __future__ import annotations

from math import degrees
from tkinter import BOTH, Frame, Label, LabelFrame, Widget

from scaraemu.core.model.telemetry_dto import TelemetryDTO
from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPanel(LabelFrame):
    '''
        Panel rendering live Cartesian, joint, and stepper step counts.

        It defines:

            :attributes:
                | _val_x - Cartesian X readout label.
                | _val_y - Cartesian Y readout label.
                | _val_z - Cartesian Z readout label.
                | _val_phi - Tool orientation Phi readout label.
                | _val_q1 - Shoulder Theta1 readout label.
                | _val_q2 - Elbow Theta2 readout label.
                | _val_q4 - Wrist Theta4 readout label.
                | _val_s1 - Step count J1 readout label.
                | _val_s2 - Step count J2 readout label.
                | _val_sz - Step count Z readout label.
                | _val_s4 - Step count J4 readout label.
            :methods:
                | __init__ - Initializes telemetry layout and widgets.
                | update_telemetry - Updates display values from TelemetryDTO.
    '''

    _val_x: Label
    _val_y: Label
    _val_z: Label
    _val_phi: Label
    _val_q1: Label
    _val_q2: Label
    _val_q4: Label
    _val_s1: Label
    _val_s2: Label
    _val_sz: Label
    _val_s4: Label

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes telemetry layout and widgets.

            :param parent: Parent Tkinter widget.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Live Robot Telemetry  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8
        )

        grid_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        grid_frame.pack(fill=BOTH, expand=True)

        self._val_x = self._make_row(grid_frame, 0, 'X Pose:', '0.00 mm', ThemeManager.ACCENT_CYAN)
        self._val_y = self._make_row(grid_frame, 1, 'Y Pose:', '0.00 mm', ThemeManager.ACCENT_CYAN)
        self._val_z = self._make_row(grid_frame, 2, 'Z Height:', '0.00 mm', ThemeManager.ACCENT_CYAN)
        self._val_phi = self._make_row(grid_frame, 3, 'Tool Phi:', '0.00°', ThemeManager.ACCENT_CYAN)

        sep: Frame = Frame(grid_frame, height=1, bg=ThemeManager.BORDER_COLOR)
        sep.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)

        self._val_q1 = self._make_row(grid_frame, 5, 'J1 (Theta1):', '0.00°', ThemeManager.ACCENT_BLUE)
        self._val_q2 = self._make_row(grid_frame, 6, 'J2 (Theta2):', '0.00°', ThemeManager.ACCENT_BLUE)
        self._val_q4 = self._make_row(grid_frame, 7, 'J4 (Theta4):', '0.00°', ThemeManager.ACCENT_BLUE)

        sep2: Frame = Frame(grid_frame, height=1, bg=ThemeManager.BORDER_COLOR)
        sep2.grid(row=8, column=0, columnspan=2, sticky='ew', pady=5)

        self._val_s1 = self._make_row(grid_frame, 9, 'Step J1:', '0', ThemeManager.ACCENT_YELLOW)
        self._val_s2 = self._make_row(grid_frame, 10, 'Step J2:', '0', ThemeManager.ACCENT_YELLOW)
        self._val_sz = self._make_row(grid_frame, 11, 'Step Z:', '0', ThemeManager.ACCENT_YELLOW)
        self._val_s4 = self._make_row(grid_frame, 12, 'Step J4:', '0', ThemeManager.ACCENT_YELLOW)

    def _make_row(self, parent: Frame, row: int, label_text: str, default_val: str, val_color: str) -> Label:
        '''
            Creates a standard label and value pair in the telemetry grid.

            :param parent: Parent frame container.
            :param row: Grid row index.
            :param label_text: Descriptor label text.
            :param default_val: Initial display string.
            :param val_color: Color for value text.
            :return: The value Tkinter Label widget.
            :exceptions: None.
        '''
        lbl: Label = Label(
            parent,
            text=label_text,
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
            anchor='w'
        )
        lbl.grid(row=row, column=0, sticky='w', pady=2)

        val_lbl: Label = Label(
            parent,
            text=default_val,
            bg=ThemeManager.BG_PANEL,
            fg=val_color,
            font=(ThemeManager.FONT_MONO, 9, 'bold'),
            anchor='e'
        )
        val_lbl.grid(row=row, column=1, sticky='e', padx=(15, 0), pady=2)
        return val_lbl

    def update_telemetry(self, telem: TelemetryDTO) -> None:
        '''
            Updates display values from TelemetryDTO.

            :param telem: Current TelemetryDTO snapshot.
            :exceptions: None.
        '''
        if not self.winfo_ismapped():
            return

        self._val_x.config(text=f'{telem.pose.x:.2f} mm')
        self._val_y.config(text=f'{telem.pose.y:.2f} mm')
        self._val_z.config(text=f'{telem.pose.z:.2f} mm')
        self._val_phi.config(text=f'{degrees(telem.pose.phi):.2f}°')

        self._val_q1.config(text=f'{degrees(telem.joints.theta1):.2f}°')
        self._val_q2.config(text=f'{degrees(telem.joints.theta2):.2f}°')
        self._val_q4.config(text=f'{degrees(telem.joints.theta4):.2f}°')

        self._val_s1.config(text=f'{telem.steps.j1_steps:,}')
        self._val_s2.config(text=f'{telem.steps.j2_steps:,}')
        self._val_sz.config(text=f'{telem.steps.z_steps:,}')
        self._val_s4.config(text=f'{telem.steps.j4_steps:,}')
