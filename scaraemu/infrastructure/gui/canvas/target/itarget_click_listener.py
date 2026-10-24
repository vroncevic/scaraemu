# -*- coding: UTF-8 -*-

'''
Module
    itarget_click_listener.py
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
    Interface protocol for canvas target coordinate click events.
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
class ITargetClickListener(Protocol):
    '''
        Interface protocol for planar XY and vertical Z interactive target clicks.

        It defines:

            :methods:
                | handle_xy_click - Processes click on planar XY canvas.
                | handle_z_click - Processes click on vertical Z canvas.
                | get_version - Returns protocol specification version.
    '''

    def handle_xy_click(self, x: float, y: float) -> bool:
        '''
            Processes click on planar XY canvas.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :return: True if target dispatched, False if rejected or unreachable.
            :exceptions: None.
        '''

    def handle_z_click(self, z: float) -> bool:
        '''
            Processes click on vertical Z canvas.

            :param z: Target Z in mm.
            :return: True if target dispatched, False if rejected or unreachable.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol specification version.

            :return: Semantic version string.
            :exceptions: None.
        '''
