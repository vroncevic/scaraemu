# -*- coding: UTF-8 -*-

'''
Module
    ibuilder.py
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
    Structural interface protocol for GUI widget layout builders.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ILayoutBuilder(Protocol):
    '''
        Structural interface protocol for GUI widget layout builders.

        It defines:

            :attributes:
                | canvas_xy - Planar top-down view canvas view port.
                | canvas_z - Elevation side view canvas view port.
                | telemetry_view - Telemetry values readout monitor view port.
                | queue_view - Trajectory queue depth observer view port.
            :methods:
                | build_layout - Builds and packs the complete GUI layout hierarchy.
                | set_connected_state - Updates hardware connection state in layout toolbar.
                | set_server_state - Updates virtual robot server state in layout toolbar.
                | append_log - Appends diagnostic log entry to layout console panel.
                | get_version - Returns builder component version string.
    '''

    canvas_xy: ICanvasXY
    canvas_z: ICanvasZ
    telemetry_view: ITelemetryView
    queue_view: IQueueDepthView

    def build_layout(
        self,
        *,
        root: Tk,
        bounds: ScaraBounds,
        target_click_listener: ITargetClickListener,
        delegates: GuiDelegatesBundle,
    ) -> None:
        '''
            Builds and packs the complete GUI layout hierarchy.

            :param root: Tkinter root window.
            :param bounds: SCARA kinematic bounds and limits.
            :param target_click_listener: Listener for interactive canvas target clicks.
            :param delegates: Bundled user action and event delegates.
        '''

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates hardware connection state in layout toolbar.

            :param connected: True if connected to hardware, False otherwise.
        '''

    def set_server_state(self, running: bool, port: int = 8888) -> None:
        '''
            Updates virtual robot server state in layout toolbar.

            :param running: True if server active, False otherwise.
            :param port: Listening TCP port number.
        '''

    def append_log(self, message: str, tag: str) -> None:
        '''
            Appends diagnostic log entry to layout console panel.

            :param message: Diagnostic log text line.
            :param tag: Log entry category tag.
        '''

    def get_version(self) -> str:
        '''
            Returns builder component version string.

            :return: Semantic version string.
        '''
