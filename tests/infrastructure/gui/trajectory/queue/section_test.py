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
    Unit tests for TrajectoryQueueSection subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.queue.section import TrajectoryQueueSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockQueueActionDelegate:
    '''
        Mock delegate tracking queue clearing action.
    '''

    clear_called: bool
    clear_trail_called: bool

    def __init__(self) -> None:
        '''
            Initializes call records list.

            :exceptions: None.
        '''
        self.clear_called = False
        self.clear_trail_called = False

    def handle_clear_queue(self) -> None:
        '''
            Records clear queue invocation.

            :exceptions: None.
        '''
        self.clear_called = True

    def handle_clear_trail(self) -> None:
        '''
            Records clear trail invocation.

            :exceptions: None.
        '''
        self.clear_trail_called = True

    def get_version(self) -> str:
        '''
            Returns mock version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestTrajectoryQueueSection(TestCase):
    '''
        Unit tests for TrajectoryQueueSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_queue_depth_update_and_version - Tests queue depth display update and version inquiry.
                | test_clear_queue_action - Tests that clear button executes delegate action.
                | test_clear_trail_action - Tests that clear trail button executes delegate action.
                | test_update_queue_depth_when_destroyed - Tests update ignored when widget destroyed.
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

    def test_queue_depth_update_and_version(self) -> None:
        '''
            Tests queue depth display update and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockQueueActionDelegate()
        section = TrajectoryQueueSection(self._root, delegate=delegate)
        section.pack()

        self.assertIsInstance(section, TrajectoryQueueSection)
        self.assertEqual(section.get_version(), '1.0.2')

        section.update_queue_depth(5)
        section.update_queue_depth(0)
        self.assertIn('0 pts', section.get_queue_text())

    def test_clear_queue_action(self) -> None:
        '''
            Tests that clear button executes delegate action.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockQueueActionDelegate()
        section = TrajectoryQueueSection(self._root, delegate=delegate)
        section.pack()

        delegate.handle_clear_queue()
        self.assertTrue(delegate.clear_called)

    def test_clear_trail_action(self) -> None:
        '''
            Tests that clear trail button executes delegate action.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockQueueActionDelegate()
        section = TrajectoryQueueSection(self._root, delegate=delegate)
        section.pack()

        delegate.handle_clear_trail()
        self.assertTrue(delegate.clear_trail_called)

    def test_update_queue_depth_when_destroyed(self) -> None:
        '''
            Tests update_queue_depth does nothing when widget is destroyed.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        delegate = _MockQueueActionDelegate()
        section = TrajectoryQueueSection(self._root, delegate=delegate)
        section.pack()
        section.destroy()
        section.update_queue_depth(10)


if __name__ == '__main__':
    unittest_main()
