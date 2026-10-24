# -*- coding: UTF-8 -*-

'''
Module
    holder_test.py
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
    Unit tests for VirtualPlannedPoseHolder implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.server.pose.holder import VirtualPlannedPoseHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualPlannedPoseHolder(TestCase):
    '''
        Test cases verifying VirtualPlannedPoseHolder state retention and base pose selection.

        It defines:

            :methods:
                | setUp - Sets up test fixture with planned pose holder.
                | test_initial_state - Verifies initial state falls back to current pose.
                | test_set_and_get_base_pose - Verifies setting planned pose returns it.
                | test_reset - Verifies reset clears planned pose flag.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with planned pose holder.

            :exceptions: None.
        '''
        self._holder = VirtualPlannedPoseHolder()

    def test_initial_state(self) -> None:
        '''
            Verifies initial state falls back to current pose.

            :exceptions: None.
        '''
        current = ScaraPose(x=10.0, y=20.0, z=30.0, phi=0.5)
        base = self._holder.get_base_pose(queue_depth=0, current_pose=current)
        self.assertEqual(base, current)

    def test_set_and_get_base_pose(self) -> None:
        '''
            Verifies setting planned pose returns it when queue depth is positive.

            :exceptions: None.
        '''
        planned = ScaraPose(x=100.0, y=150.0, z=20.0, phi=1.0)
        current = ScaraPose(x=10.0, y=20.0, z=30.0, phi=0.5)
        self._holder.set_planned_pose(planned)

        base_with_queue = self._holder.get_base_pose(queue_depth=1, current_pose=current)
        self.assertEqual(base_with_queue, planned)

        base_without_queue = self._holder.get_base_pose(queue_depth=0, current_pose=current)
        self.assertEqual(base_without_queue, current)

    def test_reset(self) -> None:
        '''
            Verifies reset clears planned pose.

            :exceptions: None.
        '''
        planned = ScaraPose(x=100.0, y=150.0, z=20.0, phi=1.0)
        current = ScaraPose(x=10.0, y=20.0, z=30.0, phi=0.5)
        self._holder.set_planned_pose(planned)

        self._holder.reset()
        base = self._holder.get_base_pose(queue_depth=1, current_pose=current)
        self.assertEqual(base, current)

    def test_get_version(self) -> None:
        '''
            Verifies version retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self._holder.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
