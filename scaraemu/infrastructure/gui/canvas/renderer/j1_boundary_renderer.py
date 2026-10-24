# -*- coding: UTF-8 -*-

'''
Module
    j1_boundary_renderer.py
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
    Renders rear unreachable boundary crescent when J1 angle limit is less than PI.
'''

from __future__ import annotations

from math import degrees, pi
from tkinter import Canvas

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer
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


class J1BoundaryRenderer:
    '''
        Renders rear unreachable boundary crescent when J1 angle limit is less than PI.

        It defines:

            :methods:
                | is_j1_limited - Checks whether J1 angular range is bounded.
                | calculate_polygon_points - Calculates screen coordinate vertices for boundary crescent.
                | render - Draws rear boundary crescent polygon and limit label on Canvas.
                | get_version - Returns component version string.
    '''

    @classmethod
    def is_j1_limited(cls, bounds: ScaraBounds) -> bool:
        '''
            Checks whether J1 angular range is bounded below PI.

            :param bounds: Kinematic geometry and limits model.
            :return: True if J1 is bounded below PI, False otherwise.
            :exceptions: None.
        '''
        return bounds.joints.j1_max_rad < pi

    @classmethod
    def calculate_polygon_points(
        cls,
        bounds: ScaraBounds,
        transformer: ICoordinateTransformer,
        boundary_service: IWorkspaceBoundaryService,
    ) -> list[float]:
        '''
            Calculates screen coordinate polygon points for J1 limit crescent.

            :param bounds: Kinematic geometry and limits model.
            :param transformer: Coordinate projection transformer.
            :param boundary_service: Workspace boundary kinematics calculation service.
            :return: Flattened list of screen coordinate pairs [x0, y0, x1, y1, ...].
            :exceptions: None.
        '''
        pts = boundary_service.calculate_forbidden_zone_polygon(bounds)
        poly_pts: list[float] = []

        for pt in pts:
            sx, sy = transformer.world_to_screen(pt.x, pt.y)
            poly_pts.extend((sx, sy))

        return poly_pts

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        bounds: ScaraBounds,
        transformer: ICoordinateTransformer,
        reach_adapter: IWorkspaceReachAdapter,
        boundary_service: IWorkspaceBoundaryService,
    ) -> bool:
        '''
            Renders rear unreachable boundary crescent and label on canvas.

            :param canvas: Target Canvas widget.
            :param bounds: Kinematic geometry and limits model.
            :param transformer: Coordinate projection transformer.
            :param reach_adapter: Workspace reach metrics adapter.
            :param boundary_service: Workspace boundary kinematics calculation service.
            :return: True if boundary crescent was rendered, False if J1 is not limited.
            :exceptions: None.
        '''
        if not cls.is_j1_limited(bounds):
            return False

        poly_pts: list[float] = cls.calculate_polygon_points(
            bounds, transformer, boundary_service
        )
        canvas.create_polygon(
            *poly_pts,
            fill=ThemeManager.ACCENT_RED,
            stipple='gray25',
            outline=ThemeManager.ACCENT_RED,
            dash=(2, 2),
            width=1.5
        )

        j1_max: float = bounds.joints.j1_max_rad
        r_max: float = reach_adapter.get_safe_r_max()
        j1_max_deg: float = degrees(j1_max)
        lbl_x, lbl_y = transformer.world_to_screen(-r_max + 18.0, 0.0)
        canvas.create_text(
            lbl_x, lbl_y,
            text=f'J1 LIMIT\n(±{j1_max_deg:.0f}°)',
            fill=ThemeManager.ACCENT_RED,
            font=(ThemeManager.FONT_FAMILY, 7, 'bold'),
            justify='center'
        )

        return True

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
