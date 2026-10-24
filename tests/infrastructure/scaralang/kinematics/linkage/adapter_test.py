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
    Unit tests for LinkageAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver

from scaraemu.infrastructure.scaralang.kinematics.linkage.adapter import LinkageAdapter
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLinkageAdapter(TestCase):
    '''
        Validates LinkageAdapter forward kinematics linkage calculations.

        It defines:

            :methods:
                | setUp - Prepares mock kinematics collaborator and adapter instance.
                | test_structural_typing - Verifies structural protocol conformance.
                | test_solve_fk_pose - Verifies delegation of elbow and wrist pose calculation.
                | test_solve_fk - Verifies delegation of end-effector calculation.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with mocked IPlanarKinematicsSolver.

            :exceptions: None.
        '''
        self.mock_planar = MagicMock(spec=IPlanarKinematicsSolver)
        self.adapter = LinkageAdapter(planar=self.mock_planar)

    def test_structural_typing(self) -> None:
        '''
            Verifies LinkageAdapter satisfies ILinkageAdapter protocol structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter, ILinkageAdapter)

    def test_solve_fk_pose(self) -> None:
        '''
            Verifies solve_fk_pose delegates to scaralang planar solver.

            :exceptions: None.
        '''
        elbow = Point2D(x=150.0, y=0.0)
        wrist = Point2D(x=300.0, y=0.0)
        self.mock_planar.solve_fk_pose_2d.return_value = (elbow, wrist)

        res_elbow, res_wrist = self.adapter.solve_fk_pose(0.0, 0.0)
        self.mock_planar.solve_fk_pose_2d.assert_called_once_with(0.0, 0.0)
        self.assertEqual(res_elbow.x, 150.0)
        self.assertEqual(res_wrist.x, 300.0)

    def test_solve_fk(self) -> None:
        '''
            Verifies solve_fk delegates to scaralang planar solver.

            :exceptions: None.
        '''
        pt = Point2D(x=300.0, y=0.0)
        self.mock_planar.solve_fk_2d.return_value = pt

        res = self.adapter.solve_fk(0.0, 0.0)
        self.mock_planar.solve_fk_2d.assert_called_once_with(0.0, 0.0)
        self.assertEqual(res.x, 300.0)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self.adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
