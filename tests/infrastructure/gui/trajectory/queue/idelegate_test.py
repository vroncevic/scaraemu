# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for IQueueActionDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyQueueActionDelegate:
    '''
        Dummy delegate for IQueueActionDelegate protocol conformance.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.clear_count: int = 0
        self.trail_clear_count: int = 0

    def handle_clear_queue(self) -> None:
        '''
            Tests handle clear queue.

            :exceptions: None.
        '''
        self.clear_count += 1

    def handle_clear_trail(self) -> None:
        '''
            Tests handle clear trail.

            :exceptions: None.
        '''
        self.trail_clear_count += 1

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestQueueActionDelegate(TestCase):
    '''
        Test cases verifying IQueueActionDelegate protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy delegate satisfies IQueueActionDelegate protocol.
                | test_clear_queue_handling - Verifies invocation of clear queue action and version.
                | test_clear_trail_handling - Verifies invocation of clear trail action.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy delegate satisfies IQueueActionDelegate protocol.

            :exceptions: None.
        '''
        delegate = _DummyQueueActionDelegate()
        self.assertIsInstance(delegate, IQueueActionDelegate)

    def test_clear_queue_handling(self) -> None:
        '''
            Verifies invocation of clear queue action and version.

            :exceptions: None.
        '''
        delegate = _DummyQueueActionDelegate()
        delegate.handle_clear_queue()

        self.assertEqual(delegate.clear_count, 1)
        self.assertEqual(delegate.get_version(), '1.0.2')

    def test_clear_trail_handling(self) -> None:
        '''
            Verifies invocation of clear trail action.

            :exceptions: None.
        '''
        delegate = _DummyQueueActionDelegate()
        delegate.handle_clear_trail()

        self.assertEqual(delegate.trail_clear_count, 1)


if __name__ == '__main__':
    unittest_main()
