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
    Unit tests for DeadZoneBypassAdapter implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import Mock

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.bypass.adapter import DeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadZoneBypassAdapter(TestCase):
    '''
        Unit tests for DeadZoneBypassAdapter.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and adapter instance.
                | test_implements_protocol - Verifies structural protocol conformance.
                | test_plan_bypass_delegates_to_planner - Verifies waypoint mapping and delegation.
                | test_is_segment_crossing_dead_zone_delegates_to_validator - Verifies boundary check delegation.
                | test_get_version - Verifies version string representation.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock collaborators and adapter instance.

            :exceptions: None.
        '''
        self.mock_planner = Mock(spec=IDeadZoneBypassPlanner)
        self.mock_validator = Mock(spec=IDeadZoneValidator)
        self.adapter = DeadZoneBypassAdapter(
            planner=self.mock_planner,
            validator=self.mock_validator,
        )

    def test_implements_protocol(self) -> None:
        '''
            Verifies structural protocol conformance at runtime.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter, IDeadZoneBypassAdapter)

    def test_plan_bypass_delegates_to_planner(self) -> None:
        '''
            Verifies waypoint mapping and delegation to injected planner.

            :exceptions: None.
        '''
        start_pose = ScaraPose(x=150.0, y=0.0, z=-10.0, phi=0.0)
        end_pose = ScaraPose(x=-150.0, y=0.0, z=-20.0, phi=45.0)

        mock_waypoints = [
            Waypoint(
                x=100.0,
                y=50.0,
                z=-20.0,
                phi=0.0,
                speed=100.0,
                name='',
                command='',
            ),
            Waypoint(
                x=-150.0,
                y=0.0,
                z=-20.0,
                phi=0.0,
                speed=100.0,
                name='',
                command='',
            ),
        ]
        self.mock_planner.plan_bypass.return_value = mock_waypoints

        result = self.adapter.plan_bypass(start_pose, end_pose)

        self.mock_planner.plan_bypass.assert_called_once_with(
            start_pt=Point2D(x=150.0, y=0.0),
            end_pt=Point2D(x=-150.0, y=0.0),
            z=-20.0,
            speed=100.0,
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].x, 100.0)
        self.assertEqual(result[0].y, 50.0)
        self.assertEqual(result[0].z, -20.0)
        self.assertEqual(result[0].phi, 45.0)
        self.assertEqual(result[1].x, -150.0)
        self.assertEqual(result[1].y, 0.0)
        self.assertEqual(result[1].z, -20.0)
        self.assertEqual(result[1].phi, 45.0)

    def test_is_segment_crossing_dead_zone_delegates_to_validator(self) -> None:
        '''
            Verifies dead zone traversal check delegation to injected validator.

            :exceptions: None.
        '''
        start_pose = ScaraPose(x=150.0, y=0.0, z=0.0, phi=0.0)
        end_pose = ScaraPose(x=-150.0, y=0.0, z=0.0, phi=0.0)

        self.mock_validator.is_segment_crossing_dead_zone.return_value = True

        result = self.adapter.is_segment_crossing_dead_zone(start_pose, end_pose)

        self.assertTrue(result)
        self.mock_validator.is_segment_crossing_dead_zone.assert_called_once_with(
            Point2D(x=150.0, y=0.0),
            Point2D(x=-150.0, y=0.0),
        )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns a valid semantic version string.

            :exceptions: None.
        '''
        version = self.adapter.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    unittest_main()
