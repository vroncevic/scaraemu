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
    Unit tests for TrajectoryPresetSection subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.preset.section import TrajectoryPresetSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockTrajectoryPresetDelegate:
    '''
        Mock delegate tracking demo preset selection.
    '''

    selected_presets: list[str]

    def __init__(self) -> None:
        '''
            Initializes call records list.

            :exceptions: None.
        '''
        self.selected_presets = []

    def handle_demo_select(self, preset_name: str) -> None:
        '''
            Records preset selection.

            :param preset_name: Selected preset name.
            :exceptions: None.
        '''
        self.selected_presets.append(preset_name)

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestTrajectoryPresetSection(TestCase):
    '''
        Unit tests for TrajectoryPresetSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_preset_section_and_version - Tests section initialization and version inquiry.
                | test_preset_dispatch - Tests that delegate receives preset names.
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

    def test_preset_section_and_version(self) -> None:
        '''
            Tests section initialization and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockTrajectoryPresetDelegate()
        section = TrajectoryPresetSection(self._root, delegate=delegate)
        section.pack()

        self.assertIsInstance(section, TrajectoryPresetSection)
        self.assertEqual(section.get_version(), '1.0.2')

    def test_preset_dispatch(self) -> None:
        '''
            Tests that delegate receives preset names.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockTrajectoryPresetDelegate()
        section = TrajectoryPresetSection(self._root, delegate=delegate)
        section.pack()

        delegate.handle_demo_select('circle')
        self.assertIn('circle', delegate.selected_presets)


if __name__ == '__main__':
    unittest_main()
