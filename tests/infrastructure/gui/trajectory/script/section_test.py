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
    Unit tests for ScriptLoaderSection subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from scaraemu.infrastructure.gui.trajectory.script.section import ScriptLoaderSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockScriptLoaderDelegate:
    '''
        Mock script loader delegate.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.loaded_scripts: list[str] = []

    def handle_load_script(self, script_path: str) -> None:
        '''
            Tests handle load script.

            :param script_path: Input script_path.
            :exceptions: None.
        '''
        self.loaded_scripts.append(script_path)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestScriptLoaderSection(TestCase):
    '''
        Unit tests for ScriptLoaderSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_section_initialization_and_version - Tests section initialization and version inquiry.
                | test_handle_script_selected - Tests script selection dispatches to delegate.
                | test_handle_browse_file - Tests browsing file dialog dispatches selected path to delegate.
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

    def test_section_initialization_and_version(self) -> None:
        '''
            Tests section initialization and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockScriptLoaderDelegate()
        section = ScriptLoaderSection(self._root, delegate=delegate)
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')

    @patch(
        'scaraemu.infrastructure.gui.trajectory.script.section.ScriptExampleDiscovery.discover_examples',
        return_value={'test.scara': '/path/to/test.scara'},
    )
    def test_handle_script_selected(self, _mock_discovery: MagicMock) -> None:
        '''
            Tests script selection dispatches to delegate.

            :param _mock_discovery: Mocked discovery method.
            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockScriptLoaderDelegate()
        section = ScriptLoaderSection(self._root, delegate=delegate)
        section.load_example('test.scara')

        self.assertEqual(delegate.loaded_scripts, ['/path/to/test.scara'])

    @patch(
        'scaraemu.infrastructure.gui.trajectory.script.section.askopenfilename',
        return_value='/path/to/plan.json',
    )
    def test_handle_browse_file(self, _mock_dialog: MagicMock) -> None:
        '''
            Tests browsing file dialog dispatches selected path to delegate.

            :param _mock_dialog: Mocked file dialog.
            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockScriptLoaderDelegate()
        section = ScriptLoaderSection(self._root, delegate=delegate)
        section.handle_browse_file()
        self.assertEqual(delegate.loaded_scripts, ['/path/to/plan.json'])


if __name__ == '__main__':
    unittest_main()
