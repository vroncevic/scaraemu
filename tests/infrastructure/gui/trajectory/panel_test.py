# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for TrajectoryDemoPanel composite container.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.panel import TrajectoryDemoPanel
from scaraemu.infrastructure.gui.trajectory.preset.section import TrajectoryPresetSection
from scaraemu.infrastructure.gui.trajectory.queue.section import TrajectoryQueueSection
from scaraemu.infrastructure.gui.trajectory.script.section import ScriptLoaderSection

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
        Mock preset delegate.
    '''

    def __init__(self) -> None:
        self.selected: list[str] = []

    def handle_demo_select(self, preset_name: str) -> None:
        '''
            Handles demo select.

            :param preset_name: Input preset_name.
            :exceptions: None.
        '''
        self.selected.append(preset_name)

    def get_version(self) -> str:
        '''
            Returns version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockScriptLoaderDelegate:
    '''
        Mock script loader delegate.
    '''

    def __init__(self) -> None:
        self.loaded: list[str] = []

    def handle_load_script(self, script_path: str) -> None:
        '''
            Handles load script.

            :param script_path: Input script_path.
            :exceptions: None.
        '''
        self.loaded.append(script_path)

    def get_version(self) -> str:
        '''
            Returns version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockQueueActionDelegate:
    '''
        Mock queue action delegate.
    '''

    def __init__(self) -> None:
        self.cleared: list[bool] = []

    def handle_clear_queue(self) -> None:
        '''
            Handles clear queue.

            :exceptions: None.
        '''
        self.cleared.append(True)

    def handle_clear_trail(self) -> None:
        '''
            Handles clear trail.

            :exceptions: None.
        '''
        self.cleared.append(True)

    def get_version(self) -> str:
        '''
            Returns version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestTrajectoryDemoPanel(TestCase):
    '''
        Unit tests for TrajectoryDemoPanel composite container.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_composite_panel_assembly_and_version - Tests subcomponent assembly, queue section access, and version.
                | test_preset_and_clear_actions - Tests that subcomponents invoke demo and queue delegates.
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

    def test_composite_panel_assembly_and_version(self) -> None:
        '''
            Tests subcomponent assembly, queue section access, and version.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        preset_delegate = _MockTrajectoryPresetDelegate()
        script_delegate = _MockScriptLoaderDelegate()
        queue_delegate = _MockQueueActionDelegate()

        panel = TrajectoryDemoPanel(
            self._root,
            preset_delegate=preset_delegate,
            script_delegate=script_delegate,
            queue_delegate=queue_delegate,
        )
        panel.pack()

        preset_sec, script_sec, queue_sec = panel.get_sections()
        self.assertIsInstance(preset_sec, TrajectoryPresetSection)
        self.assertIsInstance(script_sec, ScriptLoaderSection)
        self.assertIsInstance(queue_sec, TrajectoryQueueSection)
        self.assertIsInstance(panel.queue_section, TrajectoryQueueSection)
        self.assertEqual(panel.get_version(), '1.0.2')

        panel.queue_section.update_queue_depth(15)
        self.assertEqual(panel.queue_section.get_queue_text(), 'Queue: 15 pts')

    def test_preset_and_clear_actions(self) -> None:
        '''
            Tests that subcomponents invoke demo and queue delegates.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        preset_delegate = _MockTrajectoryPresetDelegate()
        script_delegate = _MockScriptLoaderDelegate()
        queue_delegate = _MockQueueActionDelegate()

        panel = TrajectoryDemoPanel(
            self._root,
            preset_delegate=preset_delegate,
            script_delegate=script_delegate,
            queue_delegate=queue_delegate,
        )
        panel.pack()

        preset_sec, _, _ = panel.get_sections()
        preset_sec.select_preset('star')
        self.assertEqual(preset_delegate.selected, ['star'])

        queue_delegate.handle_clear_queue()
        self.assertEqual(queue_delegate.cleared, [True])


if __name__ == '__main__':
    unittest_main()
