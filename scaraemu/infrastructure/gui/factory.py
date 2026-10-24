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
    Factory instantiating GUI presentation subsystem.
'''

from __future__ import annotations

from scaraemu.infrastructure.connection.dependencies import ConnectionDependencies
from scaraemu.infrastructure.connection.factory import ConnectionFactory
from scaraemu.infrastructure.connection.provides import ConnectionProvides
from scaraemu.infrastructure.streaming.dependencies import StreamingDependencies
from scaraemu.infrastructure.streaming.factory import StreamingFactory
from scaraemu.infrastructure.streaming.provides import StreamingProvides
from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.bridge.factory import BridgeFactory
from scaraemu.infrastructure.gui.delegates.assembly import GuiDelegatesAssembly
from scaraemu.infrastructure.gui.delegates.dependencies import DelegatesDependencies
from scaraemu.infrastructure.gui.delegates.factory import GuiDelegatesFactory
from scaraemu.infrastructure.gui.dependencies import GuiDependencies
from scaraemu.infrastructure.gui.engine import ScaraEmuGUI
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.gui.layout.builder.builder import LayoutBuilder
from scaraemu.infrastructure.gui.layout.builder.dependencies import LayoutDependencies
from scaraemu.infrastructure.gui.layout.builder.factory import LayoutBuilderFactory
from scaraemu.infrastructure.gui.lifecycle.runner import GuiLifecycleRunner
from scaraemu.infrastructure.gui.lifecycle.factory import GuiLifecycleRunnerFactory
from scaraemu.infrastructure.gui.provides import GuiProvides
from scaraemu.infrastructure.gui.window.factory import WindowConfiguratorFactory
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiFactory:
    '''
        Factory providing configured GUI presentation subsystem instances.

        It defines:

            :methods:
                | create - Assembles and returns GuiProvides with collaborators.
                | get_version - Returns factory component version.
    '''

    @classmethod
    def create(cls, dependencies: GuiDependencies) -> GuiProvides:
        '''
            Assembles GUI collaborators and returns a wired GuiProvides instance.

            :param dependencies: Encapsulated GUI dependencies and parameters.
            :return: Fully wired GuiProvides instance exposing IGUI.
            :exceptions: None.
        '''
        layout_deps = LayoutDependencies(
            port_scanner=dependencies.services.port_scanner,
            preference_repository=dependencies.services.preferences.serial,
            manipulator_linkage_adapter=dependencies.services.scaralang.linkage,
            reach_adapter=dependencies.services.scaralang.reach,
            boundary_service=dependencies.services.scaralang.boundary,
        )
        layout_builder: LayoutBuilder = LayoutBuilderFactory.create(
            dependencies=layout_deps
        )

        adapters: BridgeProvides = BridgeFactory.create(
            layout_builder=layout_builder,
            server_log_holder=dependencies.services.server.log_holder,
        )

        streaming_deps = StreamingDependencies(
            transport=dependencies.services.transport,
            log_listener=adapters.log_listener,
            kinematics=dependencies.services.kinematics,
            codec=dependencies.services.scaralang.codec,
        )
        streaming: StreamingProvides = StreamingFactory.create(
            dependencies=streaming_deps
        )

        connection_deps = ConnectionDependencies(
            transport=dependencies.services.transport,
            bridge_synchronizer=adapters.bridge_synchronizer,
            log_listener=adapters.log_listener,
            codec=dependencies.services.scaralang.codec,
            response_decoder=dependencies.services.scaralang.response_decoder,
            kinematics=dependencies.services.kinematics,
            streamer=streaming.streamer,
        )
        connection: ConnectionProvides = ConnectionFactory.create(
            dependencies=connection_deps
        )

        delegates_deps = DelegatesDependencies(
            bounds=dependencies.bounds,
            services=dependencies.services,
            adapters=adapters,
            connection=connection,
            streaming=streaming,
        )
        delegates_assembly: GuiDelegatesAssembly = GuiDelegatesFactory.create(
            dependencies=delegates_deps,
        )

        configurator: IWindowConfigurator = WindowConfiguratorFactory.create()
        lifecycle_runner: GuiLifecycleRunner = (
            GuiLifecycleRunnerFactory.create(
                emulation_service=dependencies.services.emulation_service,
                window_configurator=configurator,
            )
        )

        gui: IGUI = ScaraEmuGUI(
            bounds=dependencies.bounds,
            target_click_listener=delegates_assembly.target_click_coordinator,
            delegates=delegates_assembly.delegates,
            server_manager=delegates_assembly.server_manager,
            layout_builder=layout_builder,
            lifecycle_runner=lifecycle_runner,
            initial_script=dependencies.initial_script,
        )

        return GuiProvides(gui=gui)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
