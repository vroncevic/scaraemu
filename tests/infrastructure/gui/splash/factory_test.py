# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SplashScreenFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scaraemu.infrastructure.gui.splash.factory import SplashScreenFactory
from scaraemu.infrastructure.gui.splash.ifactory import ISplashScreenFactory
from scaraemu.infrastructure.gui.splash.screen import SplashScreen

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSplashScreenFactory(TestCase):
    '''
        Tests verifying SplashScreenFactory creation methods.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_factory_version(self) -> None:
        '''Verifies factory version string.'''
        self.assertEqual(SplashScreenFactory.get_version(), '1.0.2')

    def test_create_returns_splash_screen(self) -> None:
        '''Verifies create returns active SplashScreen instance.'''
        splash = SplashScreenFactory.create(self.root)
        self.assertIsInstance(splash, SplashScreen)
        splash.close()

    def test_satisfies_isplash_screen_factory(self) -> None:
        '''Verifies SplashScreenFactory conforms to ISplashScreenFactory protocol.'''
        self.assertIsInstance(SplashScreenFactory, ISplashScreenFactory)


if __name__ == '__main__':
    main()
