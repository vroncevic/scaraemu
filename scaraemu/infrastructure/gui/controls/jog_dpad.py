# -*- coding: UTF-8 -*-

'''
Module
    jog_dpad.py
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

from math import radians
from tkinter import Button, FLAT, Frame, Widget
from typing import Callable

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
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
                | _step_supplier - Function returning the active step size in mm.
                | _on_jog - Callback receiving (dx, dy, dz, dphi).
                | _on_home_xy - Callback for homing planar axes.
                | _on_home_z - Callback for homing vertical axis.
            :methods:
                | __init__ - Initializes the D-pad button grid.
                | _do_jog - Triggers jog callback with current delta.
                | _btn - Helper to configure and place grid buttons.
    '''

    _step_supplier: Callable[[], float]
    _on_jog: Callable[[float, float, float, float], None] | None
    _on_home_xy: Callable[[], None] | None
    _on_home_z: Callable[[], None] | None

    def __init__(
        self,
        parent: Widget,
        step_supplier: Callable[[], float],
        on_jog: Callable[[float, float, float, float], None] | None = None,
        on_home_xy: Callable[[], None] | None = None,
        on_home_z: Callable[[], None] | None = None,
    ) -> None:
        '''
            Initializes the D-pad button grid.

            :param parent: Parent Tkinter widget.
            :param step_supplier: Callback returning active step distance.
            :param on_jog: Callback for incremental motion (dx, dy, dz, dphi).
            :param on_home_xy: Callback for homing XY planar axes.
            :param on_home_z: Callback for homing vertical Z axis.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._step_supplier = step_supplier
        self._on_jog = on_jog
        self._on_home_xy = on_home_xy
        self._on_home_z = on_home_z

        self._btn('Y+', 0, 1, lambda: self._do_jog(0.0, self._step_supplier(), 0.0, 0.0))
        self._btn('X-', 1, 0, lambda: self._do_jog(-self._step_supplier(), 0.0, 0.0, 0.0))
        self._btn('H_XY', 1, 1, self._handle_home_xy, bg='#3e4451', fg=ThemeManager.ACCENT_CYAN)
        self._btn('X+', 1, 2, lambda: self._do_jog(self._step_supplier(), 0.0, 0.0, 0.0))
        self._btn('Y-', 2, 1, lambda: self._do_jog(0.0, -self._step_supplier(), 0.0, 0.0))

        self._btn('Z+', 0, 4, lambda: self._do_jog(0.0, 0.0, self._step_supplier(), 0.0))
        self._btn('H_Z', 1, 4, self._handle_home_z, bg='#3e4451', fg=ThemeManager.ACCENT_CYAN)
        self._btn('Z-', 2, 4, lambda: self._do_jog(0.0, 0.0, -self._step_supplier(), 0.0))

        self._btn('Φ-', 1, 3, lambda: self._do_jog(0.0, 0.0, 0.0, -radians(10.0)))
        self._btn('Φ+', 1, 5, lambda: self._do_jog(0.0, 0.0, 0.0, radians(10.0)))

    def _do_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Executes jog displacement callback.

            :param dx: X delta in mm.
            :param dy: Y delta in mm.
            :param dz: Z delta in mm.
            :param dphi: Tool angle delta in radians.
            :exceptions: None.
        '''
        if self._on_jog is not None:
            self._on_jog(dx, dy, dz, dphi)

    def _handle_home_xy(self) -> None:
        '''
            Executes XY homing callback.

            :exceptions: None.
        '''
        if self._on_home_xy is not None:
            self._on_home_xy()

    def _handle_home_z(self) -> None:
        '''
            Executes Z homing callback.

            :exceptions: None.
        '''
        if self._on_home_z is not None:
            self._on_home_z()

    def _btn(
        self,
        text: str,
        r: int,
        c: int,
        cmd: Callable[[], None],
        bg: str = '#313244',
        fg: str = ThemeManager.TEXT_PRIMARY
    ) -> Button:
        '''
            Helper for creating styled jog button.

            :param text: Button label.
            :param r: Grid row index.
            :param c: Grid column index.
            :param cmd: Click handler.
            :param bg: Background color hex.
            :param fg: Foreground color hex.
            :return: The button widget.
            :exceptions: None.
        '''
        b: Button = Button(
            self,
            text=text,
            bg=bg,
            fg=fg,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            width=5,
            relief=FLAT,
            command=cmd
        )
        b.grid(row=r, column=c, padx=2, pady=2)
        return b
