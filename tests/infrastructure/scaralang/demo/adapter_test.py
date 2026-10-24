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
    Unit test cases for TrajectoryDemoAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.service.trajectory.discretization.factory import DiscretizationFactory
from scaralang.core.service.trajectory.discretization.provides import DiscretizationProvides

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.demo.adapter import TrajectoryDemoAdapter
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoAdapterTestCase(TestCase):
    '''
        Test case verifying TrajectoryDemoAdapter functionality.

        It defines:

            :methods:
                | setUp - Initializes test adapter with real scaralang discretizers.
                | test_satisfies_protocol - Verifies structural protocol conformance.
                | test_generate_circle - Tests circle generation produces poses.
                | test_generate_square - Tests square generation produces poses.
                | test_generate_fallback - Tests fallback preset produces center pose.
                | test_get_version - Verifies version string.
    '''

    adapter: TrajectoryDemoAdapter

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test.
        '''
        provides: DiscretizationProvides = DiscretizationFactory.create()
        self.adapter = TrajectoryDemoAdapter(provides.circle, provides.rectangle)

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies adapter satisfies ITrajectoryDemoAdapter protocol.
        '''
        self.assertIsInstance(self.adapter, ITrajectoryDemoAdapter)

    def test_generate_circle(self) -> None:
        '''
            Tests circle preset generation returns list of ScaraPose instances.
        '''
        poses: list[ScaraPose] = self.adapter.generate('circle', 100.0, 50.0, 10.0)
        self.assertIsInstance(poses, list)
        self.assertGreater(len(poses), 0)
        self.assertIsInstance(poses[0], ScaraPose)
        self.assertEqual(poses[0].phi, 0.0)

    def test_generate_square(self) -> None:
        '''
            Tests square preset generation returns list of ScaraPose instances.
        '''
        poses: list[ScaraPose] = self.adapter.generate('square', 100.0, 50.0, 10.0)
        self.assertIsInstance(poses, list)
        self.assertGreater(len(poses), 0)
        self.assertIsInstance(poses[0], ScaraPose)
        self.assertEqual(poses[0].phi, 0.0)

    def test_generate_fallback(self) -> None:
        '''
            Tests fallback preset returns list containing center pose.
        '''
        poses: list[ScaraPose] = self.adapter.generate('unknown', 100.0, 50.0, 10.0)
        self.assertEqual(len(poses), 1)
        self.assertEqual(poses[0].x, 100.0)
        self.assertEqual(poses[0].y, 50.0)
        self.assertEqual(poses[0].z, 10.0)
        self.assertEqual(poses[0].phi, 0.0)

    def test_get_version(self) -> None:
        '''
            Verifies version string.
        '''
        self.assertEqual(self.adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
