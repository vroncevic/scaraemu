# -*- coding: UTF-8 -*-

'''
Module
    server.py
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
    Implementation of IVirtualManipulatorServer simulating RP2040 firmware over TCP loopback.
'''

from __future__ import annotations

from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
    socket as Socket,
)
from threading import Event, Lock, Thread
from typing import Final

from scaraemu.infrastructure.server.accept.iworker import IServerAcceptWorker
from scaraemu.infrastructure.server.dispatcher.idispatcher import IServerFrameDispatcher
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualManipulatorServer:
    '''
        Virtual robot controller TCP server emulating RP2040 firmware execution.

        It defines:

            :attributes:
                | _accept_worker - Injected accept worker listening for client connections.
                | _dispatcher - Injected server frame and command dispatcher.
                | _log_listener - Injected server event log listener.
                | _stop_event - Event signaling server shutdown.
                | _lock - Mutex protecting server lifecycle state transitions.
                | _is_running - Flag indicating whether server is actively listening.
                | _server_thread - Background thread executing accept worker.
                | _server_socket - Active listening TCP server socket.
            :methods:
                | __init__ - Initializes virtual robot server with accept worker and dispatcher.
                | start - Starts listening for external host connections.
                | stop - Terminates background server and closes client sockets.
                | is_running - Checks whether server is currently active.
                | get_version - Returns server component version string.
    '''

    _accept_worker: IServerAcceptWorker
    _dispatcher: IServerFrameDispatcher
    _log_listener: IServerLogListener
    _stop_event: Event
    _lock: Lock
    _is_running: bool
    _server_thread: Thread
    _server_socket: Socket

    def __init__(
        self,
        *,
        accept_worker: IServerAcceptWorker,
        dispatcher: IServerFrameDispatcher,
        log_listener: IServerLogListener,
    ) -> None:
        '''
            Initializes virtual robot server with accept worker, dispatcher, and log listener.

            :param accept_worker: Injected IServerAcceptWorker instance.
            :param dispatcher: Injected IServerFrameDispatcher instance.
            :param log_listener: Injected IServerLogListener instance.
            :exceptions: None.
        '''
        self._accept_worker: Final[IServerAcceptWorker] = accept_worker
        self._dispatcher: Final[IServerFrameDispatcher] = dispatcher
        self._log_listener: Final[IServerLogListener] = log_listener
        self._stop_event: Final[Event] = Event()
        self._lock: Final[Lock] = Lock()
        self._is_running = False
        self._server_thread = Thread(target=bool)
        self._server_socket = Socket()
        self._server_socket.close()

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts listening for external host connections.

            :param host: Local IP bind address.
            :param port: TCP listening port number.
            :return: True if server started successfully, False otherwise.
            :exceptions: None.
        '''
        with self._lock:
            if self._is_running:
                return True

            try:
                srv: Socket = Socket(AF_INET, SOCK_STREAM)
                srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                srv.bind((host, port))
                srv.listen(1)
                srv.settimeout(0.5)
                self._server_socket = srv
                bound_port: int = srv.getsockname()[1]
                self._is_running = True
                self._stop_event.clear()
                self._dispatcher.reset()

                self._server_thread = Thread(
                    target=self._accept_worker.run,
                    kwargs={
                        'server_socket': self._server_socket,
                        'stop_event': self._stop_event,
                    },
                    daemon=True,
                )
                self._server_thread.start()
                self._log_listener.on_server_log(
                    f'✅ Virtual Manipulator Server listening on {host}:{bound_port}'
                )
                return True

            except OSError as exc:
                try:
                    srv.close()

                except OSError:
                    pass
                self._log_listener.on_server_log(
                    f'❌ Failed to start Virtual Robot Server: {exc}'
                )

                return False

    def stop(self) -> None:
        '''
            Terminates background server and closes listening socket.

            :exceptions: None.
        '''
        with self._lock:
            self._stop_event.set()

            if self._is_running:
                try:
                    self._server_socket.close()

                except OSError:
                    pass

                self._is_running = False

                if self._server_thread.is_alive():
                    self._server_thread.join(timeout=0.5)

                self._log_listener.on_server_log('ℹ️ Virtual Robot Controller stopped.')

    def is_running(self) -> bool:
        '''
            Checks whether server is currently active.

            :return: True if listening, False otherwise.
            :exceptions: None.
        '''
        return self._is_running and not self._stop_event.is_set()

    def get_version(self) -> str:
        '''
            Returns server component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
