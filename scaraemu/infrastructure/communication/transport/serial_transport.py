# -*- coding: UTF-8 -*-

'''
Module
    serial_transport.py
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
    Thread-safe PySerial transport implementing ITransport protocol.
'''

from __future__ import annotations

from threading import Lock, Event, Thread
from time import sleep
from typing import Callable, Final

from serial import Serial, SerialException

from scaraemu.infrastructure.communication.transport.itransport import ITransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransport(ITransport):
    '''
        Hardware serial communication transport communicating with microcontroller over UART/USB.

        It defines:

            :attributes:
                | _serial - PySerial connection instance.
                | _lock - Mutex protecting serial TX write operations.
                | _stop_event - Event signaling reader thread termination.
                | _reader_thread - Background RX polling thread.
                | _on_line - Callback invoked when a complete line is received.
                | _on_log - Callback for communication logging.
            :methods:
                | __init__ - Initializes transport handle and sync primitives.
                | is_connected - Checks if serial port is open.
                | set_callbacks - Registers packet reception and connection logging hooks.
                | connect - Opens serial port with port name and baudrate.
                | disconnect - Closes serial connection and stops RX thread.
                | write_line - Transmits formatted command string over serial.
    '''

    _serial: Serial | None
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
            Initializes transport handle and sync primitives.

            :param on_line: Optional line received callback.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._serial = None
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
            Checks if serial port is open.

            :return: True if open, False otherwise.
            :exceptions: None.
        '''
        return bool(self._serial and self._serial.is_open)

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        '''
            Opens serial port with port name and baudrate.

            :param port: Device port path (e.g. '/dev/ttyACM0').
            :param baudrate: Transmission baud rate (default 115200).
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        try:
            self._serial = Serial(port, baudrate, timeout=0.1)
            self._stop_event.clear()
            self._reader_thread = Thread(target=self._reader_loop, daemon=True)
            self._reader_thread.start()

            if self._on_log:
                self._on_log(f'[HOST]: Connected to {port} @ {baudrate} bps')

            return True
        except (OSError, SerialException) as exc:
            if self._on_log:
                self._on_log(f'[ERR]: Connection failed: {exc}')
            self.disconnect()
            return False

    def disconnect(self) -> None:
        '''
            Closes serial connection and stops RX thread.

            :exceptions: None.
        '''
        self._stop_event.set()
        if self._serial:
            try:
                self._serial.close()
            except (OSError, SerialException, TypeError, AttributeError):
                pass
            self._serial = None

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=0.2)
            self._reader_thread = None

        if self._on_log:
            self._on_log('[HOST]: Disconnected from serial port')

    def write_line(self, data: str) -> bool:
        '''
            Transmits formatted command string over serial.

            :param data: Formatted command payload.
            :return: True if written successfully, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected() or not self._serial:
            return False
        with self._lock:
            try:
                payload: bytes = f'{data.strip()}\n'.encode('utf-8')
                self._serial.write(payload)
                self._serial.flush()
                return True
            except (OSError, SerialException) as exc:
                if self._on_log:
                    self._on_log(f'[TX ERR]: {exc}')
                return False

    def _reader_loop(self) -> None:
        '''
            Background thread polling and assembling incoming newline-terminated lines.

            :exceptions: None.
        '''
        buffer: str = ''
        abnormal_disconnect: bool = False
        while not self._stop_event.is_set():
            ser = self._serial
            if not ser or not ser.is_open:
                break
            try:
                data: bytes = ser.read(64)
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
            except (OSError, SerialException, TypeError, AttributeError):
                if not self._stop_event.is_set():
                    abnormal_disconnect = True
                break

        if abnormal_disconnect:
            if self._serial:
                try:
                    self._serial.close()
                except (OSError, SerialException, TypeError, AttributeError):
                    pass
                self._serial = None
            if self._on_log:
                self._on_log('[HOST]: Connection lost (device disconnected / unplugged)')
