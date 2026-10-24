# -*- coding: UTF-8 -*-

'''
Module
    imanager.py
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
    Abstract interface protocol for virtual robot server lifecycle manager.
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
class IVirtualServerManager(Protocol):
    '''
        Structural protocol defining virtual robot server lifecycle management.

        It defines:

            :methods:
                | is_running - Checks whether the virtual robot server is running.
                | toggle - Starts or stops the background TCP server on given port.
                | stop - Stops the virtual robot server.
                | get_version - Returns interface version string.
    '''

    def is_running(self) -> bool:
        '''
            Checks whether the virtual robot server is actively running.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''

    def toggle(self, port: int) -> bool:
        '''
            Starts or stops the background TCP server on given port.

            :param port: Listening TCP port number.
            :return: True if started, False if stopped or failed.
            :exceptions: None.
        '''

    def stop(self) -> None:
        '''
            Stops the virtual robot server if active.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
