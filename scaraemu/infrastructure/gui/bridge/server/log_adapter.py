# -*- coding: UTF-8 -*-

'''
Module
    log_adapter.py
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
    Adapter bridging ILogListener to IServerLogListener protocol.
'''

from __future__ import annotations

from typing import Final

from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerLogAdapter:
    '''
        Adapts ILogListener to satisfy IServerLogListener protocol.

        It defines:

            :attributes:
                | _log_listener - Injected ILogListener instance.
            :methods:
                | __init__ - Initializes adapter with target log listener.
                | on_server_log - Forwards server log message to target log listener.
                | get_version - Returns adapter component version.
    '''

    _log_listener: ILogListener

    def __init__(self, log_listener: ILogListener) -> None:
        '''
            Initializes adapter with target log listener.

            :param log_listener: Injected ILogListener instance.
            :exceptions: None.
        '''
        self._log_listener: Final[ILogListener] = log_listener

    def on_server_log(self, message: str) -> None:
        '''
            Forwards server log message to target log listener.

            :param message: Log message text.
            :exceptions: None.
        '''
        tag: str = 'err' if ('❌' in message or 'Failed' in message) else 'host'
        self._log_listener.append_log(message, tag)

    def get_version(self) -> str:
        '''
            Returns adapter component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
