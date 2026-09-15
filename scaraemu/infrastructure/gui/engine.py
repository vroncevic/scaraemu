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

from tkinter import Tk
from typing import Final

from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.gui.bridge.hardware_bridge_controller import HardwareBridgeController
from scaraemu.infrastructure.gui.events.gui_event_handler import GuiEventHandler
from scaraemu.infrastructure.gui.server.virtual_server_manager import VirtualServerManager
from scaraemu.infrastructure.gui.ticker.simulation_ticker import SimulationTicker
from scaraemu.infrastructure.gui.layout.gui_layout_builder import GuiLayoutBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraEmuGUI:
    '''
        Top-level graphical user interface adapter for SCARA Emulator and Visualizer.

        It defines:

            :attributes:
                | _service - Kinematics and emulator simulation service facade.
                | _bridge - Hardware communication bridge controller.
                | _initial_script - Optional initial script to parse on launch.
                | _initial_server - Optional TCP port for virtual server on launch.
                | _layout_builder - UI widget hierarchy constructor.
                | _server_manager - Virtual robot TCP server lifecycle manager.
                | _ticker - Periodic simulation and visualization ticker.
                | _root - Root Tkinter window.
            :methods:
                | __init__ - Initializes GUI adapter with service and transport dependencies.
                | is_initialized - Returns initialization status.
                | load_file - Sets initial plan or DSL script to load upon GUI startup.
                | run - Constructs Tkinter windows and starts event loop.
    '''

    _service: Final[IService]
    _bridge: Final[HardwareBridgeController]
    _initial_script: str | None
    _initial_server: int | None
    _layout_builder: GuiLayoutBuilder
    _server_manager: VirtualServerManager
    _ticker: SimulationTicker | None
    _root: Tk | None

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
        self._layout_builder = GuiLayoutBuilder()
        self._server_manager = VirtualServerManager(
            emulator=self._service.get_emulator(),
            log_host=self._log_host,
            state_callback=self._on_server_state_changed
        )
        self._ticker = None
        self._root = None

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
        self._layout_builder.setup_window(self._root)

        event_handler = GuiEventHandler(
            service=self._service,
            bridge=self._bridge,
            log_host=self._log_host,
            flash_unreachable=lambda x, y: self._layout_builder.canvas_xy.flash_unreachable(x, y)
        )

        self._layout_builder.build_layout(
            root=self._root,
            geometry=self._service.get_kinematics().get_geometry(),
            event_handler=event_handler,
            on_connect_toggle=self._bridge.handle_connect_toggle,
            on_server_toggle=self._toggle_virtual_server,
            on_manual_send=self._bridge.handle_manual_send,
            on_toggle_hold=self._toggle_hold,
            on_clear_queue=lambda: (
                self._service.get_emulator().clear_queue(),
                self._bridge.clear_queue()
            )
        )

        self._bridge.set_log_listener(self._layout_builder.console_panel.append_log)
        self._layout_builder.maximize_window(self._root)

        if self._initial_server:
            self._toggle_virtual_server()

        if self._initial_script:
            event_handler.handle_load_script(self._initial_script)

        self._ticker = SimulationTicker(
            service=self._service,
            canvas_xy=self._layout_builder.canvas_xy,
            canvas_z=self._layout_builder.canvas_z,
            telemetry_panel=self._layout_builder.telemetry_panel,
            demo_panel=self._layout_builder.demo_panel
        )
        self._ticker.start(self._root)
        self._root.mainloop()

    def _toggle_virtual_server(self) -> None:
        '''
            Starts or stops background TCP virtual robot server.

            :exceptions: None.
        '''
        port: int = self._initial_server if self._initial_server else 8888
        self._server_manager.toggle(port=port)

    def _on_server_state_changed(self, running: bool, port: int | None) -> None:
        '''
            Updates serial bar UI button state when server state changes.

            :param running: True if server started, False if stopped.
            :param port: Listening port if running.
            :exceptions: None.
        '''
        if hasattr(self._layout_builder, 'serial_bar') and self._layout_builder.serial_bar is not None:
            self._layout_builder.serial_bar.set_server_state(running, port)

    def _toggle_hold(self) -> None:
        '''
            Toggles hold state on emulator and sends hold/resume to hardware bridge.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        held = not emu.get_telemetry().hold_active
        emu.set_hold(held)
        if held:
            self._bridge.send_hardware_hold()
        else:
            self._bridge.send_hardware_resume()

    def _log_host(self, msg: str, tag: str = 'err') -> None:
        '''
            Appends host diagnostic message to serial console.

            :param msg: Message string.
            :param tag: Color tag.
            :exceptions: None.
        '''
        if hasattr(self._layout_builder, 'console_panel') and self._layout_builder.console_panel is not None:
            self._layout_builder.console_panel.append_log(msg, tag)

    def _on_bridge_state_change(self, connected: bool) -> None:
        '''
            Updates emulator service connection status.

            :param connected: Connection state.
            :exceptions: None.
        '''
        self._service.get_emulator().set_hardware_connected(connected)
        if hasattr(self._layout_builder, 'serial_bar') and self._layout_builder.serial_bar is not None:
            self._layout_builder.serial_bar.set_connected_state(connected)

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
