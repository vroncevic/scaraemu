# -*- coding: UTF-8 -*-

'''
Module
    canvas_z.py
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
    Vertical Z-axis elevation and radial reach projection interactive canvas.
'''

from __future__ import annotations

import math
import tkinter as tk
from typing import Callable

from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.gui.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasZ(tk.Canvas, ICanvasZ):
    '''
        Side vertical Z-axis tower and radial elevation visualizer canvas.

        It defines:

            :attributes:
                | _geometry - Active ScaraGeometry model.
                | _width_px - Canvas pixel width.
                | _height_px - Canvas pixel height.
                | _on_target_click - Callback for interactive vertical height targeting.
            :methods:
                | __init__ - Initializes canvas and registers event handlers.
                | set_on_target_click - Registers target Z height click callback.
                | redraw - Renders tower, carriage, elevation, and radial arm projection.
    '''

    _geometry: ScaraGeometry
    _width_px: float
    _height_px: float
    _on_target_click: Callable[[float], None] | None

    def __init__(
        self,
        parent: tk.Widget,
        geometry: ScaraGeometry,
        width: int = 480,
        height: int = 240
    ) -> None:
        '''
            Initializes vertical Z canvas.

            :param parent: Parent Tkinter widget.
            :param geometry: SCARA physical link lengths.
            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=ThemeManager.BG_CANVAS,
            highlightthickness=1,
            highlightbackground=ThemeManager.BORDER_COLOR
        )
        self._geometry = geometry
        self._width_px = float(width)
        self._height_px = float(height)
        self._on_target_click = None

        self.bind('<Configure>', self._on_resize)
        self.bind('<Button-1>', self._handle_mouse)

    def set_on_target_click(self, callback: Callable[[float], None]) -> None:
        '''
            Registers click/drag callback for commanding Z coordinate.

            :param callback: Callback receiving target Z height in mm.
            :exceptions: None.
        '''
        self._on_target_click = callback

    def _on_resize(self, event: tk.Event) -> None:
        '''
            Updates canvas dimensions on widget resize.

            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        if event.width > 10 and event.height > 10:
            self._width_px = float(event.width)
            self._height_px = float(event.height)

    def _z_to_screen_y(self, z: float, bottom_y: float, top_y: float) -> float:
        '''
            Maps vertical Z in mm to canvas screen Y in pixels.

            :param z: Z elevation in mm.
            :param bottom_y: Bottom pixel coordinate (Z=0).
            :param top_y: Top pixel coordinate (Z=Zmax).
            :return: Screen Y coordinate.
            :exceptions: None.
        '''
        z_clamped: float = max(self._geometry.z_min, min(self._geometry.z_max, z))
        span_z: float = max(1.0, self._geometry.z_max - self._geometry.z_min)
        ratio: float = (z_clamped - self._geometry.z_min) / span_z
        return bottom_y - ratio * (bottom_y - top_y)

    def _screen_y_to_z(self, sy: float, bottom_y: float, top_y: float) -> float:
        '''
            Maps screen Y pixel coordinate back to vertical Z in mm.

            :param sy: Screen Y coordinate in pixels.
            :param bottom_y: Bottom pixel coordinate (Z=0).
            :param top_y: Top pixel coordinate (Z=Zmax).
            :return: Clamped Z elevation in mm.
            :exceptions: None.
        '''
        ratio: float = (bottom_y - sy) / max(1.0, bottom_y - top_y)
        z: float = self._geometry.z_min + ratio * (self._geometry.z_max - self._geometry.z_min)
        return max(self._geometry.z_min, min(self._geometry.z_max, z))

    def _handle_mouse(self, event: tk.Event) -> None:
        '''
            Translates mouse interaction to Z coordinate and triggers callback.

            :param event: Tkinter mouse event.
            :exceptions: None.
        '''
        if self._on_target_click is not None:
            bottom_y: float = self._height_px - 40.0
            top_y: float = 40.0
            z_target: float = self._screen_y_to_z(event.y, bottom_y, top_y)
            self._on_target_click(z_target)

    def redraw(self, pose: ScaraPose, current_target: ScaraPose | None = None) -> None:
        '''
            Renders tower, carriage, elevation, and radial arm projection.

            :param pose: Current Cartesian pose.
            :param current_target: Optional active target pose.
            :exceptions: None.
        '''
        self.delete('all')

        bottom_y: float = self._height_px - 40.0
        top_y: float = 40.0
        tower_x: float = 80.0

        self.create_line(tower_x - 15, bottom_y + 10, tower_x + 15, bottom_y + 10, fill=ThemeManager.BORDER_COLOR, width=4)
        self.create_line(tower_x - 8, top_y, tower_x - 8, bottom_y, fill='#45475a', width=3)
        self.create_line(tower_x + 8, top_y, tower_x + 8, bottom_y, fill='#45475a', width=3)
        self.create_line(tower_x, top_y, tower_x, bottom_y, fill=ThemeManager.ACCENT_CYAN, width=2, dash=(2, 2))

        curr_y: float = self._z_to_screen_y(pose.z, bottom_y, top_y)

        if current_target is not None:
            tgt_y: float = self._z_to_screen_y(current_target.z, bottom_y, top_y)
            self.create_line(tower_x - 25, tgt_y, self._width_px - 20, tgt_y, fill=ThemeManager.ACCENT_ORANGE, width=1, dash=(3, 3))

        c_w: float = 28.0
        c_h: float = 14.0
        self.create_rectangle(
            tower_x - c_w / 2, curr_y - c_h / 2,
            tower_x + c_w / 2, curr_y + c_h / 2,
            fill=ThemeManager.ACCENT_BLUE,
            outline=ThemeManager.TEXT_PRIMARY,
            width=2
        )

        r_current: float = math.hypot(pose.x, pose.y)
        max_reach: float = max(1.0, self._geometry.r_max)
        arm_px: float = (r_current / max_reach) * max(20.0, self._width_px - tower_x - 60.0)
        arm_end_x: float = tower_x + arm_px

        self.create_line(tower_x + c_w / 2, curr_y, arm_end_x, curr_y, fill=ThemeManager.ACCENT_CYAN, width=5, capstyle=tk.ROUND)
        self.create_line(arm_end_x, curr_y, arm_end_x, curr_y + 20, fill=ThemeManager.ACCENT_GREEN, width=3, arrow=tk.LAST)
        self.create_oval(arm_end_x - 4, curr_y - 4, arm_end_x + 4, curr_y + 4, fill=ThemeManager.ACCENT_YELLOW)

        self.create_text(
            10, 15,
            anchor='w',
            text=f'Z SIDE VIEW  |  Height: {pose.z:.1f} mm  |  Radius: {r_current:.1f} mm',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold')
        )
