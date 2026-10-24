# -*- coding: UTF-8 -*-

'''
Module
    manipulator_arm_renderer.py
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
    Renders articulated SCARA kinematic links, joint bearings, and end-effector.
'''

from __future__ import annotations

from math import cos, sin
from tkinter import Canvas, LAST, ROUND

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.renderer.manipulator_render_context import ManipulatorRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorArmRenderer:
    '''
        Draws articulated links, rotary joint circles, and orientation arrow on canvas.

        It defines:

            :methods:
                | render - Draws links, joints, and tool arrow onto target canvas.
                | get_version - Returns renderer version string.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        context: ManipulatorRenderContext,
        pose: ScaraPose,
        joints: ScaraJoints,
    ) -> None:
        '''
            Renders manipulator links, joints, and end-effector arrow.

            :param canvas: Target Canvas widget.
            :param context: Manipulator arm rendering context.
            :param pose: Current Cartesian tool pose.
            :param joints: Current joint angular positions.
            :exceptions: None.
        '''
        transformer: ICoordinateTransformer = context.transformer
        bx, by = transformer.world_to_screen(0.0, 0.0)
        elbow, wrist = context.manipulator_linkage_adapter.solve_fk_pose(
            joints.theta1, joints.theta2
        )
        ex, ey = transformer.world_to_screen(elbow.x, elbow.y)
        wx, wy = transformer.world_to_screen(wrist.x, wrist.y)

        canvas.create_line(bx, by, ex, ey, fill=ThemeManager.ACCENT_CYAN, width=6, capstyle=ROUND)
        canvas.create_line(ex, ey, wx, wy, fill=ThemeManager.ACCENT_BLUE, width=5, capstyle=ROUND)

        tool_len: float = 20.0
        tool_phi: float = pose.phi
        tx_end: float = wrist.x + tool_len * cos(tool_phi)
        ty_end: float = wrist.y + tool_len * sin(tool_phi)
        tex, tey = transformer.world_to_screen(tx_end, ty_end)
        canvas.create_line(wx, wy, tex, tey, fill=ThemeManager.ACCENT_GREEN, width=3, arrow=LAST)

        canvas.create_oval(
            bx - 8, by - 8, bx + 8, by + 8,
            fill='#45475a', outline=ThemeManager.TEXT_PRIMARY, width=2
        )
        canvas.create_oval(
            ex - 6, ey - 6, ex + 6, ey + 6,
            fill=ThemeManager.ACCENT_CYAN, outline=ThemeManager.TEXT_PRIMARY, width=2
        )
        canvas.create_oval(
            wx - 5, wy - 5, wx + 5, wy + 5,
            fill=ThemeManager.ACCENT_BLUE, outline=ThemeManager.TEXT_PRIMARY, width=2
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
