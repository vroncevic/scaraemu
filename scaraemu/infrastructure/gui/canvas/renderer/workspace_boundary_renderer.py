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

from tkinter import Canvas

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.gui.canvas.viewport.viewport import Viewport
from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
from scaraemu.infrastructure.gui.canvas.renderer.j1_boundary_renderer import J1BoundaryRenderer
from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

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
                | get_version - Returns renderer version string.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        bounds: ScaraBounds,
        viewport: Viewport,
        transformer: ICoordinateTransformer,
        reach_adapter: IWorkspaceReachAdapter,
        boundary_service: IWorkspaceBoundaryService,
    ) -> None:
        '''
            Renders background Cartesian grid and reach boundaries.

            :param canvas: Target Tkinter Canvas widget.
            :param bounds: Kinematic geometry and operational limits model.
            :param viewport: Coordinate viewport translator providing dimensions and scale.
            :param transformer: Coordinate projection transformer.
            :param reach_adapter: Workspace reach metrics adapter.
            :param boundary_service: Workspace boundary kinematics calculation service.
            :exceptions: None.
        '''
        bx, by = transformer.world_to_screen(0.0, 0.0)
        width_px, height_px = viewport.get_dimensions()
        scale = viewport.get_scale()

        canvas.create_rectangle(
            0, 0, width_px, height_px,
            fill=ThemeManager.ACCENT_RED,
            stipple='gray25',
            outline=''
        )

        safe_r_max: float = reach_adapter.get_safe_r_max()
        r_max_px: float = safe_r_max * scale
        canvas.create_oval(
            bx - r_max_px, by - r_max_px,
            bx + r_max_px, by + r_max_px,
            fill=ThemeManager.BG_CANVAS,
            outline=ThemeManager.ACCENT_CYAN,
            dash=(3, 3),
            width=1.5
        )

        r_dead: float = reach_adapter.get_safe_r_min()
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

        J1BoundaryRenderer.render(
            canvas, bounds, transformer, reach_adapter, boundary_service
        )

        canvas.create_line(0, by, width_px, by, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))
        canvas.create_line(bx, 0, bx, height_px, fill=ThemeManager.BORDER_COLOR, dash=(1, 3))

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
