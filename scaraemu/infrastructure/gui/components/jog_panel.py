# -*- coding: UTF-8 -*-

'''
Module
    jog_panel.py
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
    Manual Cartesian and joint jog control panel component.
'''

from __future__ import annotations

import math
import tkinter as tk
from typing import Callable

from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanel(tk.LabelFrame):
    '''
        Manual jog and movement direction controls with step resolution selector.

        It defines:

            :attributes:
                | _step_var - Active step size in mm.
                | _on_jog - Callback receiving (dx, dy, dz, dphi).
                | _on_home_xy - Callback for homing planar XY axes.
                | _on_home_z - Callback for homing vertical Z axis.
                | _on_toggle_elbow - Callback for elbow solution toggling.
                | _on_toggle_motors - Callback for motor driver power toggling.
                | _on_estop - Callback for emergency stop.
            :methods:
                | __init__ - Initializes jog buttons and control elements.
    '''

    _step_var: tk.DoubleVar
    _on_jog: Callable[[float, float, float, float], None] | None
    _on_home_xy: Callable[[], None] | None
    _on_home_z: Callable[[], None] | None
    _on_toggle_elbow: Callable[[], None] | None
    _on_toggle_motors: Callable[[], None] | None
    _on_estop: Callable[[], None] | None

    def __init__(
        self,
        parent: tk.Widget,
        on_jog: Callable[[float, float, float, float], None] | None = None,
        on_home_xy: Callable[[], None] | None = None,
        on_home_z: Callable[[], None] | None = None,
        on_toggle_elbow: Callable[[], None] | None = None,
        on_toggle_motors: Callable[[], None] | None = None,
        on_estop: Callable[[], None] | None = None
    ) -> None:
        '''
            Initializes jog buttons and control elements.

            :param parent: Parent Tkinter widget.
            :param on_jog: Callback for incremental displacement (dx, dy, dz, dphi).
            :param on_home_xy: Callback for homing XY planar axes.
            :param on_home_z: Callback for homing Z vertical axis.
            :param on_toggle_elbow: Callback for toggling elbow-left/right.
            :param on_toggle_motors: Callback for motor enable/disable.
            :param on_estop: Callback for emergency stop.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Manual Jog Controls  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8
        )
        self._on_jog = on_jog
        self._on_home_xy = on_home_xy
        self._on_home_z = on_home_z
        self._on_toggle_elbow = on_toggle_elbow
        self._on_toggle_motors = on_toggle_motors
        self._on_estop = on_estop

        step_frame: tk.Frame = tk.Frame(self, bg=ThemeManager.BG_PANEL)
        step_frame.pack(fill=tk.X, pady=(0, 8))

        lbl_step: tk.Label = tk.Label(
            step_frame,
            text='Step:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9)
        )
        lbl_step.pack(side=tk.LEFT, padx=(0, 5))

        self._step_var = tk.DoubleVar(value=5.0)
        for s in (1.0, 5.0, 10.0, 25.0):
            rb = tk.Radiobutton(
                step_frame,
                text=f'{s:.0f}mm',
                value=s,
                variable=self._step_var,
                bg=ThemeManager.BG_PANEL,
                fg=ThemeManager.TEXT_PRIMARY,
                selectcolor=ThemeManager.BG_CANVAS,
                activebackground=ThemeManager.BG_PANEL,
                font=(ThemeManager.FONT_FAMILY, 8)
            )
            rb.pack(side=tk.LEFT, padx=2)

        btn_grid: tk.Frame = tk.Frame(self, bg=ThemeManager.BG_PANEL)
        btn_grid.pack(fill=tk.X, pady=4)

        self._btn(btn_grid, 'Y+', 0, 1, lambda: self._do_jog(0.0, self._get_step(), 0.0, 0.0))
        self._btn(btn_grid, 'X-', 1, 0, lambda: self._do_jog(-self._get_step(), 0.0, 0.0, 0.0))
        self._btn(btn_grid, 'H_XY', 1, 1, self._handle_home_xy, bg='#3e4451', fg=ThemeManager.ACCENT_CYAN)
        self._btn(btn_grid, 'X+', 1, 2, lambda: self._do_jog(self._get_step(), 0.0, 0.0, 0.0))
        self._btn(btn_grid, 'Y-', 2, 1, lambda: self._do_jog(0.0, -self._get_step(), 0.0, 0.0))

        self._btn(btn_grid, 'Z+', 0, 4, lambda: self._do_jog(0.0, 0.0, self._get_step(), 0.0))
        self._btn(btn_grid, 'H_Z', 1, 4, self._handle_home_z, bg='#3e4451', fg=ThemeManager.ACCENT_CYAN)
        self._btn(btn_grid, 'Z-', 2, 4, lambda: self._do_jog(0.0, 0.0, -self._get_step(), 0.0))

        self._btn(btn_grid, 'Φ-', 1, 3, lambda: self._do_jog(0.0, 0.0, 0.0, -math.radians(10.0)))
        self._btn(btn_grid, 'Φ+', 1, 5, lambda: self._do_jog(0.0, 0.0, 0.0, math.radians(10.0)))

        ctrl_frame: tk.Frame = tk.Frame(self, bg=ThemeManager.BG_PANEL)
        ctrl_frame.pack(fill=tk.X, pady=(10, 0))

        btn_elbow: tk.Button = tk.Button(
            ctrl_frame,
            text='Toggle Lefty/Righty',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=tk.FLAT,
            command=self._handle_elbow
        )
        btn_elbow.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        btn_estop: tk.Button = tk.Button(
            ctrl_frame,
            text='E-STOP',
            bg=ThemeManager.ACCENT_RED,
            fg='#ffffff',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=tk.FLAT,
            command=self._handle_estop
        )
        btn_estop.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def _get_step(self) -> float:
        '''
            Returns current selected step distance in mm.

            :return: Step size in mm.
            :exceptions: None.
        '''
        return self._step_var.get()

    def _do_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Dispatches relative displacement jog command.

            :param dx: Delta X in mm.
            :param dy: Delta Y in mm.
            :param dz: Delta Z in mm.
            :param dphi: Delta Phi in radians.
            :exceptions: None.
        '''
        if self._on_jog is not None:
            self._on_jog(dx, dy, dz, dphi)

    def _handle_home_xy(self) -> None:
        '''
            Dispatches planar XY homing command.

            :exceptions: None.
        '''
        if self._on_home_xy is not None:
            self._on_home_xy()

    def _handle_home_z(self) -> None:
        '''
            Dispatches vertical Z homing command.

            :exceptions: None.
        '''
        if self._on_home_z is not None:
            self._on_home_z()

    def _handle_elbow(self) -> None:
        '''
            Dispatches elbow toggle command.

            :exceptions: None.
        '''
        if self._on_toggle_elbow is not None:
            self._on_toggle_elbow()

    def _handle_estop(self) -> None:
        '''
            Dispatches emergency stop command.

            :exceptions: None.
        '''
        if self._on_estop is not None:
            self._on_estop()

    def _btn(
        self,
        parent: tk.Frame,
        text: str,
        r: int,
        c: int,
        cmd: Callable[[], None],
        bg: str = '#45475a',
        fg: str = ThemeManager.TEXT_PRIMARY
    ) -> tk.Button:
        '''
            Helper creating styled jog button.

            :param parent: Parent frame container.
            :param text: Button label.
            :param r: Grid row.
            :param c: Grid column.
            :param cmd: Click handler function.
            :param bg: Optional background hex color.
            :param fg: Optional foreground hex color.
            :return: The button instance.
            :exceptions: None.
        '''
        b = tk.Button(
            parent,
            text=text,
            width=5,
            bg=bg,
            fg=fg,
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=tk.FLAT,
            command=cmd
        )
        b.grid(row=r, column=c, padx=2, pady=2)
        return b
