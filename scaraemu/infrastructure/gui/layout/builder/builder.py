# -*- coding: UTF-8 -*-

'''
Module
    builder.py
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
    Builder constructing and styling the Tkinter widget layout hierarchy for the emulator GUI.
'''

from __future__ import annotations

from tkinter import BOTH, HORIZONTAL, X, Frame, PanedWindow, Tk
from tkinter.ttk import Notebook

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.console.panel import ConsolePanel
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.jog.panel import JogPanel
from scaraemu.infrastructure.gui.layout.builder.dependencies import LayoutDependencies
from scaraemu.infrastructure.gui.machine.panel import MachinePanel
from scaraemu.infrastructure.gui.telemetry.panel import TelemetryPanel
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.theme.style import NotebookStyleConfigurator
from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.toolbar.panel import SerialBar
from scaraemu.infrastructure.gui.trajectory.panel import TrajectoryDemoPanel
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LayoutBuilder:
    '''
        Constructs and wires the Tkinter widget layout hierarchy for the SCARA emulator GUI.

        It defines:

            :attributes:
                | _dependencies - Layout parameter bundle dependencies.
                | _is_built - Flag indicating if GUI layout hierarchy is constructed.
                | serial_bar - Top connection and server control toolbar.
                | canvas_xy - Top-down planar canvas.
                | canvas_z - Side elevation canvas.
                | telemetry_panel - Telemetry readout monitor.
                | jog_panel - Manual jog control panel.
                | machine_panel - Machine state, configuration, and safety panel.
                | demo_panel - Trajectory demo presets and script loading.
                | console_panel - Serial communication log and manual CLI.
            :methods:
                | __init__ - Initializes layout builder with layout dependencies bundle.
                | build_layout - Builds and packs all GUI widget components.
                | set_connected_state - Updates hardware connection state in layout toolbar.
                | set_server_state - Updates virtual robot server state in layout toolbar.
                | append_log - Appends diagnostic log entry to layout console panel.
                | get_version - Returns builder component version string.
    '''

    _dependencies: LayoutDependencies
    _is_built: bool
    serial_bar: SerialBar
    canvas_xy: CanvasXY
    canvas_z: CanvasZ
    telemetry_panel: TelemetryPanel
    jog_panel: JogPanel
    machine_panel: MachinePanel
    demo_panel: TrajectoryDemoPanel
    console_panel: ConsolePanel
    telemetry_view: ITelemetryView
    queue_view: IQueueDepthView

    def __init__(
        self,
        dependencies: LayoutDependencies,
    ) -> None:
        '''
            Initializes layout builder with layout dependencies bundle.

            :param dependencies: Injected LayoutDependencies parameter bundle.
            :exceptions: None.
        '''
        self._dependencies = dependencies
        self._is_built = False

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
            :param delegates: Injected GUI action delegates bundle.
            :exceptions: None.
        '''
        self.serial_bar = SerialBar(
            root,
            delegate=delegates.serial_bar,
            port_scanner=self._dependencies.port_scanner,
            preference_repository=self._dependencies.preference_repository,
        )
        self.serial_bar.pack(fill=X)

        main_paned = PanedWindow(root, orient=HORIZONTAL, bg=ThemeManager.BG_DARK, bd=0, sashwidth=4)
        main_paned.pack(fill=BOTH, expand=True, padx=8, pady=8)

        left_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK)
        main_paned.add(left_col, stretch='always')

        config_xy = CanvasConfig(
            bounds=bounds,
            width=480,
            height=480,
            target_click_listener=target_click_listener,
        )
        self.canvas_xy = CanvasXY(
            left_col,
            config=config_xy,
            manipulator_linkage_adapter=self._dependencies.manipulator_linkage_adapter,
            reach_adapter=self._dependencies.reach_adapter,
            boundary_service=self._dependencies.boundary_service,
        )
        self.canvas_xy.pack(fill=BOTH, expand=True, pady=(0, 6))

        config_z = CanvasConfig(
            bounds=bounds,
            width=480,
            height=180,
            target_click_listener=target_click_listener,
        )
        self.canvas_z = CanvasZ(left_col, config=config_z)
        self.canvas_z.pack(fill=X)

        right_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK, width=390)
        main_paned.add(right_col, stretch='never')

        NotebookStyleConfigurator.configure(root)

        notebook = Notebook(right_col)
        notebook.pack(fill=BOTH, expand=True)
        notebook.bind('<<NotebookTabChanged>>', lambda e: notebook.update_idletasks())

        tab_control: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_demo: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)
        tab_console: Frame = Frame(notebook, bg=ThemeManager.BG_DARK)

        notebook.add(tab_control, text='  Monitor & Jog  ')
        notebook.add(tab_demo, text='  Trajectories  ')
        notebook.add(tab_console, text='  Serial Console  ')

        self.telemetry_panel = TelemetryPanel(tab_control)
        self.telemetry_panel.pack(fill=X, pady=(0, 6))

        self.jog_panel = JogPanel(
            tab_control,
            jog_delegate=delegates.jog,
        )
        self.jog_panel.pack(fill=X, pady=(0, 6))

        self.machine_panel = MachinePanel(
            tab_control,
            config_delegate=delegates.config,
            safety_delegate=delegates.safety,
        )
        self.machine_panel.pack(fill=X)

        self.demo_panel = TrajectoryDemoPanel(
            tab_demo,
            preset_delegate=delegates.preset,
            script_delegate=delegates.script,
            queue_delegate=delegates.queue,
        )
        self.demo_panel.pack(fill=X, pady=(0, 6))

        self.console_panel = ConsolePanel(tab_console)
        self.console_panel.pack(fill=BOTH, expand=True)

        self.telemetry_view = self.telemetry_panel
        self.queue_view = self.demo_panel.queue_section
        self._is_built = True

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates hardware connection state in layout toolbar.

            :param connected: True if connected to hardware, False otherwise.
            :exceptions: None.
        '''
        if self._is_built:
            self.serial_bar.set_connected_state(connected)

    def set_server_state(self, running: bool, port: int = 8888) -> None:
        '''
            Updates virtual robot server state in layout toolbar.

            :param running: True if server active, False otherwise.
            :param port: Listening TCP port number.
            :exceptions: None.
        '''
        if self._is_built:
            self.serial_bar.set_server_state(running, port)

    def append_log(self, message: str, tag: str) -> None:
        '''
            Appends diagnostic log entry to layout console panel.

            :param message: Diagnostic log text line.
            :param tag: Log entry category tag.
            :exceptions: None.
        '''
        if self._is_built:
            self.console_panel.append_log(message, tag)

    def get_version(self) -> str:
        '''
            Returns builder component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
