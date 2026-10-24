# -*- coding: UTF-8 -*-

'''
Module
    configurator.py
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
    Dedicated window configurator managing OS window options, title, and geometry.
'''

from __future__ import annotations

from tkinter import TclError, Tk

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WindowConfigurator:
    '''
        Configures root window dimensions, minimum sizes, and zoom state across platforms.

        It defines:

            :methods:
                | setup_window - Configures root window title, geometry, and styling.
                | maximize_window - Maximizes root window.
                | get_version - Returns configurator version string.
    '''

    def setup_window(self, root: Tk) -> None:
        '''
            Configures root window title, geometry, and styles.

            :param root: Tkinter root window.
            :exceptions: None.
        '''
        root.withdraw()
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

    def get_version(self) -> str:
        '''
            Returns configurator version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
