# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Coordinates machine kinematic configuration and motor power state actions.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigurationCoordinator:
    '''
        Coordinates machine kinematic configuration switching and motor power toggling.

        It defines:

            :attributes:
                | _emulation_controller - Manipulator mode and safety state controller.
                | _command_port - Hardware bridge command port.
                | _log_listener - Logging sink for host diagnostics.
            :methods:
                | __init__ - Initializes configuration coordinator with controllers and ports.
                | handle_toggle_elbow - Toggles between Lefty and Righty elbow configurations.
                | handle_toggle_motors - Toggles motor driver power state.
                | get_version - Returns coordinator component version string.
    '''

    _emulation_controller: IEmulationController
    _command_port: ICommandDispatcher
    _log_listener: ILogListener

    def __init__(
        self,
        *,
        emulation_controller: IEmulationController,
        command_port: ICommandDispatcher,
        log_listener: ILogListener,
    ) -> None:
        '''
            Initializes configuration coordinator with controllers and ports.

            :param emulation_controller: Mode and safety state controller.
            :param command_port: Hardware bridge command port.
            :param log_listener: Logging listener for host diagnostics.
            :exceptions: None.
        '''
        self._emulation_controller: Final[IEmulationController] = (
            emulation_controller
        )
        self._command_port: Final[ICommandDispatcher] = command_port
        self._log_listener: Final[ILogListener] = log_listener

    def handle_toggle_elbow(self) -> None:
        '''
            Toggles between Lefty and Righty elbow configurations.

            :exceptions: None.
        '''
        flags: EmulationFlags = self._emulation_controller.get_flags()
        curr_left: bool = flags.elbow_left
        new_left: bool = not curr_left
        self._emulation_controller.set_elbow_mode(new_left)
        mode_str: str = 'Lefty' if new_left else 'Righty'
        self._log_listener.append_log(
            f'[HOST]: Switched to {mode_str} configuration', 'info'
        )

    def handle_toggle_motors(self) -> None:
        '''
            Toggles motor driver power enable.

            :exceptions: None.
        '''
        flags: EmulationFlags = self._emulation_controller.get_flags()
        curr_state: bool = flags.motors_enabled
        new_state: bool = not curr_state
        self._emulation_controller.set_motors_enabled(new_state)
        msg_id: MessageId = (
            MessageId.CMD_ENABLE if new_state else MessageId.CMD_DISABLE
        )
        self._command_port.send_command(msg_id)

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
