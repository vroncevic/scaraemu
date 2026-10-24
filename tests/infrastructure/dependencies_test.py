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
    Unit tests for InfrastructureDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.context.bundle import ContextBundle
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.dependencies import InfrastructureDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfrastructureDependencies(TestCase):
    '''
        Test cases verifying InfrastructureDependencies.

        It defines:

            :methods:
                | test_dependencies_instantiation - Verifies dataclass properties.
    '''

    def test_dependencies_instantiation(self) -> None:
        '''
            Verifies dataclass properties.

            :exceptions: None.
        '''
        mock_base = MagicMock(spec=BaseBundle)
        mock_context = MagicMock(spec=ContextBundle)
        mock_bounds = MagicMock(spec=ScaraBounds)
        mock_kinematics = MagicMock(spec=IManipulatorKinematics)
        mock_emulation = MagicMock(spec=IEmulationService)
        mock_controller = MagicMock(spec=IEmulationController)
        mock_queue = MagicMock(spec=IEmulationQueue)
        mock_notifier = MagicMock(spec=IMotionNotifier)
        mock_pose = MagicMock(spec=ScaraPose)

        deps = InfrastructureDependencies(
            base_bundle=mock_base,
            context_bundle=mock_context,
            bounds=mock_bounds,
            kinematics=mock_kinematics,
            emulation_service=mock_emulation,
            emulation_controller=mock_controller,
            emulation_queue=mock_queue,
            motion_notifier=mock_notifier,
            home_pose=mock_pose,
            initial_script_path='/tmp/test.scara',
        )

        self.assertIs(deps.base_bundle, mock_base)
        self.assertIs(deps.context_bundle, mock_context)
        self.assertIs(deps.bounds, mock_bounds)
        self.assertIs(deps.kinematics, mock_kinematics)
        self.assertIs(deps.emulation_service, mock_emulation)
        self.assertIs(deps.emulation_controller, mock_controller)
        self.assertIs(deps.emulation_queue, mock_queue)
        self.assertIs(deps.motion_notifier, mock_notifier)
        self.assertIs(deps.home_pose, mock_pose)
        self.assertEqual(deps.initial_script_path, '/tmp/test.scara')


if __name__ == '__main__':
    unittest_main()
