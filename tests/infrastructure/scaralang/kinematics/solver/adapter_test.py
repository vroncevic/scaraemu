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
    Unit tests for KinematicsAdapter implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import Mock

from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.adapter import KinematicsAdapter
from scaraemu.infrastructure.scaralang.kinematics.solver.iadapter import IKinematicsAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsAdapter(TestCase):
    '''
        Unit tests for KinematicsAdapter.

        It defines:

            :methods:
                | setUp - Initializes mock kinematics dependencies and adapter instance.
                | test_implements_protocols - Verifies structural protocol conformance at runtime.
                | test_solve_fk_computes_pose_correctly - Verifies solve_fk delegates to kinematics service and builds ScaraPose.
                | test_solve_ik_computes_reachable_joints - Verifies solve_ik returns reachable joints when solution exists.
                | test_solve_ik_computes_unreachable_joints - Verifies solve_ik returns unreachable joints when solver returns None.
                | test_steps_to_joints_delegates_to_converter - Verifies steps_to_joints converts step counts via injected converter.
                | test_joints_to_steps_delegates_to_converter - Verifies joints_to_steps converts joint angles via injected converter.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock kinematics dependencies and adapter instance.

            :exceptions: None.
        '''
        self._mock_planar: Mock = Mock(spec=IPlanarKinematicsSolver)
        self._mock_converter: Mock = Mock(spec=IJointStepTransmissionConverter)
        self._adapter: KinematicsAdapter = KinematicsAdapter(
            planar=self._mock_planar,
            converter=self._mock_converter,
        )

    def test_implements_protocols(self) -> None:
        '''
            Verifies structural protocol conformance at runtime.

            :exceptions: None.
        '''
        self.assertIsInstance(self._adapter, IManipulatorKinematics)
        self.assertIsInstance(self._adapter, IKinematicsAdapter)

    def test_solve_fk_computes_pose_correctly(self) -> None:
        '''
            Verifies solve_fk delegates to kinematics service and builds ScaraPose.

            :exceptions: None.
        '''
        self._mock_planar.solve_fk_2d.return_value = Point2D(x=150.0, y=75.0)
        joints = ScaraJoints(theta1=10.0, theta2=20.0, z=-15.0, theta4=30.0, reachable=True)

        pose = self._adapter.solve_fk(joints)

        self._mock_planar.solve_fk_2d.assert_called_once_with(10.0, 20.0)
        self.assertEqual(pose.x, 150.0)
        self.assertEqual(pose.y, 75.0)
        self.assertEqual(pose.z, -15.0)
        self.assertEqual(pose.phi, 30.0)

    def test_solve_ik_computes_reachable_joints(self) -> None:
        '''
            Verifies solve_ik returns reachable joints when solution exists.

            :exceptions: None.
        '''
        self._mock_planar.solve_ik_2d.return_value = ScaraJoints2D(
            theta1=12.5,
            theta2=45.0,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        pose = ScaraPose(x=200.0, y=100.0, z=-5.0, phi=90.0)

        joints = self._adapter.solve_ik(pose, elbow_left=True)

        self.assertTrue(joints.reachable)
        self.assertEqual(joints.theta1, 12.5)
        self.assertEqual(joints.theta2, 45.0)
        self.assertEqual(joints.z, -5.0)
        self.assertEqual(joints.theta4, 90.0)

    def test_solve_ik_computes_unreachable_joints(self) -> None:
        '''
            Verifies solve_ik returns unreachable joints when solver returns None.

            :exceptions: None.
        '''
        self._mock_planar.solve_ik_2d.return_value = ScaraJoints2D(
            theta1=0.0,
            theta2=0.0,
            reachable=False,
            status=IkStatus.OUT_OF_REACH,
        )
        pose = ScaraPose(x=9999.0, y=9999.0, z=0.0, phi=0.0)

        joints = self._adapter.solve_ik(pose, elbow_left=False)

        self.assertFalse(joints.reachable)
        self.assertEqual(joints.theta1, 0.0)
        self.assertEqual(joints.theta2, 0.0)
        self.assertEqual(joints.z, 0.0)
        self.assertEqual(joints.theta4, 0.0)

    def test_steps_to_joints_delegates_to_converter(self) -> None:
        '''
            Verifies steps_to_joints converts step counts via injected converter.

            :exceptions: None.
        '''
        self._mock_converter.steps_to_angles.return_value = (15.0, 30.0, -10.0, 45.0)
        steps = ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=-500, j4_steps=400)

        joints = self._adapter.steps_to_joints(steps)

        self._mock_converter.steps_to_angles.assert_called_once_with(100, 200, -500, 400)
        self.assertEqual(joints.theta1, 15.0)
        self.assertEqual(joints.theta2, 30.0)
        self.assertEqual(joints.z, -10.0)
        self.assertEqual(joints.theta4, 45.0)
        self.assertTrue(joints.reachable)

    def test_joints_to_steps_delegates_to_converter(self) -> None:
        '''
            Verifies joints_to_steps converts joint angles via injected converter.

            :exceptions: None.
        '''
        self._mock_converter.angles_to_steps.return_value = JointStepCoordinates(
            j1=1000, j2=2000, z=-5000, j4=4000
        )
        joints = ScaraJoints(theta1=10.0, theta2=20.0, z=-25.0, theta4=35.0, reachable=True)

        steps = self._adapter.joints_to_steps(joints)

        self._mock_converter.angles_to_steps.assert_called_once_with(10.0, 20.0, -25.0, 35.0)
        self.assertEqual(steps.j1_steps, 1000)
        self.assertEqual(steps.j2_steps, 2000)
        self.assertEqual(steps.z_steps, -5000)
        self.assertEqual(steps.j4_steps, 4000)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self._adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
