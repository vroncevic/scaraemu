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
    Unit tests for VirtualBinaryFrameProcessorFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.emulation.provides import EmulationProvides
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.server.processor.dependencies import BinaryProcessorDependencies
from scaraemu.infrastructure.server.processor.factory import VirtualBinaryFrameProcessorFactory
from scaraemu.infrastructure.server.processor.processor import VirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyServerLogListener:
    '''
        Dummy server log listener for tests.
    '''

    def on_server_log(self, message: str) -> None:
        '''Handles server log.'''
        _ = message

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class VirtualBinaryFrameProcessorFactoryTestCase(TestCase):
    '''
        Unit tests for VirtualBinaryFrameProcessorFactory.

        It defines:

            :methods:
                | setUp - Prepares real service dependencies for factory methods.
                | test_create - Tests processor creation with explicit dependencies.
                | test_get_version - Tests factory version string retrieval.
    '''

    _emu_provides: EmulationProvides
    _kinematics: IManipulatorKinematics
    _log_listener: _DummyServerLogListener

    def setUp(self) -> None:
        '''
            Prepares real service dependencies for factory methods.

            :exceptions: None.
        '''
        self._kinematics = KinematicsAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds(),
            transmission=DefaultScaraProfile.create_transmission(),
        )
        initial_pose = ScaraPose(x=200.0, y=0.0, z=50.0, phi=0.0)
        emu_deps = EmulationDependencies(
            kinematics=self._kinematics,
            initial_pose=initial_pose,
        )
        self._emu_provides = EmulationFactory.create(dependencies=emu_deps)
        self._log_listener = _DummyServerLogListener()

    def test_create(self) -> None:
        '''
            Tests processor creation with explicit dependencies.

            :exceptions: None.
        '''
        response_builder: IBinaryResponseBuilderAdapter = (
            BinaryResponseBuilderAdapterFactory.create()
        )
        decoder: IBinaryPayloadDecoderAdapter = (
            BinaryPayloadDecoderAdapterFactory.create()
        )
        motion_validator = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        dependencies = BinaryProcessorDependencies(
            emulation_controller=self._emu_provides.controller,
            emulation_service=self._emu_provides.service,
            emulation_queue=self._emu_provides.queue,
            kinematics=self._kinematics,
            response_builder=response_builder,
            decoder=decoder,
            home_pose=ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0),
            motion_validator=motion_validator,
            log_listener=self._log_listener,
        )
        processor: VirtualBinaryFrameProcessor = (
            VirtualBinaryFrameProcessorFactory.create(
                dependencies=dependencies,
            )
        )
        self.assertIsInstance(processor, VirtualBinaryFrameProcessor)

    def test_get_version(self) -> None:
        '''
            Tests factory version string retrieval.

            :exceptions: None.
        '''
        version: str = VirtualBinaryFrameProcessorFactory.get_version()
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
