# -*- coding: UTF-8 -*-

'''
Module
    iconfigurator_test.py
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
    Unit tests for IWindowConfigurator structural protocol.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.window.configurator import WindowConfigurator
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ValidWindowConfigurator:
    '''
        Dummy conforming implementation of IWindowConfigurator.

        It defines:

            :methods:
                | setup_window - Configures root window.
                | maximize_window - Maximizes root window.
                | get_version - Returns version string.
    '''

    def setup_window(self, root: Tk) -> None:
        '''
            Tests setup window.

            :param root: Input root.
            :exceptions: None.
        '''
        _ = root

    def maximize_window(self, root: Tk) -> None:
        '''
            Tests maximize window.

            :param root: Input root.
            :exceptions: None.
        '''
        _ = root

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidWindowConfigurator:
    '''
        Dummy non-conforming implementation missing required protocol methods.

        It defines:

            :methods:
                | dummy_action - Dummy action method.
                | get_status - Dummy status query.
    '''

    def dummy_action(self) -> None:
        '''
            Performs dummy action.

            :exceptions: None.
        '''
        _ = self

    def get_status(self) -> bool:
        '''
            Returns dummy status flag.

            :return: Boolean status.
            :exceptions: None.
        '''
        return False


class TestIWindowConfigurator(TestCase):
    '''
        Test cases verifying IWindowConfigurator protocol conformance.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming dummy instance passes runtime checkable protocol.
                | test_non_conforming_instance - Verifies non-conforming dummy instance fails protocol check.
                | test_concrete_class_satisfies_protocol - Verifies concrete WindowConfigurator class satisfies protocol methods.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming dummy instance passes runtime checkable protocol.

            :exceptions: None.
        '''
        configurator = _ValidWindowConfigurator()
        self.assertIsInstance(configurator, IWindowConfigurator)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming dummy instance fails protocol check.

            :exceptions: None.
        '''
        invalid = _InvalidWindowConfigurator()
        self.assertNotIsInstance(invalid, IWindowConfigurator)

    def test_concrete_class_satisfies_protocol(self) -> None:
        '''
            Verifies concrete WindowConfigurator class satisfies protocol methods.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(WindowConfigurator, 'setup_window'))
        self.assertTrue(hasattr(WindowConfigurator, 'maximize_window'))
        self.assertTrue(hasattr(WindowConfigurator, 'get_version'))


if __name__ == '__main__':
    unittest_main()
