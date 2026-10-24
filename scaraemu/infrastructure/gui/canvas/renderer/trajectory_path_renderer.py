# -*- coding: UTF-8 -*-

'''
Module
    trajectory_path_renderer.py
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
    Renders planned trajectory polyline paths and waypoint node markers.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Canvas

from scaraemu.infrastructure.gui.canvas.viewport.icoordinate_transformer import ICoordinateTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPathRenderer:
    '''
        Draws planned trajectory path polylines and waypoint node markers on canvas.

        It defines:

            :methods:
                | render - Draws trajectory polyline lines and waypoint circular markers.
                | get_version - Returns renderer version string.
    '''

    @classmethod
    def render(
        cls,
        canvas: Canvas,
        transformer: ICoordinateTransformer,
        planned_path: Sequence[tuple[float, float]],
    ) -> None:
        '''
            Renders planned trajectory paths and waypoint node markers.

            :param canvas: Target Tkinter canvas widget.
            :param transformer: Coordinate projection transformer.
            :param planned_path: Sequence of Cartesian (x, y) coordinates.
            :exceptions: None.
        '''
        if not planned_path:
            return

        screen_coords: list[tuple[float, float]] = [
            transformer.world_to_screen(px, py) for px, py in planned_path
        ]

        if len(screen_coords) > 1:
            flattened: list[float] = [c for pt in screen_coords for c in pt]
            canvas.create_line(
                flattened,
                fill='#98c379',
                width=2,
            )

        show_labels: bool = len(screen_coords) <= 32

        for i, (sx, sy) in enumerate(screen_coords):
            canvas.create_oval(
                sx - 3,
                sy - 3,
                sx + 3,
                sy + 3,
                fill='#98c379',
                outline='#282c34',
                width=1,
            )

            if show_labels:
                canvas.create_text(
                    sx + 5,
                    sy - 5,
                    text=f'P{i + 1}',
                    fill='#abb2bf',
                    font=('TkDefaultFont', 7),
                    anchor='sw',
                )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
