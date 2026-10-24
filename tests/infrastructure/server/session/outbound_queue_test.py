# -*- coding: UTF-8 -*-

'''
Module
    outbound_queue_test.py
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
    Unit tests for OutboundFrameQueue.
'''

from __future__ import annotations

from queue import Empty, Queue
from unittest import TestCase, main as unittest_main
from unittest.mock import patch

from scaraemu.infrastructure.server.session.ioutbound_queue import IOutboundFrameQueue
from scaraemu.infrastructure.server.session.outbound_queue import OutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestOutboundFrameQueue(TestCase):
    '''
        Test cases verifying OutboundFrameQueue functionality.

        It defines:

            :methods:
                | test_interface_compliance - Verifies protocol implementation.
                | test_push_and_pop_all - Verifies enqueuing and draining frames.
                | test_clear - Verifies clearing queued frames.
                | test_pop_all_empty_race_handled - Verifies pop_all handles Empty race condition.
                | test_clear_empty_race_handled - Verifies clear handles Empty race condition.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_interface_compliance(self) -> None:
        '''
            Verifies protocol implementation.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        self.assertIsInstance(queue, IOutboundFrameQueue)

    def test_push_and_pop_all(self) -> None:
        '''
            Verifies enqueuing and draining frames.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        self.assertEqual(queue.pop_all(), ())

        queue.push(b'frame1')
        queue.push(b'frame2')
        self.assertEqual(queue.pop_all(), (b'frame1', b'frame2'))
        self.assertEqual(queue.pop_all(), ())

    def test_clear(self) -> None:
        '''
            Verifies clearing queued frames.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        queue.push(b'frame1')
        queue.push(b'frame2')
        queue.clear()
        self.assertEqual(queue.pop_all(), ())

    def test_pop_all_empty_race_handled(self) -> None:
        '''
            Verifies pop_all handles Empty race condition gracefully.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        with patch.object(Queue, 'empty', side_effect=[False, True]), \
             patch.object(Queue, 'get_nowait', side_effect=Empty):
            self.assertEqual(queue.pop_all(), ())

    def test_clear_empty_race_handled(self) -> None:
        '''
            Verifies clear handles Empty race condition gracefully.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        with patch.object(Queue, 'empty', side_effect=[False, True]), \
             patch.object(Queue, 'get_nowait', side_effect=Empty):
            queue.clear()

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        queue = OutboundFrameQueue()
        self.assertEqual(queue.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
