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
    Coordinates machine emergency stop and feed-hold pause safety actions.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SafetyCoordinator:
    '''
        Coordinates emergency stop operations, feed-hold pausing, and motion queue flushing.

        It defines:

            :attributes:
                | _emulation_controller - Manipulator mode and safety state controller.
                | _emulation_queue - FIFO motion emulation queue.
                | _command_port - Hardware bridge command port.
            :methods:
                | __init__ - Initializes safety coordinator with controller, queue, and port.
                | handle_toggle_hold - Toggles feed-hold pause state across emulator and bridge.
                | handle_estop - Executes emergency stop and flushes motion queues.
                | get_version - Returns coordinator component version string.
    '''

    _emulation_controller: IEmulationController
    _emulation_queue: IEmulationQueue
    _command_port: ICommandDispatcher

    def __init__(
        self,
        *,
        emulation_controller: IEmulationController,
        emulation_queue: IEmulationQueue,
        command_port: ICommandDispatcher,
    ) -> None:
        '''
            Initializes safety coordinator with controller, queue, and command port.

            :param emulation_controller: Mode and safety state controller.
            :param emulation_queue: FIFO motion emulation queue.
            :param command_port: Hardware bridge command port.
            :exceptions: None.
        '''
        self._emulation_controller: Final[IEmulationController] = (
            emulation_controller
        )
        self._emulation_queue: Final[IEmulationQueue] = emulation_queue
        self._command_port: Final[ICommandDispatcher] = command_port

    def handle_toggle_hold(self) -> None:
        '''
            Toggles feed-hold pause state across emulator and bridge.

            :exceptions: None.
        '''
        flags: EmulationFlags = self._emulation_controller.get_flags()
        held: bool = not flags.hold_active
        self._emulation_controller.set_hold(held)

        if held:
            self._command_port.send_command(MessageId.CMD_HOLD)
        else:
            self._command_port.send_command(MessageId.CMD_RESUME)

    def handle_estop(self) -> None:
        '''
            Executes emergency stop.

            :exceptions: None.
        '''
        self._emulation_controller.set_estop(True)
        self._emulation_queue.clear_queue()
        self._command_port.clear_queue()
        self._command_port.send_command(MessageId.CMD_ESTOP)

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
