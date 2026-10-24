# -*- coding: UTF-8 -*-

'''
Module
    iview_test.py
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
    Unit tests for IQueueDepthView structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyQueueDepthView:
    '''
        Dummy class conforming to IQueueDepthView structurally.
    '''

    def update_queue_depth(self, count: int) -> None:
        '''
            Updates displayed queue depth count.

            :param count: Input count.
            :exceptions: None.
        '''
        _ = count

    def get_version(self) -> str:
        '''
            Returns view interface version.

            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidQueueDepthView:
    '''
        Dummy class missing required protocol methods.
    '''

    def invalid_action(self) -> None:
        '''
            Tests invalid action.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestIQueueDepthView(TestCase):
    '''
        Test cases verifying IQueueDepthView structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy conforming class satisfies IQueueDepthView structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy IQueueDepthView.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IQueueDepthView structurally.

            :exceptions: None.
        '''
        view = _DummyQueueDepthView()
        self.assertIsInstance(view, IQueueDepthView)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IQueueDepthView.

            :exceptions: None.
        '''
        invalid = _InvalidQueueDepthView()
        self.assertNotIsInstance(invalid, IQueueDepthView)


if __name__ == '__main__':
    unittest_main()
