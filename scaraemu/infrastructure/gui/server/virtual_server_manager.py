# -*- coding: UTF-8 -*-

'''
Module
    virtual_server_manager.py
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
    Virtual robot server lifecycle manager for GUI presentation layer.
'''

from __future__ import annotations

from typing import Any, Callable

from scaraemu.infrastructure.communication.server.virtual_robot_server import (
    VirtualRobotServer,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualServerManager:
    '''
        Manages the lifecycle and state of the TCP VirtualRobotServer for the GUI.

        It defines:

            :attributes:
                | _emulator - SCARA emulator model or service.
                | _log_host - Logging callback for host diagnostics.
                | _state_callback - Optional UI state update callback.
                | _virtual_server - Virtual robot TCP server instance.
            :methods:
                | __init__ - Initializes virtual server manager with dependencies.
                | is_running - Checks whether the virtual server is actively running.
                | toggle - Starts or stops the background TCP server.
                | stop - Stops the server if running.
    '''

    _emulator: Any
    _log_host: Callable[[str, str], None]
    _state_callback: Callable[[bool, int | None], None] | None
    _virtual_server: VirtualRobotServer | None

    def __init__(
        self,
        emulator: Any,
        log_host: Callable[[str, str], None],
        state_callback: Callable[[bool, int | None], None] | None = None
    ) -> None:
        '''
            Initializes virtual server manager with dependencies.

            :param emulator: SCARA emulator model or service.
            :param log_host: Logging callback for host diagnostics.
            :param state_callback: Optional UI state update callback.
            :exceptions: None.
        '''
        self._emulator = emulator
        self._log_host = log_host
        self._state_callback = state_callback
        self._virtual_server = None

    def is_running(self) -> bool:
        '''
            Checks whether the virtual server is actively running.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''
        return self._virtual_server is not None and self._virtual_server.is_running()

    def stop(self) -> None:
        '''
            Stops the virtual robot TCP server if active.

            :exceptions: None.
        '''
        if self._virtual_server is not None and self._virtual_server.is_running():
            self._virtual_server.stop()
            if self._state_callback is not None:
                self._state_callback(False, None)
            self._log_host('[HOST]: Virtual Robot Server stopped.', 'info')

    def toggle(self, port: int = 8888) -> bool:
        '''
            Toggles virtual robot TCP server state between running and stopped.

            :param port: TCP listening port.
            :return: True if started, False if stopped or failed.
            :exceptions: None.
        '''
        if self.is_running():
            self.stop()
            return False

        if self._virtual_server is None:
            self._virtual_server = VirtualRobotServer(
                emulator=self._emulator,
                on_log=lambda msg: self._log_host(msg, 'info')
            )

        success: bool = self._virtual_server.start(port=port)
        if self._state_callback is not None:
            self._state_callback(success, port if success else None)

        if success:
            self._log_host(
                f'[HOST]: Virtual Robot Server listening on 127.0.0.1:{port}',
                'info'
            )
        else:
            self._log_host(
                f'[HOST]: Failed to start Virtual Robot Server on port {port}',
                'err'
            )
        return success
