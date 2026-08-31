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

import tkinter as tk
from typing import Callable

from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoPanel(tk.LabelFrame):
    '''
        Panel for selecting and triggering predefined autonomous demonstration trajectories.

        It defines:

            :attributes:
                | _lbl_queue - Motion queue depth label.
                | _on_demo_select - Callback receiving selected trajectory preset name.
                | _on_clear_queue - Callback for clearing motion queue and path trail.
            :methods:
                | __init__ - Initializes demo buttons and queue status display.
                | update_queue_depth - Updates queue count display.
    '''

    _lbl_queue: tk.Label
    _on_demo_select: Callable[[str], None] | None
    _on_clear_queue: Callable[[], None] | None

    def __init__(
        self,
        parent: tk.Widget,
        on_demo_select: Callable[[str], None] | None = None,
        on_clear_queue: Callable[[], None] | None = None
    ) -> None:
        '''
            Initializes demo buttons and queue status display.

            :param parent: Parent Tkinter widget.
            :param on_demo_select: Callback when demo preset button is clicked.
            :param on_clear_queue: Callback when clear queue button is clicked.
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

        grid_btn: tk.Frame = tk.Frame(self, bg=ThemeManager.BG_PANEL)
        grid_btn.pack(fill=tk.X, pady=(0, 8))

        self._make_btn(grid_btn, 'Circle', 0, 0, lambda: self._trigger('circle'))
        self._make_btn(grid_btn, 'Square', 0, 1, lambda: self._trigger('square'))
        self._make_btn(grid_btn, '5-Star', 1, 0, lambda: self._trigger('star'))
        self._make_btn(grid_btn, '3D Helix', 1, 1, lambda: self._trigger('helix'))

        q_frame: tk.Frame = tk.Frame(self, bg=ThemeManager.BG_PANEL)
        q_frame.pack(fill=tk.X, pady=(4, 0))

        self._lbl_queue = tk.Label(
            q_frame,
            text='Queue: 0 pts',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 8)
        )
        self._lbl_queue.pack(side=tk.LEFT)

        btn_clear: tk.Button = tk.Button(
            q_frame,
            text='Clear Queue',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=tk.FLAT,
            command=self._clear
        )
        btn_clear.pack(side=tk.RIGHT)

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
        color = ThemeManager.ACCENT_GREEN if count == 0 else ThemeManager.ACCENT_ORANGE
        self._lbl_queue.config(text=f'Queue: {count} pts', fg=color)

    def _make_btn(self, parent: tk.Frame, text: str, r: int, c: int, cmd: Callable[[], None]) -> tk.Button:
        '''
            Helper creating styled preset button.

            :param parent: Parent frame container.
            :param text: Button text.
            :param r: Grid row.
            :param c: Grid column.
            :param cmd: Click handler.
            :return: The button instance.
            :exceptions: None.
        '''
        b = tk.Button(
            parent,
            text=text,
            bg='#45475a',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=tk.FLAT,
            command=cmd
        )
        b.grid(row=r, column=c, sticky='ew', padx=2, pady=2)
        parent.grid_columnconfigure(c, weight=1)
        return b
