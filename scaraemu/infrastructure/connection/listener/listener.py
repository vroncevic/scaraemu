# -*- coding: UTF-8 -*-

'''
Module
    listener.py
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
    Transport listener adapter forwarding transport stream events to response handler.
'''

from __future__ import annotations

from typing import Final

from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler
from scaraemu.infrastructure.connection.listener.dependencies import ListenerDependencies
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionTransportListener:
    '''
        Transport listener adapter forwarding transport stream events to response handler.

        It defines:

            :attributes:
                | _handler - Inbound packet and binary response handler.
                | _synchronizer - Bridge status and telemetry synchronizer.
            :methods:
                | __init__ - Initializes connection listener with dependency bundle.
                | on_bytes_received - Handles received raw byte chunk.
                | on_log_emitted - Handles generated transport log entry.
                | get_version - Returns listener adapter component version.
    '''

    _handler: IResponseHandler
    _synchronizer: IBridgeSynchronizer

    def __init__(self, dependencies: ListenerDependencies) -> None:
        '''
            Initializes connection listener with dependency bundle.

            :param dependencies: Encapsulated listener dependencies bundle.
            :exceptions: None.
        '''
        self._handler: Final[IResponseHandler] = dependencies.handler
        self._synchronizer: Final[IBridgeSynchronizer] = dependencies.synchronizer

    def on_bytes_received(self, data: bytes) -> None:
        '''
            Handles received raw byte chunk.

            :param data: Inbound bytes payload.
            :exceptions: None.
        '''
        self._handler.on_bytes(data)

    def on_log_emitted(self, message: str, is_tx: bool) -> None:
        '''
            Handles generated transport log entry.

            :param message: Log message string.
            :param is_tx: True if transmission log, False if reception log.
            :exceptions: None.
        '''
        _ = is_tx

        if '[HOST]: Connection lost' in message:
            self._synchronizer.on_state_change(False)

        self._handler.on_log(message)

    def get_version(self) -> str:
        '''
            Returns listener adapter component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
