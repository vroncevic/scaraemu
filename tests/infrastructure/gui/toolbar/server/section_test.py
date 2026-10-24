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
    Unit tests for ServerToggleSection toolbar subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.toolbar.server.section import ServerToggleSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockSerialBarDelegate:
    '''
        Mock delegate recording server toggle action.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.server_toggle_called: bool = False

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Tests handle connect toggle.

            :param port: Input port.
            :param baudrate: Input baudrate.
            :exceptions: None.
        '''
        _ = (port, baudrate)

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


class TestServerToggleSection(TestCase):
    '''
        Unit tests for ServerToggleSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_section_initialization_and_state - Tests section initialization and server state updating.
                | test_server_button_click_invokes_delegate - Tests server button click invoking delegate.
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

    def test_section_initialization_and_state(self) -> None:
        '''
            Tests section initialization and server state updating.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockSerialBarDelegate()
        section = ServerToggleSection(self._root, delegate=delegate)
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')

        section.set_server_state(True, 9000)
        self.assertIn(':9000', section.get_button()['text'])

        section.set_server_state(False)
        self.assertIn('OFF', section.get_button()['text'])

    def test_server_button_click_invokes_delegate(self) -> None:
        '''
            Tests server button click invoking delegate.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockSerialBarDelegate()
        section = ServerToggleSection(self._root, delegate=delegate)

        section.get_button().invoke()
        self.assertTrue(delegate.server_toggle_called)


if __name__ == '__main__':
    unittest_main()
