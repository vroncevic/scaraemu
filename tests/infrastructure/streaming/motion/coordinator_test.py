# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for MotionCoordinator.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.streaming.motion.coordinator import MotionCoordinator
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockQueueStreamer:
    '''
        Mock queue streamer recording motion requests.
    '''

    def __init__(self) -> None:
        '''Initializes mock queue streamer.'''
        self.streamed_trajectories: list[Sequence[ScaraPose]] = []
        self.cleared: bool = False

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''Streams trajectory poses.'''
        self.streamed_trajectories.append(poses)

    def process_ack(self, free_slots: int) -> None:
        '''Processes ack with free slots.'''
        _ = free_slots

    def clear(self) -> None:
        '''Clears streamer.'''
        self.cleared = True

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class TestMotionCoordinator(TestCase):
    '''
        Unit test cases for MotionCoordinator.

        It defines:

            :methods:
                | test_structural_protocol_conformity - Tests structural conformity to IMotionCoordinator.
                | test_send_hardware_move - Tests dispatching single move pose to streamer.
                | test_enqueue_hardware_trajectory - Tests dispatching trajectory waypoints to streamer.
    '''

    def test_structural_protocol_conformity(self) -> None:
        '''
            Tests structural conformity to IMotionCoordinator.

            :exceptions: None.
        '''
        streamer = _MockQueueStreamer()
        coordinator = MotionCoordinator(streamer=streamer)
        self.assertIsInstance(coordinator, IMotionCoordinator)
        self.assertEqual(coordinator.get_version(), '1.0.2')

    def test_send_hardware_move(self) -> None:
        '''
            Tests dispatching single move pose to streamer.

            :exceptions: None.
        '''
        streamer = _MockQueueStreamer()
        coordinator = MotionCoordinator(streamer=streamer)
        pose = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        coordinator.send_hardware_move(pose)
        self.assertEqual(streamer.streamed_trajectories, [(pose,)])

    def test_enqueue_hardware_trajectory(self) -> None:
        '''
            Tests dispatching trajectory waypoints to streamer.

            :exceptions: None.
        '''
        streamer = _MockQueueStreamer()
        coordinator = MotionCoordinator(streamer=streamer)
        poses = [
            ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0),
            ScaraPose(x=30.0, y=40.0, z=15.0, phi=0.0),
        ]
        coordinator.enqueue_hardware_trajectory(poses)
        self.assertEqual(streamer.streamed_trajectories, [poses])


if __name__ == '__main__':
    unittest_main()
