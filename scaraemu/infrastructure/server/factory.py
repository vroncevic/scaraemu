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
    Subsystem factory instantiating and wiring virtual manipulator server components.
'''

from __future__ import annotations

from scaraemu.infrastructure.server.accept.factory import ServerAcceptWorkerFactory
from scaraemu.infrastructure.server.accept.worker import ServerAcceptWorker
from scaraemu.infrastructure.server.dependencies import ServerDependencies
from scaraemu.infrastructure.server.dispatcher.dispatcher import ServerFrameDispatcher
from scaraemu.infrastructure.server.dispatcher.factory import ServerFrameDispatcherFactory
from scaraemu.infrastructure.server.logger.factory import ServerLogListenerHolderFactory
from scaraemu.infrastructure.server.logger.holder import ServerLogListenerHolder
from scaraemu.infrastructure.server.motion_completion_listener import ServerMotionCompletionListener
from scaraemu.infrastructure.server.processor.dependencies import BinaryProcessorDependencies
from scaraemu.infrastructure.server.processor.factory import VirtualBinaryFrameProcessorFactory
from scaraemu.infrastructure.server.processor.processor import VirtualBinaryFrameProcessor
from scaraemu.infrastructure.server.provides import ServerProvides
from scaraemu.infrastructure.server.server import VirtualManipulatorServer
from scaraemu.infrastructure.server.session.dependencies import SessionDependencies
from scaraemu.infrastructure.server.session.factory import ClientSessionWorkerFactory
from scaraemu.infrastructure.server.session.outbound_queue import OutboundFrameQueue
from scaraemu.infrastructure.server.session.worker import ClientSessionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerFactory:
    '''
        Factory providing assembled virtual manipulator server subsystem.

        It defines:

            :methods:
                | create - Builds and wires virtual manipulator server subsystem.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ServerDependencies) -> ServerProvides:
        '''
            Builds and wires virtual manipulator server subsystem.

            :param dependencies: Encapsulated server foreign dependencies bundle.
            :return: Assembled ServerProvides container.
            :exceptions: None.
        '''
        log_holder: ServerLogListenerHolder = ServerLogListenerHolderFactory.create()
        outbound_queue = OutboundFrameQueue()
        completion_listener = ServerMotionCompletionListener(
            outbound_queue=outbound_queue,
            response_builder=dependencies.response_builder,
            codec=dependencies.codec,
            log_listener=log_holder,
        )
        dependencies.motion_notifier.set_completion_listener(completion_listener)

        processor_deps = BinaryProcessorDependencies(
            emulation_controller=dependencies.emulation_controller,
            emulation_service=dependencies.emulation_service,
            emulation_queue=dependencies.emulation_queue,
            kinematics=dependencies.kinematics,
            response_builder=dependencies.response_builder,
            decoder=dependencies.decoder,
            home_pose=dependencies.home_pose,
            motion_validator=dependencies.motion_validator,
            log_listener=log_holder,
        )
        processor: VirtualBinaryFrameProcessor = (
            VirtualBinaryFrameProcessorFactory.create(
                dependencies=processor_deps,
            )
        )
        dispatcher: ServerFrameDispatcher = ServerFrameDispatcherFactory.create(
            binary_processor=processor,
            codec=dependencies.codec,
        )
        session_deps = SessionDependencies(
            dispatcher=dispatcher,
            log_listener=log_holder,
            outbound_queue=outbound_queue,
        )
        session_worker: ClientSessionWorker = ClientSessionWorkerFactory.create(
            dependencies=session_deps,
        )
        accept_worker: ServerAcceptWorker = ServerAcceptWorkerFactory.create(
            session_worker=session_worker,
            log_listener=log_holder,
        )
        server = VirtualManipulatorServer(
            accept_worker=accept_worker,
            dispatcher=dispatcher,
            log_listener=log_holder,
        )

        return ServerProvides(
            server=server,
            log_holder=log_holder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
        '''
        return __version__
