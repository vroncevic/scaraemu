# -*- coding: UTF-8 -*-

'''
Module
    worker.py
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
    Dedicated background accept worker listening for and dispatching client connections.
'''

from __future__ import annotations

from socket import socket as Socket, timeout as SocketTimeout
from threading import Event
from typing import Final

from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.session.iworker import IClientSessionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerAcceptWorker:
    '''
        Background thread worker accepting incoming client socket connections.

        It defines:

            :attributes:
                | _session_worker - Injected client session handler.
                | _log_listener - Injected server event log listener.
            :methods:
                | __init__ - Initializes accept worker with worker and listeners.
                | run - Executes accept loop until stop event is signaled.
                | get_version - Returns worker component version.
    '''

    _session_worker: IClientSessionWorker
    _log_listener: IServerLogListener

    def __init__(
        self,
        *,
        session_worker: IClientSessionWorker,
        log_listener: IServerLogListener,
    ) -> None:
        '''
            Initializes accept worker with session worker and log listener.

            :param session_worker: Injected IClientSessionWorker instance.
            :param log_listener: Injected IServerLogListener instance.
            :exceptions: None.
        '''
        self._session_worker: Final[IClientSessionWorker] = session_worker
        self._log_listener: Final[IServerLogListener] = log_listener

    def run(self, *, server_socket: Socket, stop_event: Event) -> None:
        '''
            Executes accept loop until stop event is signaled.

            :param server_socket: Listening TCP server socket.
            :param stop_event: Server shutdown signaling event.
            :exceptions: None.
        '''
        while not stop_event.is_set():
            try:
                client_sock, client_addr = server_socket.accept()
                self._log_listener.on_server_log(
                    f'🔗 Digital Twin client connected from {client_addr[0]}:{client_addr[1]}'
                )
                self._session_worker.handle_client(
                    client_sock=client_sock,
                    stop_event=stop_event,
                )

            except SocketTimeout:
                continue

            except OSError:
                break

    def get_version(self) -> str:
        '''
            Returns worker component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
