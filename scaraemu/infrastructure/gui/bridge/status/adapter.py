# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Presentation adapter forwarding hardware connection state updates to toolbar.
'''

from __future__ import annotations

from typing import Final

from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatusAdapter:
    '''
        Presentation adapter dispatching connection status changes to top serial toolbar.

        It defines:

            :attributes:
                | _layout_builder - UI widget layout builder holding serial bar reference.
            :methods:
                | __init__ - Initializes connection status adapter with layout builder reference.
                | set_connected_state - Updates connection button and badge in serial bar.
                | get_version - Returns adapter component version.
    '''

    _layout_builder: ILayoutBuilder

    def __init__(self, *, layout_builder: ILayoutBuilder) -> None:
        '''
            Initializes connection status adapter with layout builder reference.

            :param layout_builder: Injected GUI layout builder instance.
            :exceptions: None.
        '''
        self._layout_builder: Final[ILayoutBuilder] = layout_builder

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates connection button and badge in serial bar if widget is active.

            :param connected: True if connected to hardware, False otherwise.
            :exceptions: None.
        '''
        self._layout_builder.set_connected_state(connected)

    def get_version(self) -> str:
        '''
            Returns adapter component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
