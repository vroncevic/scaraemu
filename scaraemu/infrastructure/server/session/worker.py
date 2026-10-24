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
    Connected client session worker managing packet reception and responses.
'''

from __future__ import annotations

from socket import socket as Socket, timeout as SocketTimeout
from threading import Event
from typing import Final

from scaraemu.infrastructure.server.dispatcher.idispatcher import IServerFrameDispatcher
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.session.ioutbound_queue import IOutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ClientSessionWorker:
    '''
        Reads incoming requests from client socket and streams responses until disconnection.

        It defines:

            :attributes:
                | _dispatcher - Frame and command processing dispatcher.
                | _log_listener - Server event log listener.
                | _outbound_queue - Outbound frame queue for asynchronous event streaming.
            :methods:
                | __init__ - Initializes session worker with dispatcher, log listener, and outbound queue.
                | handle_client - Runs packet reception and response streaming loop.
                | get_version - Returns worker component version.
    '''

    _dispatcher: IServerFrameDispatcher
    _log_listener: IServerLogListener
    _outbound_queue: IOutboundFrameQueue

    def __init__(
        self,
        *,
        dispatcher: IServerFrameDispatcher,
        log_listener: IServerLogListener,
        outbound_queue: IOutboundFrameQueue,
    ) -> None:
        '''
            Initializes session worker with dispatcher, log listener, and outbound queue.

            :param dispatcher: Injected IServerFrameDispatcher instance.
            :param log_listener: Injected IServerLogListener instance.
            :param outbound_queue: Injected IOutboundFrameQueue instance.
            :exceptions: None.
        '''
        self._dispatcher: Final[IServerFrameDispatcher] = dispatcher
        self._log_listener: Final[IServerLogListener] = log_listener
        self._outbound_queue: Final[IOutboundFrameQueue] = outbound_queue

    def handle_client(self, *, client_sock: Socket, stop_event: Event) -> None:
        '''
            Runs packet reception and response streaming loop until client disconnects.

            :param client_sock: Connected client TCP socket.
            :param stop_event: Server shutdown signaling event.
            :exceptions: None.
        '''
        client_sock.settimeout(0.05)
        self._dispatcher.reset()
        self._outbound_queue.clear()

        try:
            while not stop_event.is_set():
                for pending_frame in self._outbound_queue.pop_all():
                    client_sock.sendall(pending_frame)

                try:
                    data: bytes = client_sock.recv(1024)

                    if not data:
                        break

                    resp_bytes: tuple[bytes, ...] = (
                        self._dispatcher.dispatch_binary(data)
                    )

                    for resp in resp_bytes:
                        client_sock.sendall(resp)

                except SocketTimeout:
                    continue

                for pending_frame in self._outbound_queue.pop_all():
                    client_sock.sendall(pending_frame)

        except OSError:
            pass

        finally:
            self._outbound_queue.clear()
            try:
                client_sock.close()

            except OSError:
                pass

            self._log_listener.on_server_log('🔌 Digital Twin client disconnected.')

    def get_version(self) -> str:
        '''
            Returns worker component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
