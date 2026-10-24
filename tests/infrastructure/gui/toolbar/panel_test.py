# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for SerialBar composite container component.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaracom.transport.preference.preference import SerialPreference

from scaraemu.infrastructure.gui.toolbar.panel import SerialBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockPortScanner:
    '''
        Mock port scanner returning test serial ports.
    '''

    def scan_ports(self) -> list[str]:
        '''
            Returns dummy port list.

            :return: List of device paths.
            :exceptions: None.
        '''
        return ['/dev/ttyUSB0']

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockPreferencesRepository:
    '''
        Mock preferences repository returning preset preferences.
    '''

    def has_preference(self) -> bool:
        '''
            Returns True indicating preference exists.

            :return: True.
            :exceptions: None.
        '''
        return True

    def load_preference(self) -> SerialPreference:
        '''
            Returns dummy SerialPreference.

            :return: SerialPreference instance.
            :exceptions: None.
        '''
        return SerialPreference(port='/dev/ttyUSB0', baud=115200)

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Simulates preference saving.

            :param preference: Selected preference.
            :return: True.
            :exceptions: None.
        '''
        _ = preference
        return True

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockActionDelegate:
    '''
        Mock delegate tracking serial bar user actions.
    '''

    def __init__(self) -> None:
        '''
            Initializes action delegate call records.

            :exceptions: None.
        '''
        self.connect_calls: list[tuple[str, int]] = []
        self.server_toggle_called: bool = False

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Records connect toggle invocation.

            :param port: Selected port path.
            :param baudrate: Selected baud rate.
            :exceptions: None.
        '''
        self.connect_calls.append((port, baudrate))

    def handle_server_toggle(self) -> None:
        '''
            Records server toggle invocation.

            :exceptions: None.
        '''
        self.server_toggle_called = True

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestSerialBar(TestCase):
    '''
        Unit tests for SerialBar.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_serial_bar_initialization_and_properties - Tests toolbar initialization, properties, and version inquiry.
                | test_serial_bar_state_updates - Tests delegating connection and server state updates.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_serial_bar_initialization_and_properties(self) -> None:
        '''
            Tests toolbar initialization, properties, and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockActionDelegate()
        toolbar = SerialBar(
            self._root,
            delegate=delegate,
            port_scanner=_MockPortScanner(),
            preference_repository=_MockPreferencesRepository(),
        )
        toolbar.pack()

        self.assertIsInstance(toolbar, SerialBar)
        self.assertEqual(toolbar.get_version(), '1.0.2')

    def test_serial_bar_state_updates(self) -> None:
        '''
            Tests delegating connection and server state updates.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockActionDelegate()
        toolbar = SerialBar(
            self._root,
            delegate=delegate,
            port_scanner=_MockPortScanner(),
            preference_repository=_MockPreferencesRepository(),
        )

        toolbar.set_connected_state(True)
        toolbar.set_connected_state(False)

        toolbar.set_server_state(True, 8888)
        toolbar.set_server_state(False, 8888)


if __name__ == '__main__':
    unittest_main()
