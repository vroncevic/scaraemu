# -*- coding: UTF-8 -*-

'''
Module
    holder.py
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
    Thread-safe dynamic holder delegating server log callbacks to registered listener.
'''

from __future__ import annotations

from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerLogListenerHolder:
    '''
        Dynamic listener holder delegating server log events to registered sink.

        It defines:

            :attributes:
                | _has_listener - Flag indicating if listener sink is registered.
                | _listener - Active server log listener sink.
            :methods:
                | __init__ - Initializes holder with unassigned listener state.
                | set_listener - Updates active server log listener sink.
                | on_server_log - Forwards log message to active listener if present.
                | get_version - Returns holder version string.
    '''

    _has_listener: bool
    _listener: IServerLogListener

    def __init__(self) -> None:
        '''
            Initializes holder with unassigned listener state.

            :exceptions: None.
        '''
        self._has_listener = False

    def set_listener(self, listener: IServerLogListener) -> None:
        '''
            Updates active server log listener sink.

            :param listener: Injected IServerLogListener instance.
            :exceptions: None.
        '''
        self._listener = listener
        self._has_listener = True

    def on_server_log(self, message: str) -> None:
        '''
            Forwards log message to active listener if present.

            :param message: Server log message string.
            :exceptions: None.
        '''
        if self._has_listener:
            self._listener.on_server_log(message)

    def get_version(self) -> str:
        '''
            Returns holder version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
