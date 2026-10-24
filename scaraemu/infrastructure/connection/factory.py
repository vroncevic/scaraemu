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
    Factory creating and configuring the hardware connection subsystem.
'''

from __future__ import annotations

from scaracom.bridge.dependencies import BridgeDependencies as ScaracomBridgeDependencies
from scaracom.bridge.factory import BridgeFactory as ScaracomBridgeFactory
from scaracom.bridge.provides import BridgeProvides as ScaracomBridgeProvides

from scaraemu.infrastructure.connection.command.dependencies import CommandDependencies
from scaraemu.infrastructure.connection.command.factory import CommandDispatcherFactory
from scaraemu.infrastructure.connection.coordinator.dependencies import CoordinatorDependencies
from scaraemu.infrastructure.connection.coordinator.factory import ConnectionCoordinatorFactory
from scaraemu.infrastructure.connection.dependencies import ConnectionDependencies
from scaraemu.infrastructure.connection.handler.dependencies import HandlerDependencies
from scaraemu.infrastructure.connection.handler.factory import ResponseHandlerFactory
from scaraemu.infrastructure.connection.listener.dependencies import ListenerDependencies
from scaraemu.infrastructure.connection.listener.factory import ConnectionTransportListenerFactory
from scaraemu.infrastructure.connection.provides import ConnectionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionFactory:
    '''
        Factory creating and configuring the hardware connection subsystem.

        It defines:

            :methods:
                | create - Instantiates and connects connection subsystem components.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ConnectionDependencies) -> ConnectionProvides:
        '''
            Instantiates and connects connection subsystem components.

            :param dependencies: Hardware connection subsystem parameter bundle.
            :return: Wired connection subsystem provides bundle.
            :exceptions: None.
        '''
        command_dependencies = CommandDependencies(
            transport=dependencies.transport,
            log_listener=dependencies.log_listener,
            streamer=dependencies.streamer,
            codec=dependencies.codec,
        )
        command_dispatcher = CommandDispatcherFactory.create(
            dependencies=command_dependencies
        )

        response_dependencies = HandlerDependencies(
            listener=dependencies.bridge_synchronizer,
            log_listener=dependencies.log_listener,
            streamer=dependencies.streamer,
            codec=dependencies.codec,
            kinematics=dependencies.kinematics,
            response_decoder=dependencies.response_decoder,
        )
        response_handler = ResponseHandlerFactory.create(
            dependencies=response_dependencies
        )

        listener_dependencies = ListenerDependencies(
            handler=response_handler,
            synchronizer=dependencies.bridge_synchronizer,
        )
        connection_listener = ConnectionTransportListenerFactory.create(
            dependencies=listener_dependencies
        )

        scaracom_bridge: ScaracomBridgeProvides = ScaracomBridgeFactory.create(
            dependencies=ScaracomBridgeDependencies(
                transport=dependencies.transport,
                listener=connection_listener,
            )
        )

        coordinator_dependencies = CoordinatorDependencies(
            connection=scaracom_bridge.coordinator,
            listener=dependencies.bridge_synchronizer,
            streamer=dependencies.streamer,
            command_dispatcher=command_dispatcher,
        )
        coordinator = ConnectionCoordinatorFactory.create(
            dependencies=coordinator_dependencies
        )

        return ConnectionProvides(
            coordinator=coordinator,
            command_dispatcher=command_dispatcher,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
        '''
        return __version__
