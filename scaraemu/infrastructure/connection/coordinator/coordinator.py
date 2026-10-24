# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Hardware connection coordinator managing serial connect and disconnect flows.
'''

from __future__ import annotations

from typing import Final

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.connection.coordinator.dependencies import CoordinatorDependencies
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionCoordinator:
    '''
        Hardware connection coordinator managing serial connect and disconnect flows.

        It defines:

            :attributes:
                | _connection - Injected hardware connection coordinator.
                | _listener - Hardware bridge status and telemetry synchronizer.
                | _streamer - Outbound trajectory queue streamer.
                | _command_dispatcher - Command dispatcher for initial status queries.
            :methods:
                | __init__ - Initializes connection coordinator with dependency bundle.
                | handle_connect_toggle - Toggles connection to serial hardware device.
                | get_version - Returns connection coordinator component version.
    '''

    _connection: IConnectionCoordinator
    _listener: IBridgeSynchronizer
    _streamer: IQueueStreamer
    _command_dispatcher: ICommandDispatcher

    def __init__(
        self, dependencies: CoordinatorDependencies
    ) -> None:
        '''
            Initializes connection coordinator with dependency bundle.

            :param dependencies: Encapsulated connection coordinator dependency bundle.
            :exceptions: None.
        '''
        self._connection: Final[IConnectionCoordinator] = dependencies.connection
        self._listener: Final[IBridgeSynchronizer] = dependencies.listener
        self._streamer: Final[IQueueStreamer] = dependencies.streamer
        self._command_dispatcher: Final[ICommandDispatcher] = dependencies.command_dispatcher

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Toggles connection to serial hardware device.

            :param port: Target serial port path.
            :param baudrate: Transmission baud rate.
            :exceptions: None.
        '''
        if self._connection.is_connected():
            self._connection.disconnect()
            self._streamer.clear()
            self._listener.on_state_change(False)
        else:
            success: bool = self._connection.connect(port, baudrate)
            self._listener.on_state_change(success)

            if success:
                self._streamer.clear()
                self._command_dispatcher.send_command(MessageId.CMD_GET_STATUS)

    def get_version(self) -> str:
        '''
            Returns connection coordinator component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
