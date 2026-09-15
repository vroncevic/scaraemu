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

from tkinter import (
    Button,
    DoubleVar,
    FLAT,
    Frame,
    Label,
    LabelFrame,
    LEFT,
    Radiobutton,
    Widget,
    X,
)
from typing import Callable, Final

from scaraemu.infrastructure.gui.controls.jog_dpad import JogDpad
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanel(LabelFrame):
    '''
        Manual jog and movement direction controls with step resolution selector.

        It defines:

            :attributes:
                | _step_var - Active step size in mm.
                | _dpad - JogDpad direction button matrix.
                | _on_toggle_elbow - Callback for elbow solution toggling.
                | _on_toggle_motors - Callback for motor driver power toggling.
                | _on_toggle_hold - Callback for feed-hold pause toggling.
                | _on_estop - Callback for emergency stop.
            :methods:
                | __init__ - Initializes jog buttons and control elements.
                | _get_step - Reads active step size from DoubleVar.
                | _handle_elbow - Dispatches elbow toggle callback.
                | _handle_motors - Dispatches motor toggle callback.
                | _handle_hold - Dispatches feed-hold callback.
                | _handle_estop - Dispatches emergency stop callback.
    '''

    _step_var: DoubleVar
    _dpad: Final[JogDpad]
    _on_toggle_elbow: Callable[[], None] | None
    _on_toggle_motors: Callable[[], None] | None
    _on_toggle_hold: Callable[[], None] | None
    _on_estop: Callable[[], None] | None

    def __init__(
        self,
        parent: Widget,
        on_jog: Callable[[float, float, float, float], None] | None = None,
        on_home_xy: Callable[[], None] | None = None,
        on_home_z: Callable[[], None] | None = None,
        on_toggle_elbow: Callable[[], None] | None = None,
        on_toggle_motors: Callable[[], None] | None = None,
        on_toggle_hold: Callable[[], None] | None = None,
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
            :param on_toggle_hold: Callback for feed-hold pause/resume toggle.
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
        self._on_toggle_elbow = on_toggle_elbow
        self._on_toggle_motors = on_toggle_motors
        self._on_toggle_hold = on_toggle_hold
        self._on_estop = on_estop

        step_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        step_frame.pack(fill=X, pady=(0, 8))

        lbl_step: Label = Label(
            step_frame,
            text='Step:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9)
        )
        lbl_step.pack(side=LEFT, padx=(0, 5))

        self._step_var = DoubleVar(value=5.0)
        for s in (1.0, 5.0, 10.0, 25.0):
            rb: Radiobutton = Radiobutton(
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
            rb.pack(side=LEFT, padx=2)

        self._dpad = JogDpad(
            self,
            step_supplier=self._get_step,
            on_jog=on_jog,
            on_home_xy=on_home_xy,
            on_home_z=on_home_z
        )
        self._dpad.pack(fill=X, pady=4)

        ctrl_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        ctrl_frame.pack(fill=X, pady=(10, 0))

        btn_elbow: Button = Button(
            ctrl_frame,
            text='Toggle Lefty/Righty',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._handle_elbow
        )
        btn_elbow.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))

        btn_hold: Button = Button(
            ctrl_frame,
            text='HOLD',
            bg=ThemeManager.ACCENT_ORANGE,
            fg='#1e1e2e',
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=FLAT,
            command=self._handle_hold
        )
        btn_hold.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))

        btn_estop: Button = Button(
            ctrl_frame,
            text='E-STOP',
            bg=ThemeManager.ACCENT_RED,
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8, 'bold'),
            relief=FLAT,
            command=self._handle_estop
        )
        btn_estop.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))

        btn_motors: Button = Button(
            ctrl_frame,
            text='Toggle Motors',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._handle_motors
        )
        btn_motors.pack(side=LEFT, expand=True, fill=X)

    def _get_step(self) -> float:
        '''
            Returns the currently selected jog distance in mm.

            :return: Step size float.
            :exceptions: None.
        '''
        return float(self._step_var.get())

    def _handle_elbow(self) -> None:
        '''
            Dispatches elbow orientation toggle callback.

            :exceptions: None.
        '''
        if self._on_toggle_elbow is not None:
            self._on_toggle_elbow()

    def _handle_motors(self) -> None:
        '''
            Dispatches motor enable toggle callback.

            :exceptions: None.
        '''
        if self._on_toggle_motors is not None:
            self._on_toggle_motors()

    def _handle_hold(self) -> None:
        '''
            Dispatches feed-hold pause toggle callback.

            :exceptions: None.
        '''
        if self._on_toggle_hold is not None:
            self._on_toggle_hold()

    def _handle_estop(self) -> None:
        '''
            Dispatches emergency stop callback.

            :exceptions: None.
        '''
        if self._on_estop is not None:
            self._on_estop()
