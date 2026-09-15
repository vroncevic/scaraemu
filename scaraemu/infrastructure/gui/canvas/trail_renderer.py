# -*- coding: UTF-8 -*-

'''
Module
    trail_renderer.py
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
    Renders motion trajectory historical path trails and active target indicators.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Canvas

from scaraemu.core.model.kinematics.scara_pose import ScaraPose
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


class TrailRenderer:
    '''
        Draws motion path trails and active Cartesian target crosshairs.

        It defines:

            :methods:
                | render - Draws motion trail line and target crosshair on canvas.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        viewport: CanvasViewport,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose | None = None
    ) -> None:
        '''
            Renders historical path trail and current target point.

            :param canvas: Target Canvas widget.
            :param viewport: Coordinate viewport translator.
            :param trail_points: Sequence of (x, y) coordinates.
            :param current_target: Optional active target pose.
            :exceptions: None.
        '''
        if len(trail_points) > 1:
            screen_trail: list[float] = []
            for tx, ty in trail_points:
                stx, sty = viewport.world_to_screen(tx, ty)
                screen_trail.extend([stx, sty])
            canvas.create_line(
                screen_trail,
                fill=ThemeManager.ACCENT_YELLOW,
                width=1.5,
                dash=(2, 2)
            )

        if current_target is not None:
            tx_s, ty_s = viewport.world_to_screen(current_target.x, current_target.y)
            canvas.create_oval(
                tx_s - 5, ty_s - 5, tx_s + 5, ty_s + 5,
                outline=ThemeManager.ACCENT_ORANGE,
                width=2
            )
            canvas.create_line(tx_s - 8, ty_s, tx_s + 8, ty_s, fill=ThemeManager.ACCENT_ORANGE, width=1.5)
            canvas.create_line(tx_s, ty_s - 8, tx_s, ty_s + 8, fill=ThemeManager.ACCENT_ORANGE, width=1.5)
