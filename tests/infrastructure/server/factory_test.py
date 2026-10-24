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
    Unit tests for ServerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.server.dependencies import ServerDependencies
from scaraemu.infrastructure.server.factory import ServerFactory
from scaraemu.infrastructure.server.iserver import IVirtualManipulatorServer
from scaraemu.infrastructure.server.logger.iholder import IServerLogListenerHolder
from scaraemu.infrastructure.server.provides import ServerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerFactory(TestCase):
    '''
        Test cases for ServerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates ServerProvides.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory instantiates ServerProvides with server and log holder.

            :exceptions: None.
        '''
        kin: IManipulatorKinematics = KinematicsAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds(),
            transmission=DefaultScaraProfile.create_transmission(),
        )
        initial_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        emu_deps = EmulationDependencies(
            kinematics=kin,
            initial_pose=initial_pose,
        )
        emu = EmulationFactory.create(dependencies=emu_deps)
        motion_validator = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        dependencies = ServerDependencies(
            emulation_controller=emu.controller,
            emulation_service=emu.service,
            emulation_queue=emu.queue,
            motion_notifier=emu.notifier,
            home_pose=initial_pose,
            kinematics=kin,
            motion_validator=motion_validator,
            response_builder=BinaryResponseBuilderAdapterFactory.create(),
            codec=BinaryFrameCodecAdapterFactory.create(),
            decoder=BinaryPayloadDecoderAdapterFactory.create(),
        )

        provides: ServerProvides = ServerFactory.create(
            dependencies=dependencies,
        )
        self.assertIsNotNone(provides)
        self.assertIsInstance(provides.server, IVirtualManipulatorServer)
        self.assertIsInstance(provides.log_holder, IServerLogListenerHolder)
        self.assertFalse(provides.server.is_running())

    def test_get_version(self) -> None:
        '''
            Verifies factory returns version string.

            :exceptions: None.
        '''
        version = ServerFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
