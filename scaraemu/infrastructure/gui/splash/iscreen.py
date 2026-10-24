# -*- coding: UTF-8 -*-

'''
Module
    iscreen.py
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
    Defines abstract interface ISplashScreen for startup splash screen presentation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISplashScreen(Protocol):
    '''
        Interface for desktop application startup splash screen.

        It defines:

            :methods:
                | set_progress - Updates loading progress percentage and status message.
                | get_progress - Retrieves current progress percentage and status text.
                | close - Dismisses and destroys the splash screen window.
                | get_version - Returns splash screen component version string.
    '''

    def set_progress(self, progress: int, status: str) -> None:
        '''
            Updates loading progress percentage and status message.

            :param progress: Integer percentage value between 0 and 100.
            :param status: Descriptive status message string.
            :exceptions: None.
        '''

    def get_progress(self) -> tuple[int, str]:
        '''
            Retrieves current progress percentage and status text.

            :return: Tuple of progress percentage integer and status text.
            :exceptions: None.
        '''

    def close(self) -> None:
        '''
            Dismisses and destroys the splash screen window.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns splash screen component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
