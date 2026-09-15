# -*- coding: UTF-8 -*-

'''
Module
    script_loader_section.py
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
    GUI sub-panel component for selecting bundled examples or loading custom .scara scripts.
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
    Widget,
    X,
)
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from typing import Callable

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptLoaderSection(Frame):
    '''
        Sub-panel for discovering, choosing, and loading SCARA DSL scripts and JSON plans.

        It defines:

            :attributes:
                | _cbo_scripts - Combobox selector for bundled examples.
                | _script_paths - Mapping from example display names to file paths.
                | _on_load_script - Callback receiving path to script or plan.
            :methods:
                | __init__ - Initializes script loader selector and browse button.
                | _populate_examples - Discovers and populates bundled .scara scripts.
                | _on_script_selected - Dispatches script loading on combobox selection.
                | _on_browse_file - Opens file dialog to load user .scara or .json plan.
    '''

    _cbo_scripts: Combobox
    _script_paths: dict[str, str]
    _on_load_script: Callable[[str], None] | None

    def __init__(
        self,
        parent: Widget,
        on_load_script: Callable[[str], None] | None = None
    ) -> None:
        '''
            Initializes script loader selector and browse button.

            :param parent: Parent Tkinter widget.
            :param on_load_script: Callback when .scara script or plan is selected.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._on_load_script = on_load_script
        self._script_paths = {}

        lbl_scara = Label(
            self,
            text='SCARA DSL Script:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 8),
        )
        lbl_scara.pack(side=TOP, anchor='w')

        ctrl_row: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
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

    def _populate_examples(self) -> None:
        '''
            Discovers and populates bundled .scara scripts into the selector.

            :exceptions: None.
        '''
        search_dirs: list[Path] = [
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
        name: str = self._cbo_scripts.get()
        filepath: str | None = self._script_paths.get(name)
        if filepath and self._on_load_script is not None:
            self._on_load_script(filepath)

    def _on_browse_file(self) -> None:
        '''
            Opens file dialog to load user .scara or .json plan.

            :exceptions: None.
        '''
        self.update_idletasks()
        filepath: str = askopenfilename(
            parent=self.winfo_toplevel(),
            filetypes=[
                ('SCARA Scripts & Plans', '*.scara *.json'),
                ('All Files', '*.*'),
            ]
        )
        if filepath and self._on_load_script is not None:
            self._on_load_script(filepath)
            self.update_idletasks()
