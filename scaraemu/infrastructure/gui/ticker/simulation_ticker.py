# -*- coding: UTF-8 -*-

'''
Module
    simulation_ticker.py
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
    Periodic simulation and visualizer update ticker loop for GUI.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Any

from scaraemu.infrastructure.gui.canvas.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.controls.telemetry_panel import TelemetryPanel
from scaraemu.infrastructure.gui.trajectory.trajectory_demo_panel import TrajectoryDemoPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SimulationTicker:
    '''
        Drives the periodic simulation step and visualizer widget redraw loop.

        It defines:

            :attributes:
                | _service - Service facade providing emulator and kinematics.
                | _canvas_xy - Top-down planar canvas.
                | _canvas_z - Side elevation canvas.
                | _telemetry_panel - Telemetry readout monitor.
                | _demo_panel - Autonomous trajectory demo panel.
                | _interval_ms - Periodic timer tick interval in milliseconds.
                | _root - Root Tkinter window reference.
                | _running - Active ticking state flag.
            :methods:
                | __init__ - Initializes ticker with dependent widgets and services.
                | start - Starts periodic ticking loop using Tk after().
                | stop - Stops periodic ticking loop.
                | tick - Executes a single simulation step and redraws UI components.
                | _schedule_next - Schedules next periodic callback.
    '''

    _service: Any
    _canvas_xy: CanvasXY | None
    _canvas_z: CanvasZ | None
    _telemetry_panel: TelemetryPanel | None
    _demo_panel: TrajectoryDemoPanel | None
    _interval_ms: int
    _root: Tk | None
    _running: bool

    def __init__(
        self,
        service: Any,
        canvas_xy: CanvasXY | None = None,
        canvas_z: CanvasZ | None = None,
        telemetry_panel: TelemetryPanel | None = None,
        demo_panel: TrajectoryDemoPanel | None = None,
        interval_ms: int = 25
    ) -> None:
        '''
            Initializes ticker with dependent widgets and services.

            :param service: Service facade providing emulator and kinematics.
            :param canvas_xy: Top-down planar canvas.
            :param canvas_z: Side elevation canvas.
            :param telemetry_panel: Telemetry readout monitor.
            :param demo_panel: Autonomous trajectory demo panel.
            :param interval_ms: Periodic timer tick interval in milliseconds.
            :exceptions: None.
        '''
        self._service = service
        self._canvas_xy = canvas_xy
        self._canvas_z = canvas_z
        self._telemetry_panel = telemetry_panel
        self._demo_panel = demo_panel
        self._interval_ms = interval_ms
        self._root = None
        self._running = False

    def start(self, root: Tk) -> None:
        '''
            Starts periodic ticking loop using Tk after().

            :param root: Root Tkinter window instance.
            :exceptions: None.
        '''
        self._root = root
        self._running = True
        self._schedule_next()

    def stop(self) -> None:
        '''
            Stops periodic ticking loop.

            :exceptions: None.
        '''
        self._running = False

    def tick(self) -> None:
        '''
            Executes a single simulation step and redraws UI components.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        emu.step_simulation()

        telem = emu.get_telemetry()
        sim_state = emu.get_simulation_state()

        if self._canvas_xy is not None:
            self._canvas_xy.redraw(
                pose=telem.pose,
                joints=telem.joints,
                trail_points=sim_state.trail_points,
                current_target=sim_state.current_target
            )

        if self._canvas_z is not None:
            self._canvas_z.redraw(
                pose=telem.pose,
                current_target=sim_state.current_target
            )

        if self._telemetry_panel is not None:
            self._telemetry_panel.update_telemetry(telem)

        if self._demo_panel is not None:
            self._demo_panel.update_queue_depth(sim_state.queue_depth)

    def _schedule_next(self) -> None:
        '''
            Schedules next periodic callback if still running.

            :exceptions: None.
        '''
        if self._running and self._root is not None:
            self.tick()
            self._root.after(self._interval_ms, self._schedule_next)
