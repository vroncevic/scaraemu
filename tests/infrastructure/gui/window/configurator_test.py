# -*- coding: UTF-8 -*-

'''
Module
    configurator_test.py
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
    Unit tests for WindowConfigurator implementation.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.window.configurator import WindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWindowConfigurator(TestCase):
    '''
        Test cases verifying WindowConfigurator behavior.

        It defines:

            :methods:
                | setUp - Initializes Tkinter root window when display is available.
                | tearDown - Destroys Tkinter root window after test execution.
                | test_setup_window - Verifies setup_window applies title and configuration to root window.
                | test_maximize_window - Verifies maximize_window executes without unhandled exceptions.
                | test_maximize_window_fallback_state_zoomed - Verifies fallback to state zoomed.
                | test_maximize_window_all_tcl_errors - Verifies handling when all zoom attempts raise TclError.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    _root: Tk | None

    def setUp(self) -> None:
        '''
            Initializes Tkinter root window when display is available.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Destroys Tkinter root window after test execution.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_setup_window(self) -> None:
        '''
            Verifies setup_window applies title and configuration to root window.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        configurator = WindowConfigurator()
        configurator.setup_window(self._root)
        self.assertEqual(self._root.title(), 'SCARA Robot 4-DOF Emulator & Visualizer')

    def test_maximize_window(self) -> None:
        '''
            Verifies maximize_window executes without unhandled exceptions.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        configurator = WindowConfigurator()
        try:
            configurator.maximize_window(self._root)
        except TclError:
            self.fail('maximize_window raised unexpected TclError')

    def test_maximize_window_fallback_state_zoomed(self) -> None:
        '''
            Verifies fallback to state zoomed when attributes raises TclError.

            :exceptions: None.
        '''
        mock_root = MagicMock(spec=Tk)
        mock_root.attributes.side_effect = TclError('mock attributes zoomed error')
        configurator = WindowConfigurator()
        configurator.maximize_window(mock_root)
        mock_root.update_idletasks.assert_called_once()
        mock_root.attributes.assert_called_once_with('-zoomed', True)
        mock_root.state.assert_called_once_with('zoomed')

    def test_maximize_window_all_tcl_errors(self) -> None:
        '''
            Verifies handling when all zoom attempts raise TclError.

            :exceptions: None.
        '''
        mock_root = MagicMock(spec=Tk)
        mock_root.attributes.side_effect = TclError('mock attributes zoomed error')
        mock_root.state.side_effect = TclError('mock state zoomed error')
        configurator = WindowConfigurator()
        configurator.maximize_window(mock_root)
        mock_root.update_idletasks.assert_called_once()
        mock_root.attributes.assert_called_once_with('-zoomed', True)
        mock_root.state.assert_called_once_with('zoomed')

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        configurator = WindowConfigurator()
        self.assertIsInstance(configurator.get_version(), str)
        self.assertEqual(configurator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
