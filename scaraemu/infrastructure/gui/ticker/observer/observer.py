# -*- coding: UTF-8 -*-

'''
Module
    observer.py
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
    Dispatches simulation state and telemetry updates to GUI visualizer views.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SimulationViewObserver:
    '''
        Aggregates and updates all graphical visualizer and telemetry views on simulation ticks.

        It defines:

            :attributes:
                | _canvas_xy - Top-down planar canvas view port.
                | _canvas_z - Side elevation canvas view port.
                | _telemetry_view - Numerical telemetry monitor view port.
                | _queue_view - Queue depth observer view port.
            :methods:
                | __init__ - Initializes observer with individual GUI presentation views.
                | update_views - Refreshes all visualizer and telemetry views with current state.
                | get_version - Returns observer component version string.
    '''

    _canvas_xy: ICanvasXY
    _canvas_z: ICanvasZ
    _telemetry_view: ITelemetryView
    _queue_view: IQueueDepthView

    def __init__(
        self,
        *,
        canvas_xy: ICanvasXY,
        canvas_z: ICanvasZ,
        telemetry_view: ITelemetryView,
        queue_view: IQueueDepthView,
    ) -> None:
        '''
            Initializes observer with individual GUI presentation views.

            :param canvas_xy: Top-down planar canvas view port.
            :param canvas_z: Side elevation canvas view port.
            :param telemetry_view: Numerical telemetry monitor view port.
            :param queue_view: Queue depth observer view port.
            :exceptions: None.
        '''
        self._canvas_xy: Final[ICanvasXY] = canvas_xy
        self._canvas_z: Final[ICanvasZ] = canvas_z
        self._telemetry_view: Final[ITelemetryView] = telemetry_view
        self._queue_view: Final[IQueueDepthView] = queue_view

    def update_views(
        self,
        telemetry: Telemetry,
        simulation_state: SimulationState,
    ) -> None:
        '''
            Refreshes all visualizer and telemetry views with current state.

            :param telemetry: Current manipulator telemetry snapshot.
            :param simulation_state: Current simulation stepper state snapshot.
            :exceptions: None.
        '''
        self._canvas_xy.redraw(
            pose=telemetry.pose,
            joints=telemetry.joints,
            trail_points=simulation_state.trail_points,
            current_target=simulation_state.current_target,
            planned_path=simulation_state.planned_path,
        )
        self._canvas_z.redraw(
            pose=telemetry.pose,
            current_target=simulation_state.current_target,
        )
        self._telemetry_view.update_telemetry(telemetry)
        self._queue_view.update_queue_depth(simulation_state.queue_depth)

    def get_version(self) -> str:
        '''
            Returns observer component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
