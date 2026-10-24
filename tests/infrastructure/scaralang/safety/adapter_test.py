# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for MotionValidatorAdapter implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionValidatorAdapter(TestCase):
    '''
        Unit tests for MotionValidatorAdapter.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and adapter under test.
                | test_is_pose_valid_with_safe_pose - Verifies safe Cartesian pose is valid.
                | test_is_pose_valid_in_dead_zone - Verifies pose inside dead zone is invalid.
                | test_is_pose_valid_outside_reach - Verifies pose beyond reach envelope is invalid.
                | test_is_segment_valid_safe - Verifies safe non-crossing segment is valid.
                | test_is_segment_valid_crossing_dead_zone - Verifies segment crossing dead zone is rejected.
                | test_is_segment_valid_invalid_endpoints - Verifies segment with bad start/end is rejected.
                | test_get_version - Verifies version string representation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with default MotionValidatorAdapter.
        '''
        self._adapter: IMotionValidatorAdapter = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )

    def test_is_pose_valid_with_safe_pose(self) -> None:
        '''
            Verifies safe Cartesian pose is valid.
        '''
        pose = ScaraPose(x=200.0, y=0.0, z=0.0, phi=0.0)
        self.assertTrue(self._adapter.is_pose_valid(pose))

    def test_is_pose_valid_in_dead_zone(self) -> None:
        '''
            Verifies pose inside dead zone is invalid.
        '''
        pose = ScaraPose(x=20.0, y=20.0, z=0.0, phi=0.0)
        self.assertFalse(self._adapter.is_pose_valid(pose))

    def test_is_pose_valid_outside_reach(self) -> None:
        '''
            Verifies pose beyond reach envelope is invalid.
        '''
        pose = ScaraPose(x=800.0, y=800.0, z=0.0, phi=0.0)
        self.assertFalse(self._adapter.is_pose_valid(pose))

    def test_is_segment_valid_safe(self) -> None:
        '''
            Verifies safe non-crossing segment is valid.
        '''
        p1 = ScaraPose(x=200.0, y=50.0, z=0.0, phi=0.0)
        p2 = ScaraPose(x=200.0, y=-50.0, z=0.0, phi=0.0)
        self.assertTrue(self._adapter.is_segment_valid(p1, p2))

    def test_is_segment_valid_crossing_dead_zone(self) -> None:
        '''
            Verifies segment crossing central dead zone is rejected.
        '''
        p1 = ScaraPose(x=200.0, y=0.0, z=0.0, phi=0.0)
        p2 = ScaraPose(x=-200.0, y=0.0, z=0.0, phi=0.0)
        self.assertFalse(self._adapter.is_segment_valid(p1, p2))

    def test_is_segment_valid_invalid_endpoints(self) -> None:
        '''
            Verifies segment with bad start/end is rejected.
        '''
        bad_start = ScaraPose(x=10.0, y=10.0, z=0.0, phi=0.0)
        good_end = ScaraPose(x=200.0, y=0.0, z=0.0, phi=0.0)
        self.assertFalse(self._adapter.is_segment_valid(bad_start, good_end))
        self.assertFalse(self._adapter.is_segment_valid(good_end, bad_start))

    def test_get_version(self) -> None:
        '''
            Verifies version string representation.
        '''
        self.assertEqual(self._adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
