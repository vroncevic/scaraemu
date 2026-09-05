# -*- coding: UTF-8 -*-

'''
Module
    test_serial_port_scanner.py
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
    Unit tests for SerialPortScanner utility.
'''

from __future__ import annotations

import unittest
from scaraemu.infrastructure.communication.serial_port_scanner import SerialPortScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSerialPortScanner(unittest.TestCase):
    '''Unit test cases for SerialPortScanner.'''

    def test_list_ports(self) -> None:
        '''Tests port list return type.'''
        ports = SerialPortScanner.list_ports()
        self.assertIsInstance(ports, list)

    def test_scan_ports(self) -> None:
        '''Tests detected ports with descriptions.'''
        ports = SerialPortScanner.scan_ports()
        self.assertIsInstance(ports, list)

    def test_default_ports_for_os(self) -> None:
        '''Tests fallback port lists across operating systems.'''
        win_ports = SerialPortScanner.get_default_ports_for_os('win32')
        self.assertIn('COM1', win_ports)

        darwin_ports = SerialPortScanner.get_default_ports_for_os('darwin')
        self.assertIn('/dev/tty.usbmodem1', darwin_ports)

        linux_ports = SerialPortScanner.get_default_ports_for_os('linux')
        self.assertIn('/dev/ttyACM0', linux_ports)


if __name__ == '__main__':
    unittest.main()
