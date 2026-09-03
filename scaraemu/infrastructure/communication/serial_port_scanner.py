# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner.py
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
    Utility for detecting and enumerating available serial COM ports.
'''

from __future__ import annotations

from sys import platform
from typing import ClassVar
from serial.tools.list_ports import comports

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortScanner:
    '''
        Hardware serial port scanner discovering available USB/COM communication endpoints.

        It defines:

            :attributes:
                | LINUX_DEFAULT_PORTS - Standard Linux serial device paths.
                | WINDOWS_DEFAULT_PORTS - Standard Windows COM port identifiers.
                | DARWIN_DEFAULT_PORTS - Standard macOS USB serial device paths.
            :methods:
                | get_default_ports_for_os - Returns fallback port identifiers based on OS.
                | scan_ports - Enumerates detected serial ports with descriptions.
                | list_ports - Enumerates available raw serial port device paths.
    '''

    LINUX_DEFAULT_PORTS: ClassVar[tuple[str, ...]] = (
        '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1'
    )
    WINDOWS_DEFAULT_PORTS: ClassVar[tuple[str, ...]] = (
        'COM1', 'COM2', 'COM3', 'COM4'
    )
    DARWIN_DEFAULT_PORTS: ClassVar[tuple[str, ...]] = (
        '/dev/tty.usbmodem1', '/dev/tty.usbserial1'
    )

    @classmethod
    def get_default_ports_for_os(cls, os_name: str | None = None) -> list[str]:
        '''
            Returns fallback port identifiers based on target operating system.

            :param os_name: Optional OS platform identifier (defaults to sys.platform).
            :return: List of default port paths or names.
            :exceptions: None.
        '''
        target_os: str = (os_name or platform).lower()

        if 'darwin' in target_os or 'mac' in target_os:
            return list(cls.DARWIN_DEFAULT_PORTS)

        if 'win' in target_os:
            return list(cls.WINDOWS_DEFAULT_PORTS)

        return list(cls.LINUX_DEFAULT_PORTS)

    @classmethod
    def scan_ports(cls) -> list[str]:
        '''
            Enumerates and returns list of detected serial port identifiers with descriptions.

            :return: List of port device description strings.
            :exceptions: None.
        '''
        detected: list[str] = []

        try:
            ports = comports()

            for port in ports:
                if port.device.startswith('/dev/ttyS') and (not port.description or port.description == 'n/a'):
                    continue
                desc: str = f'{port.device} - {port.description}' if port.description else port.device
                detected.append(desc)

        except (OSError, AttributeError):
            pass

        return detected if detected else cls.get_default_ports_for_os()

    @classmethod
    def list_ports(cls) -> list[str]:
        '''
            Enumerate available raw serial port device names.

            :return: List of device port paths (e.g. ['/dev/ttyACM0', 'COM3']).
            :exceptions: None.
        '''
        try:
            ports = comports()
            return [str(port.device) for port in ports]
        except (OSError, AttributeError):
            return cls.get_default_ports_for_os()
