# -*- coding: UTF-8 -*-

'''
Module
    imanipulator_test.py
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
    Unit tests for IManipulatorKinematics protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyKinematics:
    '''
        Mock structural implementation conforming to IManipulatorKinematics.

        It defines:

            :methods:
                | solve_fk - Solves mock forward kinematics.
                | solve_ik - Solves mock inverse kinematics.
                | steps_to_joints - Converts mock steps to joints.
                | joints_to_steps - Converts mock joints to steps.
    '''

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Solves mock forward kinematics.

            :param joints: Input joints.
            :exceptions: None.
        '''
        return ScaraPose(x=100.0, y=50.0, z=joints.z, phi=0.0)

    def solve_ik(self, pose: ScaraPose, elbow_left: bool) -> ScaraJoints:
        '''
            Solves mock inverse kinematics.

            :param pose: Input pose.
            :param elbow_left: Input elbow_left.
            :exceptions: None.
        '''
        _ = (elbow_left,)
        return ScaraJoints(theta1=0.0, theta2=0.0, z=pose.z, theta4=0.0, reachable=True)

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Converts mock steps to joints.

            :param steps: Input steps.
            :exceptions: None.
        '''
        _ = (steps,)
        return ScaraJoints(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0, reachable=True)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Converts mock joints to steps.

            :param joints: Input joints.
            :exceptions: None.
        '''
        _ = (joints,)
        return ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0)


class TestIManipulatorKinematics(TestCase):
    '''
        Unit test cases for IManipulatorKinematics protocol verification.

        It defines:

            :methods:
                | test_protocol_structural_subtyping - Tests that a duck-typed class satisfies IManipulatorKinematics at runtime.
    '''

    def test_protocol_structural_subtyping(self) -> None:
        '''
            Tests that a duck-typed class satisfies IManipulatorKinematics at runtime.

            :exceptions: None.
        '''
        solver = DummyKinematics()
        self.assertIsInstance(solver, IManipulatorKinematics)


if __name__ == '__main__':
    unittest_main()
