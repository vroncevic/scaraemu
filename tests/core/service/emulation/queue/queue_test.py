# -*- coding: UTF-8 -*-

'''
Module
    queue_test.py
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
    Unit test cases for EmulationQueue.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.queue.queue import EmulationQueue
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationQueueTestCase(TestCase):
    '''
        Test case verifying EmulationQueue waypoint queuing and snapshots.

        It defines:

            :methods:
                | setUp - Prepares test environment with flags and queue instance.
                | test_structural_compliance - Verifies satisfaction of IEmulationQueue.
                | test_enqueue_and_dequeue - Verifies enqueueing and dequeueing waypoints.
                | test_enqueue_blocked_by_estop - Verifies rejection when estop is active.
                | test_clear_queue - Verifies clearing queue and resetting state.
                | test_get_snapshot - Verifies snapshot generation.
    '''

    def setUp(self) -> None:
        self.flags = EmulationFlags()
        self.queue = EmulationQueue(flags=self.flags)

    def test_structural_compliance(self) -> None:
        '''
            Verifies satisfaction of IEmulationQueue protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.queue, IEmulationQueue)

    def test_enqueue_and_dequeue(self) -> None:
        '''
            Verifies enqueueing and dequeueing waypoints.

            :exceptions: None.
        '''
        target1 = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        target2 = ScaraPose(x=30.0, y=40.0, z=5.0, phi=0.0)

        self.assertTrue(self.queue.enqueue_waypoint(target1, seq_num=1))
        self.assertTrue(self.queue.enqueue_waypoint(target2, seq_num=2))

        active = self.queue.get_active_or_next()
        self.assertTrue(active)
        self.assertEqual(active[0], target1)
        self.assertEqual(active[1], 1)

        self.queue.complete_active()
        next_active = self.queue.get_active_or_next()
        self.assertTrue(next_active)
        self.assertEqual(next_active[0], target2)

    def test_enqueue_blocked_by_estop(self) -> None:
        '''
            Verifies rejection when estop is active.

            :exceptions: None.
        '''
        self.flags.estop_active = True
        target = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        self.assertFalse(self.queue.enqueue_waypoint(target))

    def test_clear_queue(self) -> None:
        '''
            Verifies clearing queue and resetting state.

            :exceptions: None.
        '''
        target = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.queue.clear_queue()
        self.assertEqual(self.queue.get_active_or_next(), ())

    def test_get_snapshot(self) -> None:
        '''
            Verifies snapshot generation.

            :exceptions: None.
        '''
        fallback = ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)
        snapshot: EmulationQueueSnapshot = self.queue.get_snapshot(fallback)
        self.assertFalse(snapshot.has_target)
        self.assertEqual(snapshot.queue_depth, 0)
        self.assertEqual(snapshot.current_target, fallback)


if __name__ == '__main__':
    unittest_main()
