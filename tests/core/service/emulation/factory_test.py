# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit test cases for EmulationFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.provides import EmulationProvides
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationFactoryTestCase(TestCase):
    '''
        Test case verifying behavior of EmulationFactory.

        It defines:

            :methods:
                | test_create - Verifies creation of EmulationProvides container.
                | test_get_version - Verifies component version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies creation of EmulationProvides container.

            :exceptions: None.
        '''
        kinematics = MagicMock(spec=IManipulatorKinematics)
        kinematics.solve_ik.return_value = ScaraJoints(
            theta1=0.0, theta2=0.0, z=20.0, theta4=0.0, reachable=True
        )
        pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        deps = EmulationDependencies(
            kinematics=kinematics,
            initial_pose=pose,
            speed_mm_per_sec=50.0,
        )
        provides = EmulationFactory.create(dependencies=deps)
        self.assertIsInstance(provides, EmulationProvides)
        self.assertIsInstance(provides.service, IEmulationService)
        self.assertIsInstance(provides.controller, IEmulationController)
        self.assertIsInstance(provides.queue, IEmulationQueue)
        self.assertIsInstance(provides.notifier, IMotionNotifier)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        self.assertEqual(EmulationFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
