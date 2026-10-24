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
    Unit test cases for BinaryProcessorDependencies value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.processor.dependencies import BinaryProcessorDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryProcessorDependenciesTestCase(TestCase):
    '''
        Unit tests for BinaryProcessorDependencies.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        controller = MagicMock(spec=IEmulationController)
        service = MagicMock(spec=IEmulationService)
        queue = MagicMock(spec=IEmulationQueue)
        kinematics = MagicMock(spec=IManipulatorKinematics)
        response_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        decoder = MagicMock(spec=IBinaryPayloadDecoderAdapter)
        home_pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        motion_validator = MagicMock(spec=IMotionValidatorAdapter)
        log_listener = MagicMock(spec=IServerLogListener)

        bundle = BinaryProcessorDependencies(
            emulation_controller=controller,
            emulation_service=service,
            emulation_queue=queue,
            kinematics=kinematics,
            response_builder=response_builder,
            decoder=decoder,
            home_pose=home_pose,
            motion_validator=motion_validator,
            log_listener=log_listener,
        )

        self.assertIs(bundle.emulation_controller, controller)
        self.assertIs(bundle.emulation_service, service)
        self.assertIs(bundle.emulation_queue, queue)
        self.assertIs(bundle.kinematics, kinematics)
        self.assertIs(bundle.response_builder, response_builder)
        self.assertIs(bundle.decoder, decoder)
        self.assertEqual(bundle.home_pose, home_pose)
        self.assertIs(bundle.motion_validator, motion_validator)
        self.assertIs(bundle.log_listener, log_listener)


if __name__ == '__main__':
    unittest_main()
