# -*- coding: UTF-8 -*-

'''
Module
    test_kinematics_service.py
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
    Unit tests for KinematicsService analytical solver.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.core.service.kinematics_service import KinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsService(unittest.TestCase):
    '''Unit test cases for KinematicsService.'''

    def setUp(self) -> None:
        '''Sets up kinematics service instance.'''
        self.geom = ScaraGeometry(l1=150.0, l2=120.0)
        self.solver = KinematicsService(geometry=self.geom)

    def test_reachability(self) -> None:
        '''Tests workspace reach boundaries.'''
        self.assertTrue(self.solver.is_reachable(150.0, 0.0))
        self.assertTrue(self.solver.is_reachable(0.0, 200.0))
        self.assertFalse(self.solver.is_reachable(300.0, 0.0))  # Exceeds max reach (270)
        self.assertFalse(self.solver.is_reachable(10.0, 0.0))   # Inside dead zone (< 30)

    def test_ik_fk_roundtrip_righty(self) -> None:
        '''Tests inverse and forward kinematics round-trip for righty configuration.'''
        target = ScaraPose(x=180.0, y=50.0, z=25.0, phi=0.3)
        joints: ScaraJoints = self.solver.solve_ik(target, elbow_left=False)
        self.assertTrue(joints.reachable)

        fk_pose: ScaraPose = self.solver.solve_fk(joints)
        self.assertAlmostEqual(fk_pose.x, target.x, places=2)
        self.assertAlmostEqual(fk_pose.y, target.y, places=2)
        self.assertAlmostEqual(fk_pose.z, target.z, places=2)
        self.assertAlmostEqual(fk_pose.phi, target.phi, places=2)

    def test_ik_fk_roundtrip_lefty(self) -> None:
        '''Tests inverse and forward kinematics round-trip for lefty configuration.'''
        target = ScaraPose(x=160.0, y=-40.0, z=15.0, phi=-0.2)
        joints: ScaraJoints = self.solver.solve_ik(target, elbow_left=True)
        self.assertTrue(joints.reachable)

        fk_pose: ScaraPose = self.solver.solve_fk(joints)
        self.assertAlmostEqual(fk_pose.x, target.x, places=2)
        self.assertAlmostEqual(fk_pose.y, target.y, places=2)
        self.assertAlmostEqual(fk_pose.z, target.z, places=2)

    def test_joints_steps_roundtrip(self) -> None:
        '''Tests discrete motor step coordinate conversions.'''
        joints = ScaraJoints(theta1=0.5, theta2=-0.3, z=30.0, theta4=0.2)
        steps = self.solver.joints_to_steps(joints)
        reconstructed = self.solver.steps_to_joints(steps)

        self.assertAlmostEqual(reconstructed.theta1, joints.theta1, places=2)
        self.assertAlmostEqual(reconstructed.theta2, joints.theta2, places=2)
        self.assertAlmostEqual(reconstructed.z, joints.z, places=2)

    def test_interpolate_linear(self) -> None:
        '''Tests Cartesian linear waypoints subdivision.'''
        p1 = ScaraPose(x=100.0, y=0.0, z=0.0)
        p2 = ScaraPose(x=110.0, y=0.0, z=0.0)
        pts = self.solver.interpolate_linear(p1, p2, segment_len_mm=2.0)
        self.assertEqual(len(pts), 5)
        self.assertAlmostEqual(pts[-1].x, 110.0)

    def test_update_geometry(self) -> None:
        '''Tests updating physical link lengths.'''
        new_geom = ScaraGeometry(l1=200.0, l2=150.0)
        self.solver.update_geometry(new_geom)
        self.assertEqual(self.solver.get_geometry().l1, 200.0)


if __name__ == '__main__':
    unittest.main()
