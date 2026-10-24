# -*- coding: UTF-8 -*-

'''
Module
    screen_test.py
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
    Unit tests for SplashScreen implementation.
'''

from __future__ import annotations

from tkinter import Tk, Toplevel
from unittest import TestCase, main
from unittest.mock import patch

from scaraemu.infrastructure.gui.splash.iscreen import ISplashScreen
from scaraemu.infrastructure.gui.splash.screen import SplashScreen

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSplashScreen(TestCase):
    '''
        Tests verifying SplashScreen widget instantiation and lifecycle.

        It defines:

            :methods:
                | setUpClass - Sets up root Tkinter window.
                | tearDownClass - Destroys root Tkinter window.
                | test_splash_screen_conformance - Verifies protocol conformance.
                | test_splash_screen_version - Verifies version string.
                | test_set_progress_and_close - Verifies progress updates and close.
                | test_update_exception_handled - Verifies update exceptions are handled.
                | test_close_exception_handled - Verifies destroy exceptions are handled.
                | test_theme_use_exception_handled - Verifies theme_use exceptions are handled.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tkinter window.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Destroys root Tkinter window.

            :exceptions: None.
        '''
        cls.root.destroy()

    def test_splash_screen_conformance(self) -> None:
        '''
            Verifies that SplashScreen conforms to ISplashScreen protocol.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        self.assertIsInstance(splash, ISplashScreen)
        splash.close()

    def test_splash_screen_version(self) -> None:
        '''
            Verifies splash screen version string.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        self.assertEqual(splash.get_version(), '1.0.2')
        splash.close()

    def test_set_progress_and_close(self) -> None:
        '''
            Verifies set_progress updates progress value and close dismisses window.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.set_progress(50, 'Loading workspace...')
        progress, status = splash.get_progress()
        self.assertEqual(progress, 50)
        self.assertEqual(status, 'Loading workspace...')

        splash.set_progress(150, 'Clamped max')
        progress, _ = splash.get_progress()
        self.assertEqual(progress, 100)

        splash.set_progress(-20, 'Clamped min')
        progress, _ = splash.get_progress()
        self.assertEqual(progress, 0)

        splash.close()

    @patch.object(Toplevel, 'update', side_effect=Exception('update error'))
    def test_update_exception_handled(self, _mock_update: object) -> None:
        '''
            Verifies that update exceptions are handled cleanly.

            :param _mock_update: Mock update method.
            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.set_progress(25, 'Updating...')
        splash.close()

    @patch.object(Toplevel, 'destroy', side_effect=Exception('destroy error'))
    def test_close_exception_handled(self, _mock_destroy: object) -> None:
        '''
            Verifies that destroy exceptions in close are handled cleanly.

            :param _mock_destroy: Mock destroy method.
            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.close()

    @patch('scaraemu.infrastructure.gui.splash.screen.Style.theme_use', side_effect=Exception('theme error'))
    def test_theme_use_exception_handled(self, _mock_theme: object) -> None:
        '''
            Verifies that theme_use exceptions are handled cleanly.

            :param _mock_theme: Mock theme_use method.
            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        self.assertIsInstance(splash, ISplashScreen)
        splash.close()


if __name__ == '__main__':
    main()
