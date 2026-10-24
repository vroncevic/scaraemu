# -*- coding: UTF-8 -*-

'''
Module
    iholder_test.py
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
    Unit tests for IVirtualPlannedPoseHolder structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.server.pose.iholder import IVirtualPlannedPoseHolder
from scaraemu.infrastructure.server.pose.holder import VirtualPlannedPoseHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ValidPoseHolder:
    '''
        Dummy class conforming to IVirtualPlannedPoseHolder structurally.
    '''

    def get_base_pose(self, queue_depth: int, current_pose: ScaraPose) -> ScaraPose:
        '''
            Tests get base pose.

            :param queue_depth: Input queue_depth.
            :param current_pose: Input current_pose.
            :exceptions: None.
        '''
        return current_pose

    def set_planned_pose(self, pose: ScaraPose) -> None:
        '''
            Tests set planned pose.

            :param pose: Input pose.
            :exceptions: None.
        '''
        pass

    def reset(self) -> None:
        '''
            Tests reset.

            :exceptions: None.
        '''
        pass

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidPoseHolder:
    '''
        Dummy class missing required protocol methods.
    '''
    pass


class TestIVirtualPlannedPoseHolder(TestCase):
    '''
        Test cases verifying IVirtualPlannedPoseHolder structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy class satisfies protocol.
                | test_concrete_implementation - Verifies holder satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming class rejected.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IVirtualPlannedPoseHolder structurally.

            :exceptions: None.
        '''
        holder = _ValidPoseHolder()
        self.assertIsInstance(holder, IVirtualPlannedPoseHolder)

    def test_concrete_implementation(self) -> None:
        '''
            Verifies VirtualPlannedPoseHolder satisfies IVirtualPlannedPoseHolder structurally.

            :exceptions: None.
        '''
        holder = VirtualPlannedPoseHolder()
        self.assertIsInstance(holder, IVirtualPlannedPoseHolder)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IVirtualPlannedPoseHolder.

            :exceptions: None.
        '''
        invalid = _InvalidPoseHolder()
        self.assertNotIsInstance(invalid, IVirtualPlannedPoseHolder)


if __name__ == '__main__':
    unittest_main()
