# -*- coding: UTF-8 -*-

'''
Module
    z_renderer.py
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
    Renders vertical Z tower, carriage, elevation, and radial arm projection.
'''

from __future__ import annotations

from math import hypot
from tkinter import Canvas, LAST, ROUND

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.renderer.z_render_context import ZRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZRenderer:
    '''
        Renders Z elevation tower, carriage rectangle, and radial reach projection on canvas.

        It defines:

            :methods:
                | render - Draws tower rails, carriage, radial projection, and text banner.
                | get_version - Returns renderer version string.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        context: ZRenderContext,
        pose: ScaraPose,
        current_target: ScaraPose,
    ) -> None:
        '''
            Renders tower, carriage, elevation, and radial arm projection onto target canvas.

            :param canvas: Target Canvas widget.
            :param context: Z-axis canvas rendering context.
            :param pose: Current Cartesian pose.
            :param current_target: Active target destination pose.
            :exceptions: None.
        '''
        bounds: ScaraBounds = context.bounds
        coordinate_mapper: ZCoordinateMapper = context.coordinate_mapper
        width_px: float = context.width_px
        height_px: float = context.height_px
        bottom_y: float = height_px - 40.0
        top_y: float = 40.0
        tower_x: float = 80.0

        canvas.create_line(
            tower_x - 15,
            bottom_y + 10,
            tower_x + 15,
            bottom_y + 10,
            fill=ThemeManager.BORDER_COLOR,
            width=4,
        )
        canvas.create_line(
            tower_x - 8,
            top_y,
            tower_x - 8,
            bottom_y,
            fill='#45475a',
            width=3,
        )
        canvas.create_line(
            tower_x + 8,
            top_y,
            tower_x + 8,
            bottom_y,
            fill='#45475a',
            width=3,
        )
        canvas.create_line(
            tower_x,
            top_y,
            tower_x,
            bottom_y,
            fill=ThemeManager.ACCENT_CYAN,
            width=2,
            dash=(2, 2),
        )

        curr_y: float = coordinate_mapper.z_to_screen_y(pose.z, bottom_y, top_y)

        if current_target is not None:
            tgt_y: float = coordinate_mapper.z_to_screen_y(
                current_target.z, bottom_y, top_y
            )
            canvas.create_line(
                tower_x - 25,
                tgt_y,
                width_px - 20,
                tgt_y,
                fill=ThemeManager.ACCENT_ORANGE,
                width=1,
                dash=(3, 3),
            )

        c_w: float = 28.0
        c_h: float = 14.0
        canvas.create_rectangle(
            tower_x - c_w / 2,
            curr_y - c_h / 2,
            tower_x + c_w / 2,
            curr_y + c_h / 2,
            fill=ThemeManager.ACCENT_BLUE,
            outline=ThemeManager.TEXT_PRIMARY,
            width=2,
        )

        r_current: float = hypot(pose.x, pose.y)
        max_reach: float = max(1.0, bounds.links.l1 + bounds.links.l2)
        arm_px: float = (r_current / max_reach) * max(20.0, width_px - tower_x - 60.0)
        arm_end_x: float = tower_x + arm_px

        canvas.create_line(
            tower_x + c_w / 2,
            curr_y,
            arm_end_x,
            curr_y,
            fill=ThemeManager.ACCENT_CYAN,
            width=5,
            capstyle=ROUND,
        )
        canvas.create_line(
            arm_end_x,
            curr_y,
            arm_end_x,
            curr_y + 20,
            fill=ThemeManager.ACCENT_GREEN,
            width=3,
            arrow=LAST,
        )
        canvas.create_oval(
            arm_end_x - 4,
            curr_y - 4,
            arm_end_x + 4,
            curr_y + 4,
            fill=ThemeManager.ACCENT_YELLOW,
        )

        canvas.create_text(
            10,
            15,
            anchor='w',
            text=f'Z SIDE VIEW  |  Height: {pose.z:.1f} mm  |  Radius: {r_current:.1f} mm',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
