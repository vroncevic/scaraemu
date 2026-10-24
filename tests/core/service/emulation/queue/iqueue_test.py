# -*- coding: UTF-8 -*-

'''
Module
    iqueue_test.py
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
    Unit test for IEmulationQueue protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyQueue:
    '''
        Dummy class implementing IEmulationQueue structurally.

        It defines:

            :attributes:
                | waypoints - List of queued waypoints.
            :methods:
                | __init__ - Initializes dummy queue.
                | enqueue_waypoint - Enqueues a waypoint into queue.
                | clear_queue - Clears all waypoints.
                | get_snapshot - Captures snapshot of queue state.
    '''

    def __init__(self) -> None:
        '''
            Initializes dummy queue.

            :exceptions: None.
        '''
        self.waypoints: list[ScaraPose] = []

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''
            Enqueues a waypoint into queue.

            :param waypoint: Target Cartesian pose.
            :param seq_num: Optional sequence number.
            :return: True if enqueued.
            :exceptions: None.
        '''
        _ = seq_num
        self.waypoints.append(waypoint)
        return True

    def clear_queue(self) -> None:
        '''
            Clears all waypoints from queue.

            :exceptions: None.
        '''
        self.waypoints.clear()

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''
            Captures snapshot of queue state.

            :param fallback_pose: Fallback pose if no target is active.
            :return: EmulationQueueSnapshot instance.
            :exceptions: None.
        '''
        target = (
            self.waypoints[0]
            if self.waypoints
            else fallback_pose
        )
        return EmulationQueueSnapshot(
            queue_depth=len(self.waypoints),
            has_target=bool(self.waypoints),
            current_target=target,
            planned_path=(),
        )


class TestIEmulationQueue(TestCase):
    '''
        Unit tests for IEmulationQueue protocol compliance.

        It defines:

            :methods:
                | test_protocol_compliance - Verifies structural protocol compliance.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Verifies structural protocol compliance.

            :exceptions: None.
        '''
        queue = DummyQueue()
        self.assertIsInstance(queue, IEmulationQueue)
        pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        self.assertTrue(queue.enqueue_waypoint(pose))
        self.assertEqual(len(queue.waypoints), 1)
        queue.clear_queue()
        self.assertEqual(len(queue.waypoints), 0)


if __name__ == '__main__':
    unittest_main()
