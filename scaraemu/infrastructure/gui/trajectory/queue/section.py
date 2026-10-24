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
    Trajectory queue depth visualization and flush action subcomponent.
'''

from __future__ import annotations

from tkinter import Button, FLAT, Frame, Label, LEFT, RIGHT, Widget
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryQueueSection(Frame):
    '''
        Subcomponent for monitoring motion queue depth and flushing pending steps.

        It defines:

            :attributes:
                | _lbl_queue - Label widget displaying active queue count.
                | _delegate - Action delegate receiving queue flush requests.
            :methods:
                | __init__ - Initializes queue depth label and clear button.
                | update_queue_depth - Updates displayed queue count and status color.
                | get_queue_text - Returns displayed queue text for status verification.
                | get_version - Returns component version string.
    '''

    _lbl_queue: Label
    _delegate: IQueueActionDelegate

    def __init__(self, parent: Widget, delegate: IQueueActionDelegate) -> None:
        '''
            Initializes queue depth label and action buttons.

            :param parent: Parent Tkinter widget container.
            :param delegate: Action delegate with queue and trail clear methods.
            :exceptions: None.
        '''
        super().__init__(parent, bg=ThemeManager.BG_PANEL)
        self._delegate: Final[IQueueActionDelegate] = delegate

        self._lbl_queue: Final[Label] = Label(
            self,
            text='Queue: 0 pts',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_MONO, 8),
        )
        self._lbl_queue.pack(side=LEFT)

        btn_clear_trail: Button = Button(
            self,
            text='Clear Trail',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=delegate.handle_clear_trail,
        )
        btn_clear_trail.pack(side=RIGHT)

        btn_clear_queue: Button = Button(
            self,
            text='Clear Queue',
            bg='#313244',
            fg=ThemeManager.TEXT_PRIMARY,
            font=(ThemeManager.FONT_FAMILY, 8),
            relief=FLAT,
            command=delegate.handle_clear_queue,
        )
        btn_clear_queue.pack(side=RIGHT, padx=(0, 4))

    def update_queue_depth(self, count: int) -> None:
        '''
            Updates displayed queue count and status color.

            :param count: Current queue depth count.
            :exceptions: None.
        '''
        if not self.winfo_exists():
            return

        color: str = ThemeManager.ACCENT_GREEN if count == 0 else ThemeManager.ACCENT_ORANGE
        self._lbl_queue.config(text=f'Queue: {count} pts', fg=color)

    def get_queue_text(self) -> str:
        '''
            Returns displayed queue text for status verification.

            :return: Formatted queue text string.
            :exceptions: None.
        '''
        return str(self._lbl_queue.cget('text'))

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
