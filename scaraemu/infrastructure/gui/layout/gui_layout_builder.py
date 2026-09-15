# -*- coding: UTF-8 -*-

'''
Module
    gui_layout_builder.py
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
from typing import Any, Callable

from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.canvas.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.toolbar.serial_bar import SerialBar
from scaraemu.infrastructure.gui.controls.telemetry_panel import TelemetryPanel
from scaraemu.infrastructure.gui.controls.jog_panel import JogPanel
from scaraemu.infrastructure.gui.trajectory.trajectory_demo_panel import TrajectoryDemoPanel
from scaraemu.infrastructure.gui.console.serial_console_panel import SerialConsolePanel
from scaraemu.infrastructure.gui.events.gui_event_handler import GuiEventHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLayoutBuilder:
    '''
        Constructs and wires the Tkinter widget layout hierarchy for the SCARA emulator GUI.

        It defines:

            :attributes:
                | serial_bar - Top connection and server control toolbar.
                | canvas_xy - Top-down planar canvas.
                | canvas_z - Side elevation canvas.
                | telemetry_panel - Telemetry readout monitor.
                | jog_panel - Manual jogging and homing control panel.
                | demo_panel - Autonomous trajectory demo panel.
                | console_panel - Host and bridge serial log console.
            :methods:
                | __init__ - Initializes empty layout builder.
                | setup_window - Configures root window dimensions and theme styling.
                | build_layout - Instantiates and arranges all widgets within root window.
                | _configure_notebook_style - Sets up ttk Notebook tab styles.
    '''

    serial_bar: SerialBar
    canvas_xy: CanvasXY
    canvas_z: CanvasZ
    telemetry_panel: TelemetryPanel
    jog_panel: JogPanel
    demo_panel: TrajectoryDemoPanel
    console_panel: SerialConsolePanel

    def setup_window(self, root: Tk) -> None:
        '''
            Configures root window title, geometry, and styles.

            :param root: Tkinter root window.
            :exceptions: None.
        '''
        root.title('SCARA Robot 4-DOF Emulator & Visualizer')
        sw: int = root.winfo_screenwidth()
        sh: int = root.winfo_screenheight()
        root.geometry(f'{sw}x{sh}+0+0')
        root.minsize(980, 680)
        root.configure(bg=ThemeManager.BG_DARK)

    def maximize_window(self, root: Tk) -> None:
        '''
            Attempts to maximize root window across platforms.

            :param root: Tkinter root window.
            :exceptions: None.
        '''
        root.update_idletasks()
        try:
            root.attributes('-zoomed', True)
        except TclError:
            try:
                root.state('zoomed')
            except TclError:
                pass

    def _configure_notebook_style(self, root: Tk) -> None:
        '''
            Applies customized clam styling to ttk Notebook tabs.

            :param root: Tkinter root window.
            :exceptions: None.
        '''
        style = Style(root)
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

    def build_layout(
        self,
        root: Tk,
        geometry: ScaraGeometry,
        event_handler: GuiEventHandler,
        on_connect_toggle: Callable[[str, int], None],
        on_server_toggle: Callable[[], None],
        on_manual_send: Callable[[str], None],
        on_toggle_hold: Callable[[], None],
        on_clear_queue: Callable[[], None]
    ) -> None:
        '''
            Builds and packs the complete GUI layout hierarchy.

            :param root: Tkinter root window.
            :param geometry: SCARA kinematic geometry parameters.
            :param event_handler: GUI event handler for interaction callbacks.
            :param on_connect_toggle: Serial bar connection callback.
            :param on_server_toggle: Virtual server toggle callback.
            :param on_manual_send: Console manual command send callback.
            :param on_toggle_hold: Hold button toggle callback.
            :param on_clear_queue: Queue clear callback.
            :exceptions: None.
        '''
        self.serial_bar = SerialBar(
            root,
            on_connect_toggle=on_connect_toggle,
            on_server_toggle=on_server_toggle
        )
        self.serial_bar.pack(fill=X)

        main_paned = PanedWindow(root, orient=HORIZONTAL, bg=ThemeManager.BG_DARK, bd=0, sashwidth=4)
        main_paned.pack(fill=BOTH, expand=True, padx=8, pady=8)

        left_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK)
        main_paned.add(left_col, stretch='always')

        self.canvas_xy = CanvasXY(left_col, geometry=geometry)
        self.canvas_xy.pack(fill=BOTH, expand=True, pady=(0, 6))

        self.canvas_z = CanvasZ(left_col, geometry=geometry, height=180)
        self.canvas_z.pack(fill=X)

        self.canvas_xy.set_on_target_click(event_handler.handle_xy_click)
        self.canvas_z.set_on_target_click(event_handler.handle_z_click)

        right_col: Frame = Frame(main_paned, bg=ThemeManager.BG_DARK, width=390)
        main_paned.add(right_col, stretch='never')

        self._configure_notebook_style(root)

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
            on_jog=event_handler.handle_jog,
            on_home_xy=lambda: event_handler.handle_home('xy'),
            on_home_z=lambda: event_handler.handle_home('z'),
            on_toggle_elbow=event_handler.handle_toggle_elbow,
            on_toggle_motors=event_handler.handle_toggle_motors,
            on_toggle_hold=on_toggle_hold,
            on_estop=event_handler.handle_estop
        )
        self.jog_panel.pack(fill=X)

        self.demo_panel = TrajectoryDemoPanel(
            tab_demo,
            on_demo_select=event_handler.handle_demo_select,
            on_clear_queue=on_clear_queue,
            on_load_script=event_handler.handle_load_script
        )
        self.demo_panel.pack(fill=X, pady=(0, 6))

        self.console_panel = SerialConsolePanel(tab_console, on_send_cmd=on_manual_send)
        self.console_panel.pack(fill=BOTH, expand=True)
