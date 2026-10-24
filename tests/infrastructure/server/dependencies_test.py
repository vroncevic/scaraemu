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
    Unit test cases for ServerDependencies value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.server.dependencies import ServerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerDependenciesTestCase(TestCase):
    '''
        Unit tests for ServerDependencies.

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
        notifier = MagicMock(spec=IMotionNotifier)
        home_pose = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        kinematics = MagicMock(spec=IManipulatorKinematics)
        motion_validator = MagicMock(spec=IMotionValidatorAdapter)
        response_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        decoder = MagicMock(spec=IBinaryPayloadDecoderAdapter)

        bundle = ServerDependencies(
            emulation_controller=controller,
            emulation_service=service,
            emulation_queue=queue,
            motion_notifier=notifier,
            home_pose=home_pose,
            kinematics=kinematics,
            motion_validator=motion_validator,
            response_builder=response_builder,
            codec=codec,
            decoder=decoder,
        )

        self.assertIs(bundle.emulation_controller, controller)
        self.assertIs(bundle.emulation_service, service)
        self.assertIs(bundle.emulation_queue, queue)
        self.assertIs(bundle.motion_notifier, notifier)
        self.assertEqual(bundle.home_pose, home_pose)
        self.assertIs(bundle.kinematics, kinematics)
        self.assertIs(bundle.motion_validator, motion_validator)
        self.assertIs(bundle.response_builder, response_builder)
        self.assertIs(bundle.codec, codec)
        self.assertIs(bundle.decoder, decoder)


if __name__ == '__main__':
    unittest_main()
