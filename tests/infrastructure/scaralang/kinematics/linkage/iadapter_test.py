# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for ILinkageAdapter interface protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from scaralang.core.model.kinematics.pose.point_2d import Point2D

from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyLinkageAdapter:
    '''
        Minimal dummy implementation for testing ILinkageAdapter protocol conformance.
    '''

    def solve_fk_pose(
        self,
        theta1_rad: float,
        theta2_rad: float,
    ) -> tuple[Point2D, Point2D]:
        '''
            Computes Cartesian coordinates of elbow and wrist joints.
        '''
        return (Point2D(x=100.0, y=0.0), Point2D(x=200.0, y=0.0))

    def solve_fk(
        self,
        theta1_rad: float,
        theta2_rad: float,
    ) -> Point2D:
        '''
            Computes Cartesian end-effector coordinates.
        '''
        return Point2D(x=200.0, y=0.0)

    def get_version(self) -> str:
        '''
            Returns protocol version string.
        '''
        return '1.0.2'


class TestILinkageAdapter(TestCase):
    '''
        Validates structural protocol compliance for ILinkageAdapter.

        It defines:

            :methods:
                | test_protocol_implementation - Verifies protocol structural conformance.
                | test_protocol_methods - Verifies dummy class fulfills protocol methods.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies that dummy class matches ILinkageAdapter protocol.

            :exceptions: None.
        '''
        dummy = DummyLinkageAdapter()
        self.assertIsInstance(dummy, ILinkageAdapter)

    def test_protocol_methods(self) -> None:
        '''
            Verifies protocol methods behavior on compliant instance.

            :exceptions: None.
        '''
        dummy = DummyLinkageAdapter()
        elbow, wrist = dummy.solve_fk_pose(0.0, 0.0)
        self.assertEqual(elbow.x, 100.0)
        self.assertEqual(wrist.x, 200.0)
        ee = dummy.solve_fk(0.0, 0.0)
        self.assertEqual(ee.x, 200.0)
        self.assertEqual(dummy.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
