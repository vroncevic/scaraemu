# -*- coding: UTF-8 -*-

'''
Module
    igui.py
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
    Defines interface for SCARA emulator graphical user interface.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGUI(Protocol):
    '''
        Interface for SCARA emulator GUI presenter.

        It defines:

            :methods:
                | is_initialized - Returns initialization status.
                | run - Starts the Tkinter main event loop.
    '''

    def is_initialized(self) -> bool:
        '''
            Returns initialization status.

            :return: True if GUI is initialized, False otherwise.
            :exceptions: None.
        '''
        ...

    def run(self) -> None:
        '''
            Starts the Tkinter main event loop.

            :exceptions: None.
        '''
        ...
