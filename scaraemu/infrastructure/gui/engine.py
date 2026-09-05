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

from tkinter import (
    BOTH,
    HORIZONTAL,
    X,
    Frame,
    PanedWindow,
    TclError,
    Tk,
)
from tkinter.ttk import Notebook, Style
from typing import Final

from scaraemu.core.service.iservice import IService
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.gui.theme import ThemeManager
from scaraemu.infrastructure.gui.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.components.serial_bar import SerialBar
from scaraemu.infrastructure.gui.components.telemetry_panel import TelemetryPanel
from scaraemu.infrastructure.gui.components.jog_panel import JogPanel
from scaraemu.infrastructure.gui.components.trajectory_demo_panel import TrajectoryDemoPanel
from scaraemu.infrastructure.gui.components.serial_console_panel import SerialConsolePanel
from scaraemu.infrastructure.communication.transport.virtual_robot_server import VirtualRobotServer
from scaraemu.infrastructure.gui.hardware_bridge_controller import HardwareBridgeController
from scaraemu.infrastructure.gui.gui_event_handler import GuiEventHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
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
                | _initial_script - Optional initial script to parse on launch.
                | _initial_server - Optional TCP port for virtual server on launch.
                | _virtual_server - Virtual robot TCP server instance.
                | _root - Root Tkinter window.
                | _serial_bar - Top connection and server control toolbar.
                | _canvas_xy - Top-down planar canvas.
                | _canvas_z - Side elevation canvas.
                | _telemetry_panel - Telemetry readout monitor.
                | _demo_panel - Autonomous trajectory demo panel.
                | _console_panel - Host and bridge serial log console.
            :methods:
                | __init__ - Initializes GUI adapter with service and transport dependencies.
                | is_initialized - Returns initialization status.
                | _toggle_virtual_server - Starts or stops virtual robot TCP server.
                | run - Constructs Tkinter windows and starts event loop.
    '''

    _service: Final[IService]
    _bridge: Final[HardwareBridgeController]
    _initial_script: str | None
    _initial_server: int | None
    _virtual_server: VirtualRobotServer | None
    _root: Tk | None
    _serial_bar: SerialBar | None
    _canvas_xy: CanvasXY | None
    _canvas_z: CanvasZ | None
    _telemetry_panel: TelemetryPanel | None
    _demo_panel: TrajectoryDemoPanel | None
    _console_panel: SerialConsolePanel | None

    def __init__(
        self,
        service: IService,
        transport: ITransport,
        initial_script: str | None = None,
        initial_server: int | None = None
    ) -> None:
        '''
            Initializes GUI adapter with service and transport dependencies.

            :param service: Simulation and kinematics facade.
            :param transport: Communication transport instance.
            :param initial_script: Optional path to script to load on startup.
            :param initial_server: Optional TCP port to start virtual server on.
            :exceptions: None.
        '''
        self._service = service
        self._bridge = HardwareBridgeController(
            transport=transport,
            on_state_change=self._on_bridge_state_change,
            on_telemetry=self._on_hardware_telemetry,
            on_elbow_change=self._on_hardware_elbow_change
        )
        self._initial_script = initial_script
        self._initial_server = initial_server
        self._virtual_server = None
        self._root = None
        self._serial_bar = None
        self._canvas_xy = None
        self._canvas_z = None
        self._telemetry_panel = None
        self._demo_panel = None
        self._console_panel = None

    def is_initialized(self) -> bool:
        '''
            Returns initialization status.

            :return: True if GUI is initialized, False otherwise.
            :exceptions: None.
        '''
        return bool(self._service and self._bridge)

    def load_file(self, file_path: str) -> None:
        '''
            Sets initial plan or DSL script to load upon GUI startup.

            :param file_path: Path to script or plan file.
            :exceptions: None.
        '''
        self._initial_script = file_path

    def run(self) -> None:
        '''
            Constructs Tkinter widgets, layouts, and starts event loop.

            :exceptions: None.
        '''
        self._root = Tk()
        self._root.title('SCARA Robot 4-DOF Emulator & Visualizer')
        sw: int = self._root.winfo_screenwidth()
        sh: int = self._root.winfo_screenheight()
        self._root.geometry(f'{sw}x{sh}+0+0')
        self._root.minsize(980, 680)
        self._root.configure(bg=ThemeManager.BG_DARK)

        self._serial_bar = SerialBar(
            self._root,
            on_connect_toggle=self._bridge.handle_connect_toggle,
            on_server_toggle=self._toggle_virtual_server
        )
        self._serial_bar.pack(fill=X)

        main_paned = PanedWindow(self._root, orient=HORIZONTAL, bg=ThemeManager.BG_DARK, bd=0, sashwidth=4)
        main_paned.pack(fill=BOTH, expand=True, padx=8, pady=8)

        left_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK)
        main_paned.add(left_col, stretch='always')

        geom = self._service.get_kinematics().get_geometry()
        self._canvas_xy = CanvasXY(left_col, geometry=geom)
        self._canvas_xy.pack(fill=BOTH, expand=True, pady=(0, 6))

        self._canvas_z = CanvasZ(left_col, geometry=geom, height=180)
        self._canvas_z.pack(fill=X)

        event_handler = GuiEventHandler(
            service=self._service,
            bridge=self._bridge,
            log_host=self._log_host,
            flash_unreachable=lambda x, y: self._canvas_xy.flash_unreachable(x, y) if self._canvas_xy is not None else None
        )

        self._canvas_xy.set_on_target_click(event_handler.handle_xy_click)
        self._canvas_z.set_on_target_click(event_handler.handle_z_click)

        right_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK, width=390)
        main_paned.add(right_col, stretch='never')

        style = Style(self._root)
        style.theme_use('clam')
        style.configure('TNotebook', background=ThemeManager.BG_DARK, borderwidth=0)
        style.configure(
            'TNotebook.Tab',
            background=ThemeManager.BG_PANEL,
            foreground=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padding=[12, 5],
            focuscolor=ThemeManager.BG_DARK
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', ThemeManager.BG_CANVAS), ('active', ThemeManager.BG_PANEL)],
            foreground=[('selected', ThemeManager.ACCENT_CYAN), ('active', ThemeManager.TEXT_PRIMARY)]
        )

        notebook = Notebook(right_col)
        notebook.pack(fill=BOTH, expand=True)
        notebook.bind('<<NotebookTabChanged>>', lambda e: notebook.update_idletasks())

        tab_control: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_demo: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_console: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)

        notebook.add(tab_control, text='  Monitor & Jog  ')
        notebook.add(tab_demo, text='  Trajectories  ')
        notebook.add(tab_console, text='  Serial Console  ')

        self._telemetry_panel = TelemetryPanel(tab_control)
        self._telemetry_panel.pack(fill=X, pady=(0, 6))

        def _toggle_hold() -> None:
            emu = self._service.get_emulator()
            held = not emu.get_telemetry().hold_active
            emu.set_hold(held)
            if held:
                self._bridge.send_hardware_hold()
            else:
                self._bridge.send_hardware_resume()

        jog_panel = JogPanel(
            tab_control,
            on_jog=event_handler.handle_jog,
            on_home_xy=lambda: event_handler.handle_home('xy'),
            on_home_z=lambda: event_handler.handle_home('z'),
            on_toggle_elbow=event_handler.handle_toggle_elbow,
            on_toggle_motors=event_handler.handle_toggle_motors,
            on_toggle_hold=_toggle_hold,
            on_estop=event_handler.handle_estop
        )
        jog_panel.pack(fill=X)

        self._demo_panel = TrajectoryDemoPanel(
            tab_demo,
            on_demo_select=event_handler.handle_demo_select,
            on_clear_queue=lambda: (self._service.get_emulator().clear_queue(), self._bridge.clear_queue()),
            on_load_script=event_handler.handle_load_script
        )
        self._demo_panel.pack(fill=X, pady=(0, 6))

        self._console_panel = SerialConsolePanel(tab_console, on_send_cmd=self._bridge.handle_manual_send)
        self._console_panel.pack(fill=BOTH, expand=True)

        self._bridge.set_log_listener(self._console_panel.append_log)

        self._root.update_idletasks()
        try:
            self._root.attributes('-zoomed', True)
        except TclError:
            try:
                self._root.state('zoomed')
            except TclError:
                pass

        if self._initial_server:
            self._toggle_virtual_server()

        if self._initial_script:
            event_handler.handle_load_script(self._initial_script)

        self._schedule_tick()
        self._root.mainloop()

    def _toggle_virtual_server(self) -> None:
        '''
            Starts or stops background TCP virtual robot server.

            :exceptions: None.
        '''
        if self._virtual_server is not None and self._virtual_server.is_running():
            self._virtual_server.stop()
            if self._serial_bar is not None:
                self._serial_bar.set_server_state(False)
            self._log_host('[HOST]: Virtual Robot Server stopped.', 'info')
        else:
            if self._virtual_server is None:
                self._virtual_server = VirtualRobotServer(
                    emulator=self._service.get_emulator(),
                    on_log=lambda msg: self._log_host(msg, 'info')
                )
            port: int = self._initial_server if self._initial_server else 8888
            success: bool = self._virtual_server.start(port=port)
            if self._serial_bar is not None:
                self._serial_bar.set_server_state(success, port)
            if success:
                self._log_host(f'[HOST]: Virtual Robot Server listening on 127.0.0.1:{port}', 'info')
            else:
                self._log_host(f'[HOST]: Failed to start Virtual Robot Server on port {port}', 'err')

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

    def _log_host(self, msg: str, tag: str = 'err') -> None:
        '''
            Appends host diagnostic message to serial console.

            :param msg: Message string.
            :param tag: Color tag.
            :exceptions: None.
        '''
        if self._console_panel is not None:
            self._console_panel.append_log(msg, tag)
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

    def _on_hardware_elbow_change(self, is_left: bool) -> None:
        '''
            Synchronizes local emulator elbow configuration from hardware.

            :param is_left: True if Lefty, False if Righty.
            :exceptions: None.
        '''
        self._service.get_emulator().set_elbow_mode(is_left)

