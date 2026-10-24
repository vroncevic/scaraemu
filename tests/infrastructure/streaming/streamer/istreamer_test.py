# -*- coding: UTF-8 -*-

'''
Module
    istreamer_test.py
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
    Unit tests for IQueueStreamer protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyQueueStreamer:
    '''
        Dummy implementation satisfying IQueueStreamer protocol.
    '''

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Tests stream trajectory.

            :param poses: Input poses.
            :exceptions: None.
        '''

    def process_ack(self, free_slots: int) -> None:
        '''
            Tests process ACK free slots.

            :param free_slots: Free buffer slots.
            :exceptions: None.
        '''

    def clear(self) -> None:
        '''
            Tests clear queue.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Semantic version.
            :exceptions: None.
        '''
        return '1.0.2'


class QueueStreamerProtocolTestCase(TestCase):
    '''
        Test cases verifying IQueueStreamer protocol runtime checking.

        It defines:

            :methods:
                | test_dummy_implements_protocol - Tests dummy conformance.
                | test_invalid_instance_rejected - Tests non-conforming object.
    '''

    def test_dummy_implements_protocol(self) -> None:
        '''
            Tests dummy conformance.
        '''
        dummy = _DummyQueueStreamer()
        self.assertIsInstance(dummy, IQueueStreamer)

    def test_invalid_instance_rejected(self) -> None:
        '''
            Tests non-conforming object.
        '''
        self.assertNotIsInstance(object(), IQueueStreamer)


if __name__ == '__main__':
    unittest_main()
