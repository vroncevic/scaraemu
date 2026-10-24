# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for KinematicsProvides.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.setup.kinematics.provides import KinematicsProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsProvides(TestCase):
    '''
        Test cases verifying KinematicsProvides.

        It defines:

            :methods:
                | test_provides_creation - Verifies provides properties.
    '''

    def test_provides_creation(self) -> None:
        '''
            Verifies provides properties.

            :exceptions: None.
        '''
        mock_bounds: ScaraBounds = MagicMock(spec=ScaraBounds)
        mock_kinematics: IManipulatorKinematics = MagicMock(spec=IManipulatorKinematics)
        mock_home_pose: ScaraPose = MagicMock(spec=ScaraPose)

        provides = KinematicsProvides(
            bounds=mock_bounds,
            kinematics=mock_kinematics,
            home_pose=mock_home_pose,
        )

        self.assertIs(provides.bounds, mock_bounds)
        self.assertIs(provides.kinematics, mock_kinematics)
        self.assertIs(provides.home_pose, mock_home_pose)


if __name__ == '__main__':
    unittest_main()
