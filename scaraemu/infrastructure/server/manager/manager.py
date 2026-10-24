# -*- coding: UTF-8 -*-

'''
Module
    manager.py
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

from typing import Final

from scaraemu.infrastructure.server.iserver import IVirtualManipulatorServer
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.manager.ilistener import IServerStateListener

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
        Manages the lifecycle and state of the TCP VirtualManipulatorServer for the GUI.

        It defines:

            :attributes:
                | _server - Injected virtual robot TCP server instance.
                | _log_listener - Logging sink for host diagnostics.
                | _state_listener - Listener for UI server state updates.
            :methods:
                | is_running - Checks whether the virtual server is actively running.
                | stop - Stops the server if running.
                | toggle - Starts or stops the background TCP server.
                | get_version - Returns manager component version.
    '''

    _server: IVirtualManipulatorServer
    _log_listener: IServerLogListener
    _state_listener: IServerStateListener

    def __init__(
        self,
        *,
        server: IVirtualManipulatorServer,
        log_listener: IServerLogListener,
        state_listener: IServerStateListener,
    ) -> None:
        '''
            Initializes virtual server manager with injected server and listeners.

            :param server: Injected IVirtualManipulatorServer instance.
            :param log_listener: Logging listener for host diagnostics.
            :param state_listener: Listener for server lifecycle state changes.
            :exceptions: None.
        '''
        self._server: Final[IVirtualManipulatorServer] = server
        self._log_listener: Final[IServerLogListener] = log_listener
        self._state_listener: Final[IServerStateListener] = state_listener

    def is_running(self) -> bool:
        '''
            Checks whether the virtual server is actively running.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''
        return self._server.is_running()

    def stop(self) -> None:
        '''
            Stops the virtual robot TCP server if active.

            :exceptions: None.
        '''
        if self._server.is_running():
            self._server.stop()
            self._state_listener.on_server_state(False, 0)
            self._log_listener.on_server_log(
                '[HOST]: Virtual Robot Server stopped.'
            )

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

        success: bool = self._server.start(port=port)
        bound_port: int = port if success else 0
        self._state_listener.on_server_state(success, bound_port)

        if success:
            self._log_listener.on_server_log(
                f'[HOST]: Virtual Robot Server listening on 127.0.0.1:{port}'
            )
        else:
            self._log_listener.on_server_log(
                f'❌ [HOST]: Failed to start Virtual Robot Server on port {port}'
            )

        return success

    def get_version(self) -> str:
        '''
            Returns manager component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
