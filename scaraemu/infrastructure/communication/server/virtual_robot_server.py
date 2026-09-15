# -*- coding: UTF-8 -*-

'''
Module
    virtual_robot_server.py
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
    Implementation of IVirtualRobotServer simulating RP2040 firmware over TCP loopback.
'''

from __future__ import annotations

from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
    socket as Socket,
    timeout as SocketTimeout,
)
from threading import Event, Lock, Thread
from typing import Callable, Final

from scaraemu.core.service.simulation.iemulator_service import IEmulatorService
from scaraemu.infrastructure.communication.server.virtual_command_processor import (
    VirtualCommandProcessor,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualRobotServer:
    '''
        Virtual robot controller TCP server emulating RP2040 firmware execution.

        It defines:

            :attributes:
                | _processor - VirtualCommandProcessor ASCII command dispatcher.
                | _on_log - Optional log message consumer callback.
                | _server_socket - Listening socket handle.
                | _server_thread - Background socket listener thread.
                | _stop_event - Event signaling server shutdown.
                | _lock - Mutex protecting state mutations.
                | _port - Active bound listening port.
            :methods:
                | __init__ - Initializes virtual robot server.
                | start - Starts listening for external host connections.
                | stop - Terminates background server and closes client sockets.
                | is_running - Checks whether server is currently active.
                | get_port - Returns the active listening port number.
                | _server_loop - Background accept loop dispatching client sessions.
                | _handle_client - Manages reading lines and responding to connected client.
    '''

    _processor: Final[VirtualCommandProcessor]
    _on_log: Callable[[str], None] | None
    _server_socket: Socket | None
    _server_thread: Thread | None
    _stop_event: Final[Event]
    _lock: Final[Lock]
    _port: int

    def __init__(
        self,
        emulator: IEmulatorService,
        on_log: Callable[[str], None] | None = None,
    ) -> None:
        '''
            Initializes virtual robot server.

            :param emulator: SCARA emulator core service instance.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._processor = VirtualCommandProcessor(emulator=emulator)
        self._on_log = on_log
        self._server_socket = None
        self._server_thread = None
        self._stop_event = Event()
        self._lock = Lock()
        self._port = 0

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts listening for external host connections.

            :param host: Local IP bind address.
            :param port: TCP listening port number.
            :return: True if server started successfully, False otherwise.
            :exceptions: None.
        '''
        with self._lock:
            if self._server_socket is not None:
                return True

            try:
                srv: Socket = Socket(AF_INET, SOCK_STREAM)
                srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                srv.bind((host, port))
                srv.listen(1)
                srv.settimeout(0.5)
                self._server_socket = srv
                self._port = srv.getsockname()[1]
                self._stop_event.clear()
                self._processor.reset()
                self._server_thread = Thread(target=self._server_loop, daemon=True)
                self._server_thread.start()
                if self._on_log is not None:
                    self._on_log(f'✅ Virtual Robot Controller listening on {host}:{self._port}')
                return True
            except OSError as exc:
                if self._on_log is not None:
                    self._on_log(f'❌ Failed to start Virtual Robot Server: {exc}')
                return False

    def stop(self) -> None:
        '''
            Terminates background server and closes client sockets.

            :exceptions: None.
        '''
        with self._lock:
            self._stop_event.set()
            if self._server_socket is not None:
                try:
                    self._server_socket.close()
                except OSError:
                    pass
                self._server_socket = None
                self._port = 0
                if self._on_log is not None:
                    self._on_log('ℹ️ Virtual Robot Controller stopped.')

    def is_running(self) -> bool:
        '''
            Checks whether server is currently active.

            :return: True if listening, False otherwise.
            :exceptions: None.
        '''
        return self._server_socket is not None and not self._stop_event.is_set()

    def get_port(self) -> int:
        '''
            Returns the active listening port number.

            :return: Port integer.
            :exceptions: None.
        '''
        return self._port

    def _server_loop(self) -> None:
        '''
            Background accept loop dispatching client sessions.

            :exceptions: None.
        '''
        while not self._stop_event.is_set():
            try:
                if self._server_socket is None:
                    break
                client_sock, client_addr = self._server_socket.accept()
                if self._on_log is not None:
                    self._on_log(f'🔗 Digital Twin client connected from {client_addr[0]}:{client_addr[1]}')
                self._handle_client(client_sock=client_sock)
            except SocketTimeout:
                continue
            except OSError:
                break

    def _handle_client(self, *, client_sock: Socket) -> None:
        '''
            Manages reading lines and responding to connected CAM client.

            :param client_sock: Connected client socket.
            :exceptions: None.
        '''
        client_sock.settimeout(0.5)
        buffer: str = ''
        try:
            while not self._stop_event.is_set():
                try:
                    data: bytes = client_sock.recv(1024)
                    if not data:
                        break
                    buffer += data.decode('utf-8', errors='replace')
                    while '\n' in buffer:
                        line: str
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line:
                            responses: list[str] = self._processor.process_command(cmd=line)
                            for resp in responses:
                                client_sock.sendall((resp + '\n').encode('utf-8'))
                except SocketTimeout:
                    continue
        except OSError:
            pass
        finally:
            try:
                client_sock.close()
            except OSError:
                pass
            if self._on_log is not None:
                self._on_log('🔌 Digital Twin client disconnected.')
