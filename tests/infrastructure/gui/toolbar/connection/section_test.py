# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for ConnectionSection toolbar subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.toolbar.connection.section import ConnectionSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockPortProvider:
    '''
        Mock port provider returning preset port and baudrate.
    '''

    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 115200) -> None:
        '''
            Tests init.

            :param port: Input port.
            :param baud: Input baud.
            :exceptions: None.
        '''
        self._port = port
        self._baud = baud

    def get_connection_parameters(self) -> tuple[str, int]:
        '''
            Tests get connection parameters.

            :exceptions: None.
        '''
        return (self._port, self._baud)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockSerialBarDelegate:
    '''
        Mock delegate recording serial bar user actions.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.connect_calls: list[tuple[str, int]] = []
        self.server_toggle_called: bool = False

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Tests handle connect toggle.

            :param port: Input port.
            :param baudrate: Input baudrate.
            :exceptions: None.
        '''
        self.connect_calls.append((port, baudrate))

    def handle_server_toggle(self) -> None:
        '''
            Tests handle server toggle.

            :exceptions: None.
        '''
        self.server_toggle_called = True

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestConnectionSection(TestCase):
    '''
        Unit tests for ConnectionSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_section_initialization_and_toggle - Tests section initialization and connected state updating.
                | test_connect_button_click_invokes_delegate - Tests button click invoking delegate with provider parameters.
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

    def test_section_initialization_and_toggle(self) -> None:
        '''
            Tests section initialization and connected state updating.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        provider = _MockPortProvider('/dev/ttyUSB1', 57600)
        delegate = _MockSerialBarDelegate()

        section = ConnectionSection(
            self._root,
            port_provider=provider,
            delegate=delegate,
        )
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')

        section.set_connected_state(True)
        self.assertEqual(section.get_button()['text'], 'Disconnect')

        section.set_connected_state(False)
        self.assertEqual(section.get_button()['text'], 'Connect')

    def test_connect_button_click_invokes_delegate(self) -> None:
        '''
            Tests button click invoking delegate with provider parameters.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        provider = _MockPortProvider('/dev/ttyACM0', 115200)
        delegate = _MockSerialBarDelegate()

        section = ConnectionSection(
            self._root,
            port_provider=provider,
            delegate=delegate,
        )

        section.get_button().invoke()
        self.assertEqual(delegate.connect_calls, [('/dev/ttyACM0', 115200)])


if __name__ == '__main__':
    unittest_main()
