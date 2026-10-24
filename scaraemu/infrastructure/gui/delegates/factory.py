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
    Factory creating and assembling GUI action delegates and coordinators.
'''

from __future__ import annotations

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.target.elbow_auto_switch_coordinator import ElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.elbow_dependencies import ElbowDependencies
from scaraemu.infrastructure.gui.canvas.target.target_action_coordinator import TargetActionCoordinator
from scaraemu.infrastructure.gui.canvas.target.target_dependencies import TargetDependencies
from scaraemu.infrastructure.gui.canvas.target.target_motion_dispatcher import TargetMotionDispatcher
from scaraemu.infrastructure.gui.delegates.assembly import GuiDelegatesAssembly
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.delegates.dependencies import DelegatesDependencies
from scaraemu.infrastructure.gui.jog.action.coordinator import JogActionCoordinator
from scaraemu.infrastructure.gui.jog.action.dependencies import JogDependencies
from scaraemu.infrastructure.gui.machine.configuration.coordinator import ConfigurationCoordinator
from scaraemu.infrastructure.gui.machine.safety.coordinator import SafetyCoordinator
from scaraemu.infrastructure.gui.toolbar.action.coordinator import ActionCoordinator as ToolbarActionCoordinator
from scaraemu.infrastructure.gui.trajectory.preset.coordinator import TrajectoryPresetCoordinator
from scaraemu.infrastructure.gui.trajectory.queue.coordinator import QueueActionCoordinator
from scaraemu.infrastructure.gui.trajectory.script.coordinator import ScriptLoaderCoordinator
from scaraemu.infrastructure.server.manager.manager import VirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiDelegatesFactory:
    '''
        Factory creating and assembling GUI action delegates and coordinators.

        It defines:

            :methods:
                | create - Instantiates and wires all GUI delegates and coordinators.
                | get_version - Returns factory component version.
    '''

    @classmethod
    def create(
        cls,
        dependencies: DelegatesDependencies,
    ) -> GuiDelegatesAssembly:
        '''
            Instantiates and wires all GUI delegates and coordinators.

            :param dependencies: Collaborating bounds, services, adapters, and bridge parameter bundle.
            :return: Assembled GUI delegates and coordinators.
            :exceptions: None.
        '''
        services = dependencies.services
        adapters = dependencies.adapters
        connection = dependencies.connection
        streaming = dependencies.streaming

        server_manager: VirtualServerManager = VirtualServerManager(
            server=services.server.server,
            log_listener=adapters.server_log_listener,
            state_listener=adapters.server_state_listener,
        )

        toolbar_coordinator: ToolbarActionCoordinator = ToolbarActionCoordinator(
            connection_port=connection.coordinator,
            server_manager=server_manager,
            serial_preferences=services.preferences.serial,
            server_preferences=services.preferences.server,
        )

        queue_coordinator: QueueActionCoordinator = QueueActionCoordinator(
            command_port=connection.command_dispatcher,
            emulation_queue=services.emulation_queue,
            emulation_service=services.emulation_service,
        )

        elbow_deps = ElbowDependencies(
            emulation_controller=services.emulation_controller,
            kinematics=services.kinematics,
            log_listener=adapters.log_listener,
        )
        elbow_coordinator: ElbowAutoSwitchCoordinator = (
            ElbowAutoSwitchCoordinator(dependencies=elbow_deps)
        )

        motion_dispatcher: TargetMotionDispatcher = (
            TargetMotionDispatcher(
                emulation_queue=services.emulation_queue,
                motion_port=streaming.motion_coordinator,
            )
        )

        target_deps = TargetDependencies(
            emulation_service=services.emulation_service,
            validator=services.scaralang.safety,
            elbow_coordinator=elbow_coordinator,
            bypass_adapter=services.scaralang.bypass,
            motion_dispatcher=motion_dispatcher,
            log_listener=adapters.log_listener,
        )
        target_click_coordinator: TargetActionCoordinator = (
            TargetActionCoordinator(dependencies=target_deps)
        )

        home_pose: ScaraPose = services.scaralang.reach.calculate_home_pose()

        jog_deps = JogDependencies(
            emulation_service=services.emulation_service,
            emulation_queue=services.emulation_queue,
            validator=services.scaralang.safety,
            home_pose=home_pose,
            motion_port=streaming.motion_coordinator,
            log_listener=adapters.log_listener,
        )
        jog_coordinator: JogActionCoordinator = JogActionCoordinator(
            dependencies=jog_deps
        )

        config_coordinator: ConfigurationCoordinator = ConfigurationCoordinator(
            emulation_controller=services.emulation_controller,
            command_port=connection.command_dispatcher,
            log_listener=adapters.log_listener,
        )

        safety_coordinator: SafetyCoordinator = SafetyCoordinator(
            emulation_controller=services.emulation_controller,
            emulation_queue=services.emulation_queue,
            command_port=connection.command_dispatcher,
        )

        preset_coordinator: TrajectoryPresetCoordinator = TrajectoryPresetCoordinator(
            emulation_service=services.emulation_service,
            emulation_queue=services.emulation_queue,
            motion_port=streaming.motion_coordinator,
            demo_adapter=services.scaralang.demo,
        )

        script_coordinator: ScriptLoaderCoordinator = ScriptLoaderCoordinator(
            script_loader=services.scaralang.script,
            emulation_queue=services.emulation_queue,
            motion_port=streaming.motion_coordinator,
            log_listener=adapters.log_listener,
        )

        delegates: GuiDelegatesBundle = GuiDelegatesBundle(
            jog=jog_coordinator,
            config=config_coordinator,
            safety=safety_coordinator,
            preset=preset_coordinator,
            script=script_coordinator,
            serial_bar=toolbar_coordinator,
            queue=queue_coordinator,
        )

        return GuiDelegatesAssembly(
            delegates=delegates,
            target_click_coordinator=target_click_coordinator,
            server_manager=server_manager,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
