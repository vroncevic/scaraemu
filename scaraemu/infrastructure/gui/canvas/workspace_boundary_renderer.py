# -*- coding: UTF-8 -*-

'''
Module
    workspace_boundary_renderer.py
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
    Renders Cartesian workspace reachability boundaries, dead zones, and joint limits.
'''

from __future__ import annotations

from math import asin, cos, degrees, pi, sin, sqrt
from tkinter import Canvas

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.infrastructure.gui.canvas.canvas_viewport import CanvasViewport
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceBoundaryRenderer:
    '''
        Renders background reach disc, inner dead zone, and angular limit polygons.

        It defines:

            :methods:
                | render - Draws complete boundary overlays and Cartesian coordinate axes.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        geometry: ScaraGeometry,
        viewport: CanvasViewport
    ) -> None:
        '''
            Renders background Cartesian grid and reach boundaries.

            :param canvas: Target Tkinter Canvas widget.
            :param geometry: Robot physical geometry model.
            :param viewport: Coordinate viewport translator.
            :exceptions: None.
        '''
        bx, by = viewport.world_to_screen(0.0, 0.0)
        width_px, height_px = viewport.get_dimensions()
        scale = viewport.get_scale()

        # 1. Shaded unreachable outer background
        canvas.create_rectangle(
            0, 0, width_px, height_px,
            fill=ThemeManager.ACCENT_RED,
            stipple='gray25',
            outline=''
        )

        # 2. Reachable annular disc cutout
        r_max_px: float = geometry.safe_r_max * scale
        canvas.create_oval(
            bx - r_max_px, by - r_max_px,
            bx + r_max_px, by + r_max_px,
            fill=ThemeManager.BG_CANVAS,
            outline=ThemeManager.ACCENT_CYAN,
            dash=(3, 3),
            width=1.5
        )

        # 3. Inner physical dead zone
        r_dead: float = cls.calculate_dead_zone_radius(geometry)
        r_dead_px: float = r_dead * scale
        canvas.create_oval(
            bx - r_dead_px, by - r_dead_px,
            bx + r_dead_px, by + r_dead_px,
            fill=ThemeManager.ACCENT_RED,
            stipple='gray25',
            outline=ThemeManager.ACCENT_RED,
            dash=(2, 2),
            width=1.5
        )
        canvas.create_text(
            bx, by - r_dead_px * 0.45,
            text=f'DEAD ZONE\n(R < {r_dead:.0f} mm)',
            fill=ThemeManager.ACCENT_RED,
            font=(ThemeManager.FONT_FAMILY, 7, 'bold'),
            justify='center'
        )

        # 4. Rear boundary crescent for Shoulder J1 limit
        cls._render_j1_limits(canvas, geometry, viewport)

        # 5. Cartesian axes
        canvas.create_line(0, by, width_px, by, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))
        canvas.create_line(bx, 0, bx, height_px, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))

    @classmethod
    def calculate_dead_zone_radius(cls, geometry: ScaraGeometry) -> float:
        '''
            Calculates inner physical dead zone radius based on joint 2 fold angle.

            :param geometry: SCARA physical link parameters.
            :return: Dead zone radius in mm.
            :exceptions: None.
        '''
        r_dead_sq: float = (
            geometry.l1 * geometry.l1
            + geometry.l2 * geometry.l2
            + 2.0 * geometry.l1 * geometry.l2 * cos(geometry.j2_max_rad)
        )
        return sqrt(max(0.0, r_dead_sq))

    @classmethod
    def _render_j1_limits(
        cls,
        canvas: Canvas,
        geometry: ScaraGeometry,
        viewport: CanvasViewport
    ) -> None:
        '''
            Renders rear unreachable boundary crescent when J1 angle limit is less than PI.

            :param canvas: Target Canvas widget.
            :param geometry: Robot physical geometry model.
            :param viewport: Coordinate viewport translator.
            :exceptions: None.
        '''
        j1_max: float = geometry.j1_max_rad
        if j1_max >= pi:
            return

        l1: float = geometry.l1
        l2: float = geometry.l2
        r_max: float = geometry.safe_r_max
        poly_pts: list[float] = []

        steps_arc: int = 24
        start_ang: float = j1_max
        end_ang: float = 2.0 * pi - j1_max
        for i in range(steps_arc + 1):
            ang: float = start_ang + (end_ang - start_ang) * (i / steps_arc)
            wx: float = r_max * cos(ang)
            wy: float = r_max * sin(ang)
            sx, sy = viewport.world_to_screen(wx, wy)
            poly_pts.extend((sx, sy))

        sin_target: float = min(1.0, (l1 * sin(j1_max)) / l2)
        theta2_cross: float = pi - asin(sin_target) - j1_max
        elbow_neg_x: float = l1 * cos(-j1_max)
        elbow_neg_y: float = l1 * sin(-j1_max)
        steps_curve: int = 16
        for i in range(steps_curve + 1):
            q2: float = theta2_cross * (i / steps_curve)
            arm2_ang: float = -j1_max - q2
            wx = elbow_neg_x + l2 * cos(arm2_ang)
            wy = elbow_neg_y + l2 * sin(arm2_ang)
            sx, sy = viewport.world_to_screen(wx, wy)
            poly_pts.extend((sx, sy))

        elbow_pos_x: float = l1 * cos(j1_max)
        elbow_pos_y: float = l1 * sin(j1_max)
        for i in range(steps_curve, -1, -1):
            q2 = theta2_cross * (i / steps_curve)
            arm2_ang = j1_max + q2
            wx = elbow_pos_x + l2 * cos(arm2_ang)
            wy = elbow_pos_y + l2 * sin(arm2_ang)
            sx, sy = viewport.world_to_screen(wx, wy)
            poly_pts.extend((sx, sy))

        canvas.create_polygon(
            *poly_pts,
            fill=ThemeManager.ACCENT_RED,
            stipple='gray25',
            outline=ThemeManager.ACCENT_RED,
            dash=(2, 2),
            width=1.5
        )
        j1_max_deg: float = degrees(j1_max)
        lbl_x, lbl_y = viewport.world_to_screen(-r_max + 18.0, 0.0)
        canvas.create_text(
            lbl_x, lbl_y,
            text=f'J1 LIMIT\n(±{j1_max_deg:.0f}°)',
            fill=ThemeManager.ACCENT_RED,
            font=(ThemeManager.FONT_FAMILY, 7, 'bold'),
            justify='center'
        )
