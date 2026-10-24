# -*- coding: UTF-8 -*-

'''
Module
    canvas_z.py
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
    Vertical Z-axis elevation and radial reach projection interactive canvas.
'''

from __future__ import annotations

from tkinter import Canvas, Event, Widget
from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.renderer.z_render_context import ZRenderContext
from scaraemu.infrastructure.gui.canvas.viewport.z_coordinate_mapper import ZCoordinateMapper
from scaraemu.infrastructure.gui.canvas.renderer.z_renderer import ZRenderer
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasZ(Canvas):
    '''
        Side vertical Z-axis tower and radial elevation visualizer canvas.

        It defines:

            :attributes:
                | _bounds - Kinematic limits and workspace bounds.
                | _coordinate_mapper - Z coordinate to pixel translator.
                | _target_click_listener - Target height click listener.
                | _width_px - Canvas pixel width.
                | _height_px - Canvas pixel height.
            :methods:
                | __init__ - Initializes canvas and registers event handlers.
                | on_resize - Updates canvas dimensions on widget resize.
                | on_mouse_click - Translates mouse interaction to Z coordinate and triggers listener.
                | redraw - Renders tower, carriage, elevation, and radial arm projection.
                | clear - Clears all graphical elements from the canvas.
                | get_dimensions - Returns current canvas width and height in pixels.
    '''

    _bounds: ScaraBounds
    _coordinate_mapper: ZCoordinateMapper
    _target_click_listener: ITargetClickListener
    _width_px: float
    _height_px: float

    def __init__(
        self,
        parent: Widget,
        config: CanvasConfig,
    ) -> None:
        '''
            Initializes vertical Z canvas.

            :param parent: Parent Tkinter widget.
            :param config: Canvas configuration parameters bundle.
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
        self._coordinate_mapper: Final[ZCoordinateMapper] = ZCoordinateMapper(
            config.bounds.vertical
        )
        self._target_click_listener = config.target_click_listener
        self._width_px = float(config.width)
        self._height_px = float(config.height)

        self.bind('<Configure>', self.on_resize)
        self.bind('<Button-1>', self.on_mouse_click)

    def on_resize(self, event: Event) -> None:
        '''
            Updates canvas dimensions on widget resize.

            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        if event.width > 10 and event.height > 10:
            self._width_px = float(event.width)
            self._height_px = float(event.height)

    def on_mouse_click(self, event: Event) -> None:
        '''
            Translates mouse interaction to Z coordinate and triggers listener.

            :param event: Tkinter mouse event.
            :exceptions: None.
        '''
        bottom_y: float = self._height_px - 40.0
        top_y: float = 40.0
        z_target: float = self._coordinate_mapper.screen_y_to_z(
            float(event.y), bottom_y, top_y
        )
        self._target_click_listener.handle_z_click(z_target)

    def redraw(
        self, pose: ScaraPose, current_target: ScaraPose
    ) -> None:
        '''
            Renders tower, carriage, elevation, and radial arm projection.

            :param pose: Current Cartesian pose.
            :param current_target: Active target pose.
            :exceptions: None.
        '''
        self.delete('all')
        context = ZRenderContext(
            bounds=self._bounds,
            coordinate_mapper=self._coordinate_mapper,
            width_px=self._width_px,
            height_px=self._height_px,
        )
        ZRenderer.render(
            canvas=self,
            context=context,
            pose=pose,
            current_target=current_target,
        )

    def clear(self) -> None:
        '''
            Clears all graphical elements from the canvas.

            :exceptions: None.
        '''
        self.delete('all')

    def get_dimensions(self) -> tuple[float, float]:
        '''
            Returns current canvas width and height in pixels.

            :return: Tuple of width and height in pixels.
            :exceptions: None.
        '''
        return (self._width_px, self._height_px)
