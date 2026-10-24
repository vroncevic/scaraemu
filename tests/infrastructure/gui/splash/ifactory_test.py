# -*- coding: UTF-8 -*-

'''
Module
    ifactory_test.py
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
    Unit tests for ISplashScreenFactory interface protocol.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scaraemu.infrastructure.gui.splash.ifactory import ISplashScreenFactory
from scaraemu.infrastructure.gui.splash.iscreen import ISplashScreen


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummySplash:
    '''Dummy splash screen implementation for factory test.'''

    def set_progress(self, progress: int, status: str) -> None:
        '''Updates progress value and status text.'''

    def get_progress(self) -> tuple[int, str]:
        '''Returns progress value and status text.'''
        return (0, '')

    def close(self) -> None:
        '''Dismisses splash screen.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class _DummySplashFactory:
    '''Dummy splash factory implementation for protocol testing.'''

    def create(self, _parent: Tk) -> ISplashScreen:
        '''Constructs active splash screen instance.'''
        return _DummySplash()

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class TestISplashScreenFactory(TestCase):
    '''
        Tests verifying ISplashScreenFactory protocol definition and subtyping.
    '''

    def test_protocol_methods(self) -> None:
        '''Verifies methods declared on ISplashScreenFactory protocol.'''
        self.assertTrue(hasattr(ISplashScreenFactory, 'create'))
        self.assertTrue(hasattr(ISplashScreenFactory, 'get_version'))

    def test_factory_subtyping(self) -> None:
        '''Verifies structural satisfaction of ISplashScreenFactory protocol.'''
        dummy = _DummySplashFactory()
        self.assertIsInstance(dummy, ISplashScreenFactory)


if __name__ == '__main__':
    main()
