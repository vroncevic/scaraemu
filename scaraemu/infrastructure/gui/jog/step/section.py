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
    GUI subcomponent for selecting manual jog step resolution in millimeters.
'''

from __future__ import annotations

from tkinter import DoubleVar, Frame, Label, LEFT, Radiobutton, Widget

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogStepSection(Frame):
    '''
        Subcomponent containing radio buttons for selecting active jog step size.

        It defines:

            :attributes:
                | _step_var - Tkinter DoubleVar tracking active step distance in mm.
            :methods:
                | __init__ - Initializes the step selection radio buttons.
                | get_step - Reads and returns active step size in mm.
                | get_version - Returns component version string.
    '''

    _step_var: DoubleVar

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes the step selection radio buttons.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        lbl_step: Label = Label(
            self,
            text='Step:',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9),
        )
        lbl_step.pack(side=LEFT, padx=(0, 5))

        self._step_var = DoubleVar(value=5.0)
        step_options: tuple[float, ...] = (1.0, 5.0, 10.0, 25.0)

        for step in step_options:
            rb: Radiobutton = Radiobutton(
                self,
                text=f'{step:.0f}mm',
                value=step,
                variable=self._step_var,
                bg=ThemeManager.BG_PANEL,
                fg=ThemeManager.TEXT_PRIMARY,
                selectcolor=ThemeManager.BG_CANVAS,
                activebackground=ThemeManager.BG_PANEL,
                font=(ThemeManager.FONT_FAMILY, 8),
            )
            rb.pack(side=LEFT, padx=2)

    def get_step(self) -> float:
        '''
            Reads and returns active step size in mm.

            :return: Step size in millimeters.
            :exceptions: None.
        '''
        return float(self._step_var.get())

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
