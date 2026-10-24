# -*- coding: UTF-8 -*-

'''
Module
    section.py
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

from tkinter import (
    Button,
    FLAT,
    Frame,
    Label,
    LEFT,
    RIGHT,
    TOP,
    Widget,
    X,
)
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate
from scaraemu.infrastructure.scaralang.script.discovery import ScriptExampleDiscovery

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
                | _delegate - Action delegate receiving selected script path.
            :methods:
                | __init__ - Initializes script loader selector and browse button.
                | load_example - Loads named or selected script from discovered examples.
                | handle_browse_file - Opens file dialog to load user .scara or .json plan.
                | get_version - Returns component version string.
    '''

    _cbo_scripts: Combobox
    _script_paths: dict[str, str]
    _delegate: IScriptLoaderDelegate

    def __init__(self, parent: Widget, delegate: IScriptLoaderDelegate) -> None:
        '''
            Initializes script loader selector and browse button.

            :param parent: Parent Tkinter widget container.
            :param delegate: Action delegate handling script loading.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._delegate: Final[IScriptLoaderDelegate] = delegate

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

        self._script_paths = ScriptExampleDiscovery.discover_examples()
        if self._script_paths:
            self._cbo_scripts['values'] = list(self._script_paths.keys())

        self._cbo_scripts.bind('<<ComboboxSelected>>', lambda _: self.load_example())

        btn_browse: Button = Button(
            ctrl_row,
            text='📂 Load',
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=self.handle_browse_file,
        )
        btn_browse.pack(side=RIGHT)

    def load_example(self, name: str = '') -> None:
        '''
            Loads named or selected script from discovered examples.

            :param name: Optional script name; defaults to combobox selection.
            :exceptions: None.
        '''
        script_name: str = name if name else self._cbo_scripts.get()
        if script_name in self._script_paths:
            self._cbo_scripts.set(script_name)
            self._delegate.handle_load_script(self._script_paths[script_name])

    def handle_browse_file(self) -> None:
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
        if filepath:
            self._delegate.handle_load_script(filepath)
            self.update_idletasks()

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
