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
    Presentation adapter forwarding diagnostic logs to GUI layout console panel.
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


class LogAdapter:
    '''
        Presentation adapter dispatching diagnostic logs to dynamic layout console.

        It defines:

            :attributes:
                | _layout_builder - UI widget layout builder holding console reference.
            :methods:
                | __init__ - Initializes log adapter with layout builder reference.
                | append_log - Appends log entry to active console panel if present.
                | get_version - Returns adapter component version.
    '''

    _layout_builder: ILayoutBuilder

    def __init__(self, *, layout_builder: ILayoutBuilder) -> None:
        '''
            Initializes log adapter with layout builder reference.

            :param layout_builder: Injected GUI layout builder instance.
            :exceptions: None.
        '''
        self._layout_builder: Final[ILayoutBuilder] = layout_builder

    def append_log(self, message: str, tag: str) -> None:
        '''
            Appends log entry to active console panel if present.

            :param message: Diagnostic text line.
            :param tag: Log entry category tag.
            :exceptions: None.
        '''
        self._layout_builder.append_log(message, tag)

    def get_version(self) -> str:
        '''
            Returns adapter component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
