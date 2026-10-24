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
    Handler for binary tool pump and valve actuator command frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.server.handler.tool.dependencies import ToolHandlerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolHandler:
    '''
        Processes tool pump and valve actuator binary frames.

        It defines:

            :attributes:
                | _response_builder - Injected binary frame builder for wire responses.
                | _decoder - Injected binary payload decoder adapter.
            :methods:
                | __init__ - Initializes tool binary handler with dependencies bundle.
                | can_handle - Checks whether message ID is a tool command.
                | handle - Executes tool command and returns response frames.
                | get_version - Returns handler component version string.
    '''

    _response_builder: IBinaryResponseBuilderAdapter
    _decoder: IBinaryPayloadDecoderAdapter

    def __init__(
        self,
        *,
        dependencies: ToolHandlerDependencies,
    ) -> None:
        '''
            Initializes tool binary handler with dependencies bundle.

            :param dependencies: Injected ToolHandlerDependencies instance.
            :exceptions: None.
        '''
        self._response_builder: Final[IBinaryResponseBuilderAdapter] = dependencies.response_builder
        self._decoder: Final[IBinaryPayloadDecoderAdapter] = dependencies.decoder

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Checks whether message ID is a tool command.

            :param msg_id: Binary protocol MessageId enum value.
            :return: True if message ID is handled, False otherwise.
            :exceptions: None.
        '''
        return msg_id in (MessageId.CMD_TOOL_PUMP, MessageId.CMD_TOOL_VALVE)

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Executes tool command and returns response frames.

            :param frame: Inbound BinaryFrame instance.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''
        match frame.msg_id:
            case MessageId.CMD_TOOL_PUMP | MessageId.CMD_TOOL_VALVE:
                self._decoder.unpack_tool_cmd(frame.payload)
                return [self._response_builder.build_ack(
                    cmd_id=frame.msg_id, seq_num=frame.seq_num, free_slots=16
                )]
            case _:
                return []

    def get_version(self) -> str:
        '''
            Returns handler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
