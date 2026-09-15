# -*- coding: UTF-8 -*-

'''
Module
    robot_arm_renderer.py
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

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.core.model.kinematics.scara_joints import ScaraJoints
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


class RobotArmRenderer:
    '''
        Draws articulated links, rotary joint circles, and orientation arrow on canvas.

        It defines:

            :methods:
                | render - Draws links, joints, and tool arrow onto target canvas.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        geometry: ScaraGeometry,
        viewport: CanvasViewport,
        pose: ScaraPose,
        joints: ScaraJoints
    ) -> None:
        '''
            Renders robot links, joints, and end-effector arrow.

            :param canvas: Target Canvas widget.
            :param geometry: SCARA physical link parameters.
            :param viewport: Viewport coordinate mapper.
            :param pose: Current Cartesian tool pose.
            :param joints: Current joint angular positions.
            :exceptions: None.
        '''
        bx, by = viewport.world_to_screen(0.0, 0.0)
        q1: float = joints.theta1
        q2: float = joints.theta2
        l1: float = geometry.l1
        l2: float = geometry.l2

        elbow_x: float = l1 * cos(q1)
        elbow_y: float = l1 * sin(q1)
        ex, ey = viewport.world_to_screen(elbow_x, elbow_y)

        wrist_x: float = elbow_x + l2 * cos(q1 + q2)
        wrist_y: float = elbow_y + l2 * sin(q1 + q2)
        wx, wy = viewport.world_to_screen(wrist_x, wrist_y)

        canvas.create_line(bx, by, ex, ey, fill=ThemeManager.ACCENT_CYAN, width=6, capstyle=ROUND)
        canvas.create_line(ex, ey, wx, wy, fill=ThemeManager.ACCENT_BLUE, width=5, capstyle=ROUND)

        tool_len: float = 20.0
        tool_phi: float = pose.phi
        tx_end: float = wrist_x + tool_len * cos(tool_phi)
        ty_end: float = wrist_y + tool_len * sin(tool_phi)
        tex, tey = viewport.world_to_screen(tx_end, ty_end)
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
