# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    GUI presentation adapter for SCARA Robot Emulator and 2D/3D Kinematic Visualizer.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Final

from scaraemu.core.service.iservice import IService
from scaraemu.core.service.demo_generator import TrajectoryDemoGenerator
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.communication.protocol.command_formatter import CommandFormatter
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.gui.theme import ThemeManager
from scaraemu.infrastructure.gui.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.components.serial_bar import SerialBar
from scaraemu.infrastructure.gui.components.telemetry_panel import TelemetryPanel
from scaraemu.infrastructure.gui.components.jog_panel import JogPanel
from scaraemu.infrastructure.gui.components.trajectory_demo_panel import TrajectoryDemoPanel
from scaraemu.infrastructure.gui.components.serial_console_panel import SerialConsolePanel
from scaraemu.infrastructure.gui.hardware_bridge_controller import HardwareBridgeController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraEmuGUI(IGUI):
    '''
        Top-level graphical user interface adapter for SCARA Emulator and Visualizer.

        It defines:

            :attributes:
                | _service - Kinematics and emulator simulation service facade.
                | _bridge - Hardware communication bridge controller.
                | _root - Root Tkinter window.
                | _canvas_xy - Top-down planar canvas.
                | _canvas_z - Side elevation canvas.
                | _telemetry_panel - Telemetry readout monitor.
                | _demo_panel - Autonomous trajectory demo panel.
            :methods:
                | __init__ - Initializes GUI adapter with service and transport dependencies.
                | is_initialized - Returns initialization status.
                | run - Constructs Tkinter windows and starts event loop.
    '''

    _service: Final[IService]
    _bridge: Final[HardwareBridgeController]
    _root: tk.Tk | None
    _serial_bar: SerialBar | None
    _canvas_xy: CanvasXY | None
    _canvas_z: CanvasZ | None
    _telemetry_panel: TelemetryPanel | None
    _demo_panel: TrajectoryDemoPanel | None

    def __init__(
        self,
        service: IService,
        transport: ITransport
    ) -> None:
        '''
            Initializes GUI adapter with service and transport dependencies.

            :param service: Kinematics and simulation service.
            :param transport: Communication transport.
            :exceptions: None.
        '''
        self._service = service
        self._bridge = HardwareBridgeController(
            transport=transport,
            on_state_change=self._on_bridge_state_change,
            on_telemetry=self._on_hardware_telemetry
        )
        self._root = None
        self._serial_bar = None
        self._canvas_xy = None
        self._canvas_z = None
        self._telemetry_panel = None
        self._demo_panel = None

    def is_initialized(self) -> bool:
        '''
            Returns initialization status.

            :return: True if GUI is initialized, False otherwise.
            :exceptions: None.
        '''
        return bool(self._service and self._bridge)

    def run(self) -> None:
        '''
            Constructs Tkinter widgets, layouts, and starts event loop.

            :exceptions: None.
        '''
        self._root = tk.Tk()
        self._root.title('SCARA Robot 4-DOF Emulator & Visualizer')
        sw: int = self._root.winfo_screenwidth()
        sh: int = self._root.winfo_screenheight()
        self._root.geometry(f'{sw}x{sh}+0+0')
        self._root.minsize(980, 680)
        self._root.configure(bg=ThemeManager.BG_DARK)

        self._serial_bar = SerialBar(self._root, on_connect_toggle=self._bridge.handle_connect_toggle)
        self._serial_bar.pack(fill=tk.X)

        main_paned = tk.PanedWindow(self._root, orient=tk.HORIZONTAL, bg=ThemeManager.BG_DARK, bd=0, sashwidth=4)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        left_col: tk.Frame = tk.Frame(main_paned, bg=ThemeManager.BG_DARK)
        main_paned.add(left_col, stretch='always')

        geom = self._service.get_kinematics().get_geometry()
        self._canvas_xy = CanvasXY(left_col, geometry=geom)
        self._canvas_xy.pack(fill=tk.BOTH, expand=True, pady=(0, 6))
        self._canvas_xy.set_on_target_click(self._handle_xy_click)

        self._canvas_z = CanvasZ(left_col, geometry=geom, height=180)
        self._canvas_z.pack(fill=tk.X)
        self._canvas_z.set_on_target_click(self._handle_z_click)

        right_col: tk.Frame = tk.Frame(main_paned, bg=ThemeManager.BG_DARK, width=390)
        main_paned.add(right_col, stretch='never')

        notebook = ttk.Notebook(right_col)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab_control: tk.Frame = tk.Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_demo: tk.Frame = tk.Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_console: tk.Frame = tk.Frame(notebook, bg=ThemeManager.BG_DARK)

        notebook.add(tab_control, text='  Monitor & Jog  ')
        notebook.add(tab_demo, text='  Trajectories  ')
        notebook.add(tab_console, text='  Serial Console  ')

        self._telemetry_panel = TelemetryPanel(tab_control)
        self._telemetry_panel.pack(fill=tk.X, pady=(0, 6))

        jog_panel = JogPanel(
            tab_control,
            on_jog=self._handle_jog,
            on_home_xy=lambda: self._handle_home('xy'),
            on_home_z=lambda: self._handle_home('z'),
            on_toggle_elbow=self._handle_toggle_elbow,
            on_toggle_motors=self._handle_toggle_motors,
            on_estop=self._handle_estop
        )
        jog_panel.pack(fill=tk.X)

        self._demo_panel = TrajectoryDemoPanel(
            tab_demo,
            on_demo_select=self._handle_demo_select,
            on_clear_queue=lambda: (self._service.get_emulator().clear_queue(), self._bridge.clear_queue())
        )
        self._demo_panel.pack(fill=tk.X, pady=(0, 6))

        console_panel = SerialConsolePanel(tab_console, on_send_cmd=self._bridge.handle_manual_send)
        console_panel.pack(fill=tk.BOTH, expand=True)

        self._bridge.set_log_listener(console_panel.append_log)

        self._root.update_idletasks()
        try:
            self._root.attributes('-zoomed', True)
        except tk.TclError:
            try:
                self._root.state('zoomed')
            except tk.TclError:
                pass

        self._schedule_tick()
        self._root.mainloop()

    def _schedule_tick(self) -> None:
        '''
            Schedules periodic animation and simulation tick.

            :exceptions: None.
        '''
        if self._root is not None:
            self._simulation_tick()
            self._root.after(25, self._schedule_tick)

    def _simulation_tick(self) -> None:
        '''
            Advances emulator simulation step and updates UI widgets.

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

    def _handle_xy_click(self, x: float, y: float) -> None:
        '''
            Handles click on XY planar canvas.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        new_pose = ScaraPose(x=x, y=y, z=curr.z, phi=curr.phi)
        emu.set_target_pose(new_pose, direct=False)
        self._bridge.send_hardware_move(new_pose)

    def _handle_z_click(self, z: float) -> None:
        '''
            Handles click on Z vertical canvas.

            :param z: Target Z in mm.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        new_pose = ScaraPose(x=curr.x, y=curr.y, z=z, phi=curr.phi)
        emu.set_target_pose(new_pose, direct=False)
        self._bridge.send_hardware_move(new_pose)

    def _handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Handles manual incremental jog displacement.

            :param dx: Delta X in mm.
            :param dy: Delta Y in mm.
            :param dz: Delta Z in mm.
            :param dphi: Delta Phi in radians.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        target = ScaraPose(
            x=curr.x + dx,
            y=curr.y + dy,
            z=curr.z + dz,
            phi=curr.phi + dphi
        )
        emu.set_target_pose(target, direct=False)
        self._bridge.send_hardware_move(target)

    def _handle_home(self, axis: str) -> None:
        '''
            Handles homing motion for specified axis (planar XY or vertical Z).

            :param axis: Target axis ('xy' or 'z').
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        geom = self._service.get_kinematics().get_geometry()
        curr = emu.get_current_pose()

        if axis == 'xy':
            home_x: float = (geom.l1 + geom.l2) * 0.65
            target = ScaraPose(x=home_x, y=0.0, z=curr.z, phi=0.0)
        elif axis == 'z':
            home_z: float = geom.z_min + 20.0
            target = ScaraPose(x=curr.x, y=curr.y, z=home_z, phi=curr.phi)
        else:
            home_x = (geom.l1 + geom.l2) * 0.65
            home_z = geom.z_min + 20.0
            target = ScaraPose(x=home_x, y=0.0, z=home_z, phi=0.0)

        emu.set_target_pose(target, direct=False)
        self._bridge.send_hardware_move(target)


    def _handle_toggle_elbow(self) -> None:
        '''
            Toggles between Lefty and Righty elbow configurations.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr_left = emu.get_telemetry().joints.theta2 < 0
        emu.set_elbow_mode(not curr_left)

    def _handle_toggle_motors(self) -> None:
        '''
            Toggles motor driver power enable.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr_state = emu.get_telemetry().motors_enabled
        emu.set_motors_enabled(not curr_state)
        cmd = CommandFormatter.format_enable_motors() if not curr_state else CommandFormatter.format_disable_motors()
        self._bridge.handle_manual_send(cmd)

    def _handle_estop(self) -> None:
        '''
            Executes emergency stop.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        emu.set_estop(True)
        self._bridge.clear_queue()
        self._bridge.handle_manual_send(CommandFormatter.format_estop())

    def _handle_demo_select(self, demo_name: str) -> None:
        '''
            Generates and queues demo trajectory waypoints.

            :param demo_name: Demo trajectory identifier.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        poses = TrajectoryDemoGenerator.generate(demo_name, center_x=curr.x, center_y=curr.y, z=curr.z)

        if poses:
            emu.enqueue_trajectory(poses)
            self._bridge.enqueue_hardware_trajectory(poses)

    def _on_bridge_state_change(self, connected: bool) -> None:
        '''
            Updates emulator service connection status.

            :param connected: Connection state.
            :exceptions: None.
        '''
        self._service.get_emulator().set_hardware_connected(connected)
        if self._serial_bar is not None:
            self._serial_bar.set_connected_state(connected)

    def _on_hardware_telemetry(self, pose: ScaraPose) -> None:
        '''
            Handles hardware telemetry pose update.

            :param pose: ScaraPose from microcontroller.
            :exceptions: None.
        '''
        self._service.get_emulator().update_hardware_pose(pose)

