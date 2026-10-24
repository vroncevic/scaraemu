# -*- coding: UTF-8 -*-

'''
Module
    iviewport.py
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
    Interface protocol for canvas viewport dimension and scale providers.
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
class IViewport(Protocol):
    '''
        Structural interface protocol for canvas viewport metrics and scale.

        It defines:

            :methods:
                | update_size - Updates canvas dimensions upon window resize.
                | get_scale - Returns active scale multiplier.
                | get_dimensions - Returns current pixel dimensions.
                | get_version - Returns viewport interface version string.
    '''

    def update_size(self, width: int, height: int) -> None:
        '''
            Updates canvas dimensions upon window resize and recalculates scaling.

            :param width: New width in pixels.
            :param height: New height in pixels.
            :exceptions: None.
        '''

    def get_scale(self) -> float:
        '''
            Returns active scale multiplier.

            :return: Scale factor.
            :exceptions: None.
        '''

    def get_dimensions(self) -> tuple[float, float]:
        '''
            Returns current pixel dimensions (width, height).

            :return: Tuple of (width, height).
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns viewport interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
