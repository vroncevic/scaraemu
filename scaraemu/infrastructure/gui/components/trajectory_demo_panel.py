# -*- coding: UTF-8 -*-

'''
Module
    trajectory_demo_panel.py
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
    Demo trajectory generation and simulation queue control panel.
'''

from __future__ import annotations

from pathlib import Path
from tkinter import (
    FLAT,
    LEFT,
    RIGHT,
    TOP,
    Button,
    Frame,
    Label,
    LabelFrame,
    Widget,
    X,
)
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from typing import Callable

from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoPanel(LabelFrame):
    '''
        Panel for selecting and triggering predefined autonomous demonstration trajectories.

        It defines:

            :attributes:
                | _lbl_queue - Motion queue depth label.
                | _on_demo_select - Callback receiving selected trajectory preset name.
                | _on_clear_queue - Callback for clearing motion queue and path trail.
                | _on_load_script - Callback receiving path to .scara script to load.
                | _cbo_scripts - Combobox selector for bundled .scara examples.
                | _script_paths - Mapping from example display names to file paths.
            :methods:
                | __init__ - Initializes demo buttons and queue status display.
                | update_queue_depth - Updates queue count display.
                | _populate_examples - Discovers and populates bundled .scara scripts.
                | _on_script_selected - Dispatches script loading on combobox selection.
                | _on_browse_file - Opens file dialog to load user .scara or .json plan.
    '''

    _lbl_queue: Label
    _on_demo_select: Callable[[str], None] | None
    _on_clear_queue: Callable[[], None] | None
    _on_load_script: Callable[[str], None] | None
    _cbo_scripts: Combobox
    _script_paths: dict[str, str]

    def __init__(
        self,
        parent: Widget,
        on_demo_select: Callable[[str], None] | None = None,
        on_clear_queue: Callable[[], None] | None = None,
        on_load_script: Callable[[str], None] | None = None,
    ) -> None:
        '''
            Initializes demo buttons, script loader, and queue status display.

            :param parent: Parent Tkinter widget.
            :param on_demo_select: Callback when demo preset button is clicked.
            :param on_clear_queue: Callback when clear queue button is clicked.
            :param on_load_script: Callback when .scara script or plan is loaded.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Demo Trajectories  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8
        )
        self._on_demo_select = on_demo_select
        self._on_clear_queue = on_clear_queue
        self._on_load_script = on_load_script
        self._script_paths = {}

        grid_btn: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        grid_btn.pack(fill=X, pady=(0, 8))

        self._make_btn(grid_btn, 'Circle', 0, 0, lambda: self._trigger('circle'))
        self._make_btn(grid_btn, 'Square', 0, 1, lambda: self._trigger('square'))
        self._make_btn(grid_btn, '5-Star', 1, 0, lambda: self._trigger('star'))
        self._make_btn(grid_btn, '3D Helix', 1, 1, lambda: self._trigger('helix'))
        self._make_btn(grid_btn, 'Pick & Place (JUMP)', 2, 0, lambda: self._trigger('pick_and_place'), colspan=2)

        # SCARA DSL script / example loader
        scara_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        scara_frame.pack(fill=X, pady=(4, 6))

        lbl_scara = Label(
            scara_frame,
            text='SCARA DSL Script:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 8),
        )
        lbl_scara.pack(side=TOP, anchor='w')

        ctrl_row: Frame = Frame(scara_frame, bg=ThemeManager.BG_PANEL)
        ctrl_row.pack(fill=X, pady=(2, 0))

        self._cbo_scripts = Combobox(ctrl_row, state='readonly', width=16)
        self._cbo_scripts.pack(side=LEFT, fill=X, expand=True, padx=(0, 4))
        self._populate_examples()
        self._cbo_scripts.bind('<<ComboboxSelected>>', lambda e: self._on_script_selected())

        btn_browse: Button = Button(
            ctrl_row,
            text='📂 Load',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._on_browse_file,
        )
        btn_browse.pack(side=RIGHT)

        q_frame: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        q_frame.pack(fill=X, pady=(4, 0))

        self._lbl_queue = Label(
            q_frame,
            text='Queue: 0 pts',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 8)
        )
        self._lbl_queue.pack(side=LEFT)

        btn_clear: Button = Button(
            q_frame,
            text='Clear Queue',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self._clear
        )
        btn_clear.pack(side=RIGHT)

    def _populate_examples(self) -> None:
        '''
            Discovers and populates bundled .scara scripts into the selector.

            :exceptions: None.
        '''
        search_dirs = [
            Path(__file__).resolve().parents[6] / 'scarajectory' / 'github' / 'scarajectory' / 'examples',
            Path('/data/dev/python/3_tools/scarajectory/github/scarajectory/examples'),
            Path('examples'),
        ]
        self._script_paths = {}
        for d in search_dirs:
            if d.is_dir():
                for p in sorted(d.glob('*.scara')):
                    self._script_paths[p.name] = str(p)
                if self._script_paths:
                    break

        if self._script_paths:
            self._cbo_scripts['values'] = list(self._script_paths.keys())

    def _on_script_selected(self) -> None:
        '''
            Dispatches script loading when user selects from combobox.

            :exceptions: None.
        '''
        name = self._cbo_scripts.get()
        filepath = self._script_paths.get(name)
        if filepath and self._on_load_script is not None:
            self._on_load_script(filepath)

    def _on_browse_file(self) -> None:
        '''
            Opens file dialog to load user .scara or .json plan.

            :exceptions: None.
        '''
        self.update_idletasks()
        filepath = askopenfilename(
            parent=self.winfo_toplevel(),
            filetypes=[
                ('SCARA Scripts & Plans', '*.scara *.json'),
                ('All Files', '*.*'),
            ]
        )
        if filepath and self._on_load_script is not None:
            self._on_load_script(filepath)
            self.update_idletasks()

    def _trigger(self, demo_name: str) -> None:
        '''
            Dispatches demo trigger callback.

            :param demo_name: Trajectory preset name.
            :exceptions: None.
        '''
        if self._on_demo_select is not None:
            self._on_demo_select(demo_name)

    def _clear(self) -> None:
        '''
            Dispatches clear queue callback.

            :param demo_name: None.
            :exceptions: None.
        '''
        if self._on_clear_queue is not None:
            self._on_clear_queue()

    def update_queue_depth(self, count: int) -> None:
        '''
            Updates queue count display.

            :param count: Current queue depth count.
            :exceptions: None.
        '''
        if not self.winfo_ismapped():
            return

        color = ThemeManager.ACCENT_GREEN if count == 0 else ThemeManager.ACCENT_ORANGE
        self._lbl_queue.config(text=f'Queue: {count} pts', fg=color)

    def _make_btn(
        self,
        parent: Frame,
        text: str,
        r: int,
        c: int,
        cmd: Callable[[], None],
        colspan: int = 1
    ) -> Button:
        '''
            Helper creating styled preset button.

            :param parent: Parent frame container.
            :param text: Button text.
            :param r: Grid row.
            :param c: Grid column.
            :param cmd: Click handler.
            :param colspan: Grid column span.
            :return: The button instance.
            :exceptions: None.
        '''
        b = Button(
            parent,
            text=text,
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=cmd
        )
        b.grid(row=r, column=c, columnspan=colspan, sticky='ew', padx=2, pady=2)
        parent.grid_columnconfigure(c, weight=1)
        return b
