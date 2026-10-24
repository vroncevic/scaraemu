# -*- coding: UTF-8 -*-

'''
Module
    target_motion_dispatcher_test.py
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
    Unit tests for TargetMotionDispatcher component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.target.itarget_motion_dispatcher import ITargetMotionDispatcher
from scaraemu.infrastructure.gui.canvas.target.target_motion_dispatcher import TargetMotionDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationQueue:
    '''
        Mock emulation queue for target motion dispatcher test.
    '''
    def __init__(self) -> None:
        self.poses: list[ScaraPose] = []

    def enqueue_waypoint(self, waypoint: ScaraPose) -> bool:
        '''
            Enqueues waypoint.
        '''
        self.poses.append(waypoint)
        return True

    def clear_queue(self) -> None:
        '''
            Clears queue.
        '''
        self.poses.clear()


class _MockMotionPort:
    '''
        Unit tests for _MockMotionPort.
    '''
    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.moves: list[ScaraPose] = []

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Tests send hardware move.

            :param pose: Input pose.
            :exceptions: None.
        '''
        self.moves.append(pose)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestTargetMotionDispatcher(TestCase):
    '''
        Unit tests verifying TargetMotionDispatcher behavior.

        It defines:

            :methods:
                | setUp - Tests setUp.
                | test_structural_protocol_typing - Verifies TargetMotionDispatcher satisfies protocol structurally.
                | test_dispatch_motion - Verifies dispatching pose enqueues into trajectory and sends hardware move.
                | test_get_version - Verifies semantic version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Tests setUp.

            :exceptions: None.
        '''
        self.queue = _MockEmulationQueue()
        self.motion_port = _MockMotionPort()
        self.dispatcher = TargetMotionDispatcher(
            emulation_queue=self.queue,
            motion_port=self.motion_port,
        )

    def test_structural_protocol_typing(self) -> None:
        '''
            Verifies TargetMotionDispatcher satisfies protocol structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.dispatcher, ITargetMotionDispatcher)

    def test_dispatch_motion(self) -> None:
        '''
            Verifies dispatching pose enqueues into trajectory and sends hardware move.

            :exceptions: None.
        '''
        target: ScaraPose = ScaraPose(x=120.0, y=80.0, z=15.0, phi=0.5)
        self.dispatcher.dispatch_motion(target)

        self.assertEqual(len(self.queue.poses), 1)
        self.assertEqual(self.queue.poses[0], target)
        self.assertEqual(len(self.motion_port.moves), 1)
        self.assertEqual(self.motion_port.moves[0], target)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.dispatcher.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
