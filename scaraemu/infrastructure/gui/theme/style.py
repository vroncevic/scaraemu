# -*- coding: UTF-8 -*-

'''
Module
    style.py
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
    ttk Notebook theme and tab style configurator utility.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Style

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NotebookStyleConfigurator:
    '''
        Configures customized ttk theme and tab styles for Notebook widgets.

        It defines:

            :methods:
                | configure - Applies customized clam styling to ttk Notebook tabs.
                | get_version - Returns configurator version string.
    '''

    @classmethod
    def configure(cls, root: Tk) -> None:
        '''
            Applies customized clam styling to ttk Notebook tabs.

            :param root: Tkinter root window.
            :exceptions: None.
        '''
        style: Style = Style(root)
        style.theme_use('clam')
        style.configure('TNotebook', background=ThemeManager.BG_DARK, borderwidth=0)
        style.configure(
            'TNotebook.Tab',
            background=ThemeManager.BG_PANEL,
            foreground=ThemeManager.TEXT_SECONDARY,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padding=[12, 5],
            focuscolor=ThemeManager.BG_DARK,
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', ThemeManager.BG_CANVAS), ('active', ThemeManager.BG_PANEL)],
            foreground=[('selected', ThemeManager.ACCENT_CYAN), ('active', ThemeManager.TEXT_PRIMARY)],
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns configurator version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
