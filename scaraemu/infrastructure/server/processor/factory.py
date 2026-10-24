# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating IVirtualBinaryFrameProcessor implementations.
'''

from __future__ import annotations

from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler
from scaraemu.infrastructure.server.handler.jog.dependencies import JogHandlerDependencies
from scaraemu.infrastructure.server.handler.jog.factory import JogHandlerFactory
from scaraemu.infrastructure.server.handler.motion.dependencies import MotionHandlerDependencies
from scaraemu.infrastructure.server.handler.motion.factory import MotionHandlerFactory
from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies
from scaraemu.infrastructure.server.handler.system.factory import SystemHandlerFactory
from scaraemu.infrastructure.server.handler.tool.dependencies import ToolHandlerDependencies
from scaraemu.infrastructure.server.handler.tool.factory import ToolHandlerFactory
from scaraemu.infrastructure.server.pose.factory import VirtualPlannedPoseHolderFactory
from scaraemu.infrastructure.server.pose.holder import VirtualPlannedPoseHolder
from scaraemu.infrastructure.server.processor.dependencies import BinaryProcessorDependencies
from scaraemu.infrastructure.server.processor.processor import VirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualBinaryFrameProcessorFactory:
    '''
        Factory providing VirtualBinaryFrameProcessor instances.

        It defines:

            :methods:
                | create - Builds dedicated handlers and returns a processor instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: BinaryProcessorDependencies,
    ) -> VirtualBinaryFrameProcessor:
        '''
            Builds dedicated handlers and returns a VirtualBinaryFrameProcessor instance.

            :param dependencies: Injected BinaryProcessorDependencies instance.
            :return: VirtualBinaryFrameProcessor instance.
            :exceptions: None.
        '''
        decoder: IBinaryPayloadDecoderAdapter = dependencies.decoder
        system_deps = SystemHandlerDependencies(
            emulation_controller=dependencies.emulation_controller,
            emulation_queue=dependencies.emulation_queue,
            response_builder=dependencies.response_builder,
            home_pose=dependencies.home_pose,
        )
        pose_holder: VirtualPlannedPoseHolder = (
            VirtualPlannedPoseHolderFactory.create()
        )
        motion_deps = MotionHandlerDependencies(
            emulation_service=dependencies.emulation_service,
            emulation_queue=dependencies.emulation_queue,
            pose_holder=pose_holder,
            kinematics=dependencies.kinematics,
            validator=dependencies.motion_validator,
            response_builder=dependencies.response_builder,
            decoder=decoder,
            log_listener=dependencies.log_listener,
        )
        jog_deps = JogHandlerDependencies(
            emulation_service=dependencies.emulation_service,
            emulation_queue=dependencies.emulation_queue,
            pose_holder=pose_holder,
            kinematics=dependencies.kinematics,
            response_builder=dependencies.response_builder,
            decoder=decoder,
        )
        tool_deps = ToolHandlerDependencies(
            response_builder=dependencies.response_builder,
            decoder=decoder,
        )
        handlers: list[IBinaryCommandHandler] = [
            SystemHandlerFactory.create(dependencies=system_deps),
            MotionHandlerFactory.create(dependencies=motion_deps),
            JogHandlerFactory.create(dependencies=jog_deps),
            ToolHandlerFactory.create(dependencies=tool_deps),
        ]

        return VirtualBinaryFrameProcessor(
            handlers=handlers,
            response_builder=dependencies.response_builder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
