# -*- coding: UTF-8 -*-

'''
Module
    tcp_transport.py
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
    TCP socket transport implementing ITransport protocol.
'''

from __future__ import annotations

import socket
from threading import Lock, Event, Thread
from time import sleep
from typing import Callable, Final

from scaraemu.infrastructure.communication.transport.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpTransport(ITransport):
    '''
        TCP socket transport for network-connected SCARA robots.

        It defines:

            :attributes:
                | _socket - Active socket object.
                | _lock - Mutex protecting socket send operations.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Background socket polling thread.
                | _on_line - Callback invoked when a complete line is received.
                | _on_log - Callback for communication logging.
            :methods:
                | __init__ - Initializes transport handle and sync primitives.
                | is_connected - Checks if socket is connected.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | connect - Establishes TCP connection to host:port.
                | disconnect - Closes TCP connection and stops reader thread.
                | write_line - Sends string line payload over TCP socket.
    '''

    _socket: socket.socket | None
    _lock: Lock
    _stop_event: Event
    _reader_thread: Thread | None
    _on_line: Callable[[str], None] | None
    _on_log: Callable[[str], None] | None

    def __init__(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str], None] | None = None
    ) -> None:
        '''
            Initializes TCP transport.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._socket = None
        self._lock: Final[Lock] = Lock()
        self._stop_event: Final[Event] = Event()
        self._reader_thread = None
        self._on_line = on_line
        self._on_log = on_log

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str], None] | None = None
    ) -> None:
        '''
            Registers packet reception and connection logging hooks.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._on_line = on_line
        self._on_log = on_log

    def is_connected(self) -> bool:
        '''
            Checks if socket is connected.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._socket is not None

    def connect(self, port: str, baudrate: int = 8080) -> bool:
        '''
            Establishes TCP connection where port parameter represents host IP and baudrate is port number.

            :param port: Host IP address (e.g. '192.168.1.100').
            :param baudrate: Port number (e.g. 8080).
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        try:
            sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((port, baudrate))
            sock.settimeout(0.1)
            self._socket = sock
            self._stop_event.clear()
            self._reader_thread = Thread(target=self._reader_loop, daemon=True)
            self._reader_thread.start()

            if self._on_log:
                self._on_log(f'[HOST]: Connected to TCP {port}:{baudrate}')

            return True
        except (OSError, Exception) as exc:
            if self._on_log:
                self._on_log(f'[ERR]: TCP connection failed: {exc}')
            self.disconnect()
            return False

    def disconnect(self) -> None:
        '''
            Closes TCP connection and stops reader thread.

            :exceptions: None.
        '''
        self._stop_event.set()
        if self._socket:
            try:
                self._socket.close()
            except OSError:
                pass
            self._socket = None

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=0.2)
            self._reader_thread = None

        if self._on_log:
            self._on_log('[HOST]: Disconnected from TCP socket')

    def write_line(self, data: str) -> bool:
        '''
            Sends string line payload over TCP socket.

            :param data: Formatted command payload.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected() or not self._socket:
            return False
        with self._lock:
            try:
                payload: bytes = f'{data.strip()}\n'.encode('utf-8')
                self._socket.sendall(payload)
                return True
            except OSError as exc:
                if self._on_log:
                    self._on_log(f'[TX ERR]: {exc}')
                return False

    def _reader_loop(self) -> None:
        '''
            Background loop reading and assembling incoming socket lines.

            :exceptions: None.
        '''
        buffer: str = ''
        while not self._stop_event.is_set():
            sock = self._socket
            if not sock:
                break
            try:
                data: bytes = sock.recv(256)
                if data:
                    buffer += data.decode('utf-8', errors='ignore')
                    while '\n' in buffer:
                        line: str
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line and self._on_line:
                            self._on_line(line)
                else:
                    sleep(0.01)
            except (socket.timeout, BlockingIOError):
                sleep(0.01)
            except OSError:
                break
