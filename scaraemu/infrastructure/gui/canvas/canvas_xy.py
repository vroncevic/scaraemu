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
from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.viewport.coordinate_transformer import CoordinateTransformer
from scaraemu.infrastructure.gui.canvas.viewport.viewport import Viewport
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.gui.canvas.renderer.manipulator_render_context import ManipulatorRenderContext
from scaraemu.infrastructure.gui.canvas.renderer.manipulator_arm_renderer import ManipulatorArmRenderer
from scaraemu.infrastructure.gui.canvas.renderer.trajectory_path_renderer import TrajectoryPathRenderer
from scaraemu.infrastructure.gui.canvas.renderer.trail_renderer import TrailRenderer
from scaraemu.infrastructure.gui.canvas.renderer.workspace_boundary_renderer import WorkspaceBoundaryRenderer
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

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
                | _bounds - Kinematic limits and workspace bounds.
                | _viewport - Viewport metrics and scale provider.
                | _transformer - Coordinate transformation projector.
                | _target_click_listener - Listener for interactive coordinate targeting.
            :methods:
                | __init__ - Initializes canvas and registers coordinate mapping event handlers.
                | on_resize - Adjusts scale and center point on widget resize.
                | on_mouse_click - Translates mouse interaction to world coordinates and triggers listener.
                | redraw - Renders links, joints, path trail, and workspace boundaries.
                | flash_unreachable - Renders temporary unreachable indicator at coordinates.
                | get_dimensions - Returns current canvas width and height in pixels.
    '''

    _bounds: ScaraBounds
    _viewport: Viewport
    _transformer: ICoordinateTransformer
    _target_click_listener: ITargetClickListener
    _manipulator_linkage_adapter: ILinkageAdapter
    _reach_adapter: IWorkspaceReachAdapter
    _boundary_service: IWorkspaceBoundaryService

    def __init__(
        self,
        parent: Widget,
        *,
        config: CanvasConfig,
        manipulator_linkage_adapter: ILinkageAdapter,
        reach_adapter: IWorkspaceReachAdapter,
        boundary_service: IWorkspaceBoundaryService,
    ) -> None:
        '''
            Initializes canvas and registers coordinate mapping event handlers.

            :param parent: Parent Tkinter widget.
            :param config: Canvas configuration parameters bundle.
            :param manipulator_linkage_adapter: Injected ILinkageAdapter instance.
            :param reach_adapter: Injected IWorkspaceReachAdapter instance.
            :param boundary_service: Injected IWorkspaceBoundaryService instance.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            width=config.width,
            height=config.height,
            bg=ThemeManager.BG_CANVAS,
            highlightthickness=1,
            highlightbackground=ThemeManager.BORDER_COLOR,
        )
        self._bounds: Final[ScaraBounds] = config.bounds
        self._viewport: Final[Viewport] = Viewport(
            dimensions=config.bounds.links, width=config.width, height=config.height
        )
        self._transformer: Final[ICoordinateTransformer] = CoordinateTransformer(
            self._viewport
        )
        self._target_click_listener: Final[ITargetClickListener] = (
            config.target_click_listener
        )
        self._manipulator_linkage_adapter: Final[ILinkageAdapter] = (
            manipulator_linkage_adapter
        )
        self._reach_adapter: Final[IWorkspaceReachAdapter] = reach_adapter
        self._boundary_service: Final[IWorkspaceBoundaryService] = boundary_service

        self.bind('<Configure>', self.on_resize)
        self.bind('<Button-1>', self.on_mouse_click)

    def on_resize(self, event: Event) -> None:
        '''
            Adjusts scale and center point on widget resize.

            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        self._viewport.update_size(event.width, event.height)

    def on_mouse_click(self, event: Event) -> None:
        '''
            Translates mouse interaction to world coordinates and triggers listener.

            :param event: Tkinter mouse event.
            :exceptions: None.
        '''
        wx, wy = self._transformer.screen_to_world(float(event.x), float(event.y))

        if not self._target_click_listener.handle_xy_click(wx, wy):
            self.flash_unreachable(wx, wy)

    def redraw(
        self,
        pose: ScaraPose,
        joints: ScaraJoints,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose,
        planned_path: Sequence[tuple[float, float]] = (),
    ) -> None:
        '''
            Renders robot links, reach boundaries, and path trail.

            :param pose: Current Cartesian pose.
            :param joints: Current articulated joint angles.
            :param trail_points: Sequence of historical trail points.
            :param current_target: Active target pose.
            :param planned_path: Sequence of planned trajectory (x, y) coordinates.
            :exceptions: None.
        '''
        self.delete('all')
        WorkspaceBoundaryRenderer.render(
            self,
            self._bounds,
            self._viewport,
            self._transformer,
            self._reach_adapter,
            self._boundary_service,
        )
        TrajectoryPathRenderer.render(
            self, self._transformer, planned_path
        )
        TrailRenderer.render(
            self, self._transformer, trail_points, current_target
        )
        context = ManipulatorRenderContext(
            transformer=self._transformer,
            manipulator_linkage_adapter=self._manipulator_linkage_adapter,
        )
        ManipulatorArmRenderer.render(
            self, context, pose, joints
        )

        r_dead: float = self._reach_adapter.get_safe_r_min()
        safe_r_max: float = self._reach_adapter.get_safe_r_max()
        self.create_text(
            10,
            15,
            anchor='w',
            text=f'XY TOP VIEW  |  Reach: {r_dead:.0f} - {safe_r_max:.0f} mm',
            fill=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
        )

    def flash_unreachable(self, x: float, y: float) -> None:
        '''
            Renders a temporary warning indicator at unreachable target coordinates.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :exceptions: None.
        '''
        sx, sy = self._transformer.world_to_screen(x, y)
        tag: str = f'unreachable_{id(self)}'
        self.create_oval(
            sx - 8,
            sy - 8,
            sx + 8,
            sy + 8,
            outline=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag,
        )
        self.create_line(
            sx - 6,
            sy - 6,
            sx + 6,
            sy + 6,
            fill=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag,
        )
        self.create_line(
            sx - 6,
            sy + 6,
            sx + 6,
            sy - 6,
            fill=ThemeManager.ACCENT_RED,
            width=2,
            tags=tag,
        )
        self.after(600, lambda: self.delete(tag))

    def get_dimensions(self) -> tuple[float, float]:
        '''
            Returns current canvas width and height in pixels.

            :return: Tuple of width and height in pixels.
            :exceptions: None.
        '''
        return self._viewport.get_dimensions()
