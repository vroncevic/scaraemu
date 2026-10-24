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
    Unit test cases for JogDependencies parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.gui.jog.action.dependencies import JogDependencies
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogDependenciesTestCase(TestCase):
    '''
        Unit tests for JogDependencies.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        mock_emulation = MagicMock(spec=IEmulationService)
        mock_queue = MagicMock(spec=IEmulationQueue)
        mock_validator = MagicMock(spec=IMotionValidatorAdapter)
        home_pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        mock_port = MagicMock(spec=IMotionCoordinator)
        mock_logger = MagicMock(spec=ILogListener)

        bundle = JogDependencies(
            emulation_service=mock_emulation,
            emulation_queue=mock_queue,
            validator=mock_validator,
            home_pose=home_pose,
            motion_port=mock_port,
            log_listener=mock_logger,
        )

        self.assertIs(bundle.emulation_service, mock_emulation)
        self.assertIs(bundle.emulation_queue, mock_queue)
        self.assertIs(bundle.validator, mock_validator)
        self.assertEqual(bundle.home_pose, home_pose)
        self.assertIs(bundle.motion_port, mock_port)
        self.assertIs(bundle.log_listener, mock_logger)


if __name__ == '__main__':
    unittest_main()
