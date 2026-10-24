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
    Unit tests for WorkspaceReachAdapter implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, PropertyMock

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.envelope.ihome import IHomePoseCalculator

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.reach.adapter import WorkspaceReachAdapter
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceReachAdapter(TestCase):
    '''
        Validates WorkspaceReachAdapter calculations and protocol satisfaction.

        It defines:

            :methods:
                | setUp - Initializes test fixture with mock IWorkspaceEnvelope.
                | test_structural_protocol_satisfaction - Verifies protocol adherence.
                | test_get_safe_r_min - Verifies deadzone radius retrieval.
                | test_get_safe_r_max - Verifies safe outer reach calculation.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixture with mock IWorkspaceEnvelope.

            :exceptions: None.
        '''
        self.mock_envelope = MagicMock(spec=IWorkspaceEnvelope)
        type(self.mock_envelope).r_min = PropertyMock(return_value=77.6)
        type(self.mock_envelope).safe_r_max = PropertyMock(return_value=267.0)
        self.mock_home_calculator = MagicMock(spec=IHomePoseCalculator)
        self.adapter = WorkspaceReachAdapter(
            envelope=self.mock_envelope,
            home_calculator=self.mock_home_calculator,
        )

    def test_structural_protocol_satisfaction(self) -> None:
        '''
            Verifies protocol adherence.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter, IWorkspaceReachAdapter)

    def test_get_safe_r_min(self) -> None:
        '''
            Verifies deadzone radius retrieval from kinematics.

            :exceptions: None.
        '''
        self.assertEqual(self.adapter.get_safe_r_min(), 77.6)

    def test_get_safe_r_max(self) -> None:
        '''
            Verifies safe outer reach retrieval from kinematics.

            :exceptions: None.
        '''
        self.assertEqual(self.adapter.get_safe_r_max(), 267.0)

    def test_calculate_home_pose(self) -> None:
        '''
            Verifies home pose calculation from kinematics service.

            :exceptions: None.
        '''
        self.mock_home_calculator.calculate_home_pose.return_value = CartesianPose(
            x=175.5, y=0.0, z=20.0, phi=0.0
        )
        home = self.adapter.calculate_home_pose()
        self.assertIsInstance(home, ScaraPose)
        self.assertEqual(home.x, 175.5)
        self.assertEqual(home.y, 0.0)
        self.assertEqual(home.z, 20.0)
        self.assertEqual(home.phi, 0.0)
        self.mock_home_calculator.calculate_home_pose.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
