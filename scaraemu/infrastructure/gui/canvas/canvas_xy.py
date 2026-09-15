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

from collections.abc import Sequence
from tkinter import Canvas, Event, Widget
from typing import Callable, Final

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.core.model.kinematics.scara_joints import ScaraJoints
from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.canvas_viewport import CanvasViewport
from scaraemu.infrastructure.gui.canvas.robot_arm_renderer import RobotArmRenderer
from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.canvas.trail_renderer import TrailRenderer
from scaraemu.infrastructure.gui.canvas.workspace_boundary_renderer import (
    WorkspaceBoundaryRenderer,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasXY(Canvas):
    '''
        Top-down 2D XY planar SCARA kinematics visualizer canvas.

        It defines:

            :attributes:
                | _geometry - Active ScaraGeometry model.
                | _viewport - CanvasViewport coordinate and scaling manager.
                | _on_target_click - Callback for interactive coordinate targeting.
            :methods:
                | __init__ - Initializes canvas and registers coordinate mapping event handlers.
                | set_on_target_click - Registers target coordinate click callback.
                | redraw - Renders links, joints, path trail, and workspace boundaries.
                | flash_unreachable - Renders temporary unreachable indicator at coordinates.
    '''

    _geometry: Final[ScaraGeometry]
    _viewport: Final[CanvasViewport]
    _on_target_click: Callable[[float, float], None] | None

    def __init__(
        self,
        parent: Widget,
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
        self._viewport = CanvasViewport(geometry=geometry, width=width, height=height)
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

    def _on_resize(self, event: Event) -> None:
        '''
            Adjusts scale and center point on widget resize.

            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        self._viewport.update_size(event.width, event.height)

    def _handle_mouse(self, event: Event) -> None:
        '''
            Translates mouse interaction to world coordinates and triggers callback.

            :param event: Tkinter mouse event.
            :exceptions: None.
        '''
        if self._on_target_click is not None:
            wx, wy = self._viewport.screen_to_world(float(event.x), float(event.y))
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
        WorkspaceBoundaryRenderer.render(self, self._geometry, self._viewport)
        TrailRenderer.render(self, self._viewport, trail_points, current_target)
        RobotArmRenderer.render(self, self._geometry, self._viewport, pose, joints)

        r_dead: float = WorkspaceBoundaryRenderer.calculate_dead_zone_radius(self._geometry)
        self.create_text(
            10, 15,
            anchor='w',
            text=f'XY TOP VIEW  |  Reach: {r_dead:.0f} - {self._geometry.safe_r_max:.0f} mm',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold')
        )

    def flash_unreachable(self, x: float, y: float) -> None:
        '''
            Renders a temporary warning indicator at unreachable target coordinates.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :exceptions: None.
        '''
        sx, sy = self._viewport.world_to_screen(x, y)
        tag: str = f'unreachable_{id(self)}'
        self.create_oval(
            sx - 8, sy - 8, sx + 8, sy + 8,
            outline=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag
        )
        self.create_line(
            sx - 6, sy - 6, sx + 6, sy + 6,
            fill=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag
        )
        self.create_line(
            sx - 6, sy + 6, sx + 6, sy - 6,
            fill=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag
        )
        self.after(600, lambda: self.delete(tag))
