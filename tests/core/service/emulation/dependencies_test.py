# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit test cases for EmulationDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationDependenciesTestCase(TestCase):
    '''
        Test case verifying EmulationDependencies dataclass behavior.

        It defines:

            :methods:
                | test_initialization - Verifies initialization of properties.
                | test_immutability - Verifies frozen dataclass immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies initialization of properties.

            :exceptions: None.
        '''
        kinematics = MagicMock(spec=IManipulatorKinematics)
        pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        deps = EmulationDependencies(
            kinematics=kinematics,
            initial_pose=pose,
            speed_mm_per_sec=120.0,
        )
        self.assertEqual(deps.kinematics, kinematics)
        self.assertEqual(deps.initial_pose, pose)
        self.assertEqual(deps.speed_mm_per_sec, 120.0)

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass immutability.

            :exceptions: None.
        '''
        kinematics = MagicMock(spec=IManipulatorKinematics)
        pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        deps = EmulationDependencies(
            kinematics=kinematics,
            initial_pose=pose,
        )
        with self.assertRaises(AttributeError):
            deps.speed_mm_per_sec = 200.0  # type: ignore[misc]


if __name__ == '__main__':
    unittest_main()
