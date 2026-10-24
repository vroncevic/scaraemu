# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Concrete adapter for constructing binary protocol wire response frames.
'''

from __future__ import annotations

from struct import pack
from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryResponseBuilderAdapter:
    '''
        Adapter constructing packed wire protocol response frames using scaralang builder.

        It defines:

            :attributes:
                | _builder - Injected scaralang binary frame packer.
            :methods:
                | __init__ - Initializes adapter with binary frame builder.
                | build_ack - Constructs an ACK binary response frame.
                | build_nack - Constructs a NACK binary error response frame.
                | build_status - Constructs a STATUS binary telemetry response frame.
                | build_move_event - Constructs a RESP_MOVE_EVENT binary motion notification frame.
                | get_version - Returns adapter component version string.
    '''

    _builder: IBinaryFramePacker

    def __init__(self, *, builder: IBinaryFramePacker) -> None:
        '''
            Initializes adapter with binary frame builder service.

            :param builder: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._builder: Final[IBinaryFramePacker] = builder

    def build_ack(
        self,
        *,
        cmd_id: MessageId,
        seq_num: int,
        free_slots: int,
    ) -> BinaryFrame:
        '''
            Constructs an ACK response frame for a handled command.

            :param cmd_id: MessageId of acknowledged command.
            :param seq_num: Cyclic sequence index matching inbound frame.
            :param free_slots: Available queue depth capacity.
            :return: Assembled BinaryFrame with packed ACK payload.
            :exceptions: None.
        '''
        payload: bytes = pack(BinaryStructFormat.ACK, int(cmd_id), free_slots)

        return self._builder.build_frame(
            msg_id=MessageId.RESP_ACK,
            seq_num=seq_num,
            payload=payload,
        )

    def build_nack(
        self,
        *,
        cmd_id: MessageId,
        seq_num: int,
        error_code: int,
    ) -> BinaryFrame:
        '''
            Constructs a NACK error response frame for a rejected command.

            :param cmd_id: MessageId of rejected command.
            :param seq_num: Cyclic sequence index matching inbound frame.
            :param error_code: Error reason code.
            :return: Assembled BinaryFrame with packed NACK payload.
            :exceptions: None.
        '''
        payload: bytes = pack(BinaryStructFormat.NACK, int(cmd_id), error_code)

        return self._builder.build_frame(
            msg_id=MessageId.RESP_NACK,
            seq_num=seq_num,
            payload=payload,
        )

    def build_status(
        self,
        *,
        seq_num: int,
        step_coords: ScaraStepCoords,
        is_moving: bool,
    ) -> BinaryFrame:
        '''
            Constructs a STATUS telemetry response frame with motor step positions.

            :param seq_num: Cyclic sequence index matching inbound frame.
            :param step_coords: Current motor joint step coordinates.
            :param is_moving: Motion activity flag.
            :return: Assembled BinaryFrame with packed STATUS payload.
            :exceptions: None.
        '''
        payload: bytes = pack(
            BinaryStructFormat.STATUS,
            1 if is_moving else 0,
            0,
            0,
            step_coords.j1_steps,
            step_coords.j2_steps,
            step_coords.z_steps,
            step_coords.j4_steps,
        )

        return self._builder.build_frame(
            msg_id=MessageId.RESP_STATUS,
            seq_num=seq_num,
            payload=payload,
        )

    def build_move_event(
        self,
        *,
        seq_num: int,
        event_type: int,
    ) -> BinaryFrame:
        '''
            Constructs a RESP_MOVE_EVENT binary motion notification frame.

            :param seq_num: Cyclic sequence index.
            :param event_type: Motion event code (e.g. 2 for completed).
            :return: Assembled BinaryFrame with packed MOVE_EVENT payload.
            :exceptions: None.
        '''
        payload: bytes = pack(BinaryStructFormat.MOVE_EVENT, event_type, seq_num)

        return self._builder.build_frame(
            msg_id=MessageId.RESP_MOVE_EVENT,
            seq_num=seq_num,
            payload=payload,
        )

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
