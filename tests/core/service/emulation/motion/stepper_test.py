# -*- coding: UTF-8 -*-

'''
Module
    stepper_test.py
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
    Unit test cases for EmulationStepper.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.motion.stepper import EmulationStepper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationStepperTestCase(TestCase):
    '''
        Test case verifying EmulationStepper linear step calculation.

        It defines:

            :methods:
                | test_partial_step - Verifies partial step interpolation towards target.
                | test_reach_target - Verifies reaching target when step exceeds distance.
                | test_already_at_target - Verifies behavior when already at target.
                | test_get_version - Verifies version string.
    '''

    def test_partial_step(self) -> None:
        '''
            Verifies partial step interpolation towards target.

            :exceptions: None.
        '''
        stepper = EmulationStepper(speed_mm_per_sec=100.0)
        curr = ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)
        target = ScaraPose(x=100.0, y=0.0, z=0.0, phi=0.0)

        next_pose, reached = stepper.step_towards(curr, target, dt=0.5)
        self.assertFalse(reached)
        self.assertAlmostEqual(next_pose.x, 50.0)
        self.assertAlmostEqual(next_pose.y, 0.0)

    def test_reach_target(self) -> None:
        '''
            Verifies reaching target when step exceeds distance.

            :exceptions: None.
        '''
        stepper = EmulationStepper(speed_mm_per_sec=100.0)
        curr = ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)
        target = ScaraPose(x=10.0, y=0.0, z=0.0, phi=0.0)

        next_pose, reached = stepper.step_towards(curr, target, dt=0.5)
        self.assertTrue(reached)
        self.assertEqual(next_pose, target)

    def test_already_at_target(self) -> None:
        '''
            Verifies behavior when already at target.

            :exceptions: None.
        '''
        stepper = EmulationStepper(speed_mm_per_sec=100.0)
        curr = ScaraPose(x=50.0, y=20.0, z=5.0, phi=1.0)
        target = ScaraPose(x=50.0, y=20.0, z=5.0, phi=1.0)

        next_pose, reached = stepper.step_towards(curr, target, dt=0.1)
        self.assertTrue(reached)
        self.assertEqual(next_pose, target)

    def test_get_version(self) -> None:
        '''
            Verifies version string.

            :exceptions: None.
        '''
        stepper = EmulationStepper(speed_mm_per_sec=100.0)
        self.assertEqual(stepper.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
