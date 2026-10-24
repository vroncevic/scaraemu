# -*- coding: UTF-8 -*-

'''
Module
    igui_test.py
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
    Unit tests for IGUI structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyGUI:
    '''
        Dummy class conforming to IGUI structurally.

        It defines:

            :methods:
                | is_initialized - Returns initialization status.
                | load_file - Sets initial plan or DSL script to load upon GUI startup.
                | run - Starts the Tkinter main event loop.
    '''

    def is_initialized(self) -> bool:
        '''
            Returns initialization status.

            :exceptions: None.
        '''
        return True

    def load_file(self, file_path: str) -> None:
        '''
            Sets initial plan or DSL script to load upon GUI startup.

            :param file_path: Input file_path.
            :exceptions: None.
        '''
        del file_path

    def run(self) -> None:
        '''
            Starts the Tkinter main event loop.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidGUI:
    '''
        Dummy class missing required protocol methods.

        It defines:

            :methods:
                | dummy_action - Dummy placeholder action.
                | get_status - Returns dummy status.
    '''

    def dummy_action(self) -> None:
        '''
            Performs dummy action.

            :exceptions: None.
        '''

    def get_status(self) -> str:
        '''
            Returns dummy status.

            :return: Status string.
            :exceptions: None.
        '''
        return 'invalid'


class TestIGUI(TestCase):
    '''
        Test cases verifying IGUI structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy conforming class satisfies IGUI structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy IGUI.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IGUI structurally.

            :exceptions: None.
        '''
        gui = _DummyGUI()
        self.assertIsInstance(gui, IGUI)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IGUI.

            :exceptions: None.
        '''
        invalid = _InvalidGUI()
        self.assertNotIsInstance(invalid, IGUI)


if __name__ == '__main__':
    unittest_main()
