# -*- coding: UTF-8 -*-

'''
Module
    canvas_xy.py
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
    Top planar XY robot workspace interactive canvas implementation.
'''

from __future__ import annotations

import math
import tkinter as tk
from collections.abc import Sequence
from typing import Callable

from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.infrastructure.gui.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasXY(tk.Canvas, ICanvasXY):
    '''
        Top-down 2D XY planar SCARA kinematics visualizer canvas.

        It defines:

            :attributes:
                | _geometry - Active ScaraGeometry model.
                | _scale - Millimeters to canvas pixels scaling factor.
                | _center_x - Canvas origin center X pixel coordinate.
                | _center_y - Canvas origin center Y pixel coordinate.
                | _width_px - Canvas pixel width.
                | _height_px - Canvas pixel height.
                | _on_target_click - Callback for interactive coordinate targeting.
            :methods:
                | __init__ - Initializes canvas and registers coordinate mapping event handlers.
                | set_on_target_click - Registers target coordinate click callback.
                | redraw - Renders links, joints, path trail, and workspace boundaries.
    '''

    _geometry: ScaraGeometry
    _scale: float
    _center_x: float
    _center_y: float
    _width_px: float
    _height_px: float
    _on_target_click: Callable[[float, float], None] | None

    def __init__(
        self,
        parent: tk.Widget,
        geometry: ScaraGeometry,
        width: int = 480,
        height: int = 480
    ) -> None:
        '''
            Initializes canvas and registers coordinate mapping event handlers.

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
        self._scale = 0.72
        self._width_px = float(width)
        self._height_px = float(height)
        self._center_x = width / 2.0
        self._center_y = height / 2.0
        self._on_target_click = None

        self.bind('<Configure>', self._on_resize)
        self.bind('<Button-1>', self._handle_mouse)

    def set_on_target_click(self, callback: Callable[[float, float], None]) -> None:
        '''
            Registers click/drag callback for commanding XY coordinates.

            :param callback: Callback receiving (x, y) coordinates in mm.
            :exceptions: None.
        '''
        self._on_target_click = callback

    def _on_resize(self, event: tk.Event) -> None:
        '''
            Adjusts scale and center point on widget resize.

            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        if event.width > 10 and event.height > 10:
            self._width_px = float(event.width)
            self._height_px = float(event.height)
            self._center_x = self._width_px / 2.0
            self._center_y = self._height_px / 2.0
            min_dim: float = min(self._width_px, self._height_px)
            self._scale = (min_dim * 0.42) / max(1.0, self._geometry.r_max)

    def _world_to_screen(self, x: float, y: float) -> tuple[float, float]:
        '''
            Converts world millimeter coordinates to screen pixel coordinates.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :return: Tuple of (screen_x, screen_y) in pixels.
            :exceptions: None.
        '''
        sx: float = self._center_x + x * self._scale
        sy: float = self._center_y - y * self._scale
        return sx, sy

    def _screen_to_world(self, sx: float, sy: float) -> tuple[float, float]:
        '''
            Converts screen pixel coordinates back to world millimeter coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :return: Tuple of (world_x, world_y) in mm.
            :exceptions: None.
        '''
        x: float = (sx - self._center_x) / max(0.001, self._scale)
        y: float = (self._center_y - sy) / max(0.001, self._scale)
        return x, y

    def _handle_mouse(self, event: tk.Event) -> None:
        '''
            Translates mouse interaction to world coordinates and triggers callback.

            :param event: Tkinter mouse event.
            :exceptions: None.
        '''
        if self._on_target_click is not None:
            wx, wy = self._screen_to_world(event.x, event.y)
            self._on_target_click(wx, wy)

    def redraw(
        self,
        pose: ScaraPose,
        joints: ScaraJoints,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose | None = None
    ) -> None:
        '''
            Renders robot links, reach boundaries, and path trail.

            :param pose: Current Cartesian pose.
            :param joints: Current articulated joint angles.
            :param trail_points: Sequence of historical trail points.
            :param current_target: Optional active target pose.
            :exceptions: None.
        '''
        self.delete('all')
        self._draw_grid_and_bounds()

        if len(trail_points) > 1:
            screen_trail: list[float] = []
            for tx, ty in trail_points:
                stx, sty = self._world_to_screen(tx, ty)
                screen_trail.extend([stx, sty])
            self.create_line(
                screen_trail,
                fill=ThemeManager.ACCENT_YELLOW,
                width=1.5,
                dash=(2, 2)
            )

        if current_target is not None:
            tx_s, ty_s = self._world_to_screen(current_target.x, current_target.y)
            self.create_oval(
                tx_s - 5, ty_s - 5, tx_s + 5, ty_s + 5,
                outline=ThemeManager.ACCENT_ORANGE,
                width=2
            )
            self.create_line(tx_s - 8, ty_s, tx_s + 8, ty_s, fill=ThemeManager.ACCENT_ORANGE, width=1.5)
            self.create_line(tx_s, ty_s - 8, tx_s, ty_s + 8, fill=ThemeManager.ACCENT_ORANGE, width=1.5)

        bx, by = self._world_to_screen(0.0, 0.0)

        q1: float = joints.theta1
        q2: float = joints.theta2
        l1: float = self._geometry.l1
        l2: float = self._geometry.l2

        elbow_x: float = l1 * math.cos(q1)
        elbow_y: float = l1 * math.sin(q1)
        ex, ey = self._world_to_screen(elbow_x, elbow_y)

        wrist_x: float = elbow_x + l2 * math.cos(q1 + q2)
        wrist_y: float = elbow_y + l2 * math.sin(q1 + q2)
        wx, wy = self._world_to_screen(wrist_x, wrist_y)

        self.create_line(bx, by, ex, ey, fill=ThemeManager.ACCENT_CYAN, width=6, capstyle=tk.ROUND)
        self.create_line(ex, ey, wx, wy, fill=ThemeManager.ACCENT_BLUE, width=5, capstyle=tk.ROUND)

        tool_len: float = 20.0
        tool_phi: float = pose.phi
        tx_end: float = wrist_x + tool_len * math.cos(tool_phi)
        ty_end: float = wrist_y + tool_len * math.sin(tool_phi)
        tex, tey = self._world_to_screen(tx_end, ty_end)
        self.create_line(wx, wy, tex, tey, fill=ThemeManager.ACCENT_GREEN, width=3, arrow=tk.LAST)

        self.create_oval(bx - 8, by - 8, bx + 8, by + 8, fill='#45475a', outline=ThemeManager.TEXT_PRIMARY, width=2)
        self.create_oval(ex - 6, ey - 6, ex + 6, ey + 6, fill=ThemeManager.ACCENT_CYAN, outline=ThemeManager.TEXT_PRIMARY, width=2)
        self.create_oval(wx - 5, wy - 5, wx + 5, wy + 5, fill=ThemeManager.ACCENT_BLUE, outline=ThemeManager.TEXT_PRIMARY, width=2)

        self.create_text(
            10, 15,
            anchor='w',
            text=f'XY TOP VIEW  |  Reach: {self._geometry.r_min:.0f} - {self._geometry.r_max:.0f} mm',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold')
        )

    def _draw_grid_and_bounds(self) -> None:
        '''
            Renders background Cartesian grid and annular reach boundaries.

            :exceptions: None.
        '''
        bx, by = self._world_to_screen(0.0, 0.0)

        self.create_line(0, by, self._width_px, by, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))
        self.create_line(bx, 0, bx, self._height_px, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))

        r_max_px: float = self._geometry.r_max * self._scale
        self.create_oval(
            bx - r_max_px, by - r_max_px,
            bx + r_max_px, by + r_max_px,
            outline=ThemeManager.ACCENT_CYAN,
            dash=(3, 3),
            width=1.5
        )

        r_min_px: float = self._geometry.r_min * self._scale
        if r_min_px > 1.0:
            self.create_oval(
                bx - r_min_px, by - r_min_px,
                bx + r_min_px, by + r_min_px,
                outline=ThemeManager.ACCENT_RED,
                dash=(2, 2),
                width=1.5
            )
