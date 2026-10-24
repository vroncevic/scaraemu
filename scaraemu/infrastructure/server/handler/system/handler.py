# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Handler for binary system lifecycle, estop, homing, and ping frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SystemHandler:
    '''
        Processes system lifecycle, estop, homing, and ping binary frames.

        It defines:

            :attributes:
                | _emulation_controller - Injected emulation mode and safety controller.
                | _emulation_queue - Injected waypoint queue service.
                | _response_builder - Injected binary frame builder for wire responses.
                | _home_pose - Manipulator canonical home pose.
            :methods:
                | __init__ - Initializes system binary handler with dependencies bundle.
                | can_handle - Checks whether message ID is a system command.
                | handle - Executes system command and returns response frames.
                | get_version - Returns handler component version string.
    '''

    _emulation_controller: IEmulationController
    _emulation_queue: IEmulationQueue
    _response_builder: IBinaryResponseBuilderAdapter
    _home_pose: ScaraPose

    def __init__(
        self,
        *,
        dependencies: SystemHandlerDependencies,
    ) -> None:
        '''
            Initializes system binary handler with dependencies bundle.

            :param dependencies: Injected SystemHandlerDependencies instance.
            :exceptions: None.
        '''
        self._emulation_controller: Final[IEmulationController] = dependencies.emulation_controller
        self._emulation_queue: Final[IEmulationQueue] = dependencies.emulation_queue
        self._response_builder: Final[IBinaryResponseBuilderAdapter] = (
            dependencies.response_builder
        )
        self._home_pose: Final[ScaraPose] = dependencies.home_pose

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Checks whether message ID is a system command.

            :param msg_id: MessageId enum value to check.
            :return: True if handled by this handler, False otherwise.
            :exceptions: None.
        '''
        return msg_id in (
            MessageId.CMD_PING,
            MessageId.CMD_HOME,
            MessageId.CMD_ENABLE,
            MessageId.CMD_DISABLE,
            MessageId.CMD_ESTOP,
            MessageId.CMD_CLEAR_FAULT,
        )

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Executes system command and returns response frames.

            :param frame: Inbound BinaryFrame instance.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''
        free_slots: int = max(
            0, 16 - self._emulation_queue.get_snapshot(self._home_pose).queue_depth
        )
        resp_cmd: MessageId
        slots: int = free_slots

        match frame.msg_id:
            case MessageId.CMD_PING:
                resp_cmd = MessageId.CMD_PING

            case MessageId.CMD_HOME:
                self._emulation_queue.enqueue_waypoint(self._home_pose)
                resp_cmd = MessageId.CMD_HOME

            case MessageId.CMD_ENABLE:
                self._emulation_controller.set_motors_enabled(True)
                resp_cmd = MessageId.CMD_ENABLE

            case MessageId.CMD_DISABLE:
                self._emulation_controller.set_motors_enabled(False)
                resp_cmd = MessageId.CMD_DISABLE

            case MessageId.CMD_ESTOP:
                self._emulation_queue.clear_queue()
                self._emulation_controller.set_estop(True)
                resp_cmd = frame.msg_id
                slots = 16

            case MessageId.CMD_CLEAR_FAULT:
                self._emulation_controller.set_estop(False)
                resp_cmd = MessageId.CMD_CLEAR_FAULT

            case _:
                return []

        return [
            self._response_builder.build_ack(
                cmd_id=resp_cmd, seq_num=frame.seq_num, free_slots=slots
            )
        ]

    def get_version(self) -> str:
        '''
            Returns handler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
