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
    Action coordinator handling toolbar serial bar user interactions.
'''

from __future__ import annotations

from typing import Final

from scaracom.transport.preference.preference import SerialPreference
from scaracom.transport.preference.irepository import ISerialPreferenceRepository

from scaraemu.infrastructure.connection.coordinator.icoordinator import IConnectionCoordinator
from scaraemu.infrastructure.preferences.server.irepository import IServerPreferenceRepository
from scaraemu.infrastructure.server.manager.imanager import IVirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ActionCoordinator:
    '''
        Coordinates serial connection toggling and virtual robot server startup.

        It defines:

            :attributes:
                | DEFAULT_SERVER_PORT - Default TCP port used for virtual robot server.
                | _connection_port - Hardware communication connection port.
                | _server_manager - Virtual robot TCP server lifecycle manager.
                | _serial_preferences - Serial connection preference persistence repository.
                | _server_preferences - Virtual server network preference persistence repository.
            :methods:
                | __init__ - Initializes action coordinator.
                | handle_connect_toggle - Toggles connection to serial hardware device.
                | handle_server_toggle - Starts or stops the background TCP virtual robot server.
                | get_version - Returns coordinator component version.
    '''

    DEFAULT_SERVER_PORT: Final[int] = 8888

    _connection_port: IConnectionCoordinator
    _server_manager: IVirtualServerManager
    _serial_preferences: ISerialPreferenceRepository
    _server_preferences: IServerPreferenceRepository

    def __init__(
        self,
        *,
        connection_port: IConnectionCoordinator,
        server_manager: IVirtualServerManager,
        serial_preferences: ISerialPreferenceRepository,
        server_preferences: IServerPreferenceRepository,
    ) -> None:
        '''
            Initializes action coordinator with connection port, server manager, and preferences.

            :param connection_port: Hardware communication connection port.
            :param server_manager: Virtual robot TCP server manager.
            :param serial_preferences: Serial connection preference persistence repository.
            :param server_preferences: Virtual server network preference persistence repository.
            :exceptions: None.
        '''
        self._connection_port: Final[IConnectionCoordinator] = connection_port
        self._server_manager: Final[IVirtualServerManager] = server_manager
        self._serial_preferences: Final[ISerialPreferenceRepository] = serial_preferences
        self._server_preferences: Final[IServerPreferenceRepository] = server_preferences

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Toggles connection to serial hardware device.

            :param port: Selected serial port device path.
            :param baudrate: Transmission baud rate.
            :exceptions: None.
        '''
        if port and port != 'Virtual / None':
            self._serial_preferences.save_preference(
                SerialPreference(port=port, baud=baudrate)
            )

        self._connection_port.handle_connect_toggle(port, baudrate)

    def handle_server_toggle(self) -> None:
        '''
            Starts or stops the background TCP virtual robot server.

            :exceptions: None.
        '''
        port: int = self.DEFAULT_SERVER_PORT

        if self._server_preferences.has_preference():
            try:
                port = self._server_preferences.load_preference().port

            except Exception:
                port = self.DEFAULT_SERVER_PORT

        self._server_manager.toggle(port=port)

    def get_version(self) -> str:
        '''
            Returns coordinator component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
