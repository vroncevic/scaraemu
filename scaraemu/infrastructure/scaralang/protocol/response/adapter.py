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
    Concrete adapter decoding binary wire protocol response frame payloads.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar, Final

from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker
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


class BinaryResponseDecoderAdapter:
    '''
        Adapter decoding raw binary response payload bytes into typed responses.

        It defines:

            :attributes:
                | STATUS_FORMAT - Struct format for consolidated robot status payload.
                | _response_unpacker - Injected scaralang binary response unpacker.
            :methods:
                | __init__ - Initializes adapter with response unpacker.
                | unpack_ack - Deserializes 2-byte ACK payload into (acked_id, free_slots).
                | unpack_nack - Deserializes 2-byte NACK payload into (rejected_id, error_code).
                | unpack_status_steps - Deserializes STATUS payload into ScaraStepCoords.
                | get_version - Returns adapter component version string.
    '''

    STATUS_FORMAT: ClassVar[str] = str(BinaryStructFormat.STATUS)
    _response_unpacker: IBinaryResponsePayloadUnpacker

    def __init__(
        self,
        *,
        response_unpacker: IBinaryResponsePayloadUnpacker,
    ) -> None:
        '''
            Initializes adapter with response unpacker collaborator.

            :param response_unpacker: Injected IBinaryResponsePayloadUnpacker instance.
            :exceptions: None.
        '''
        self._response_unpacker: Final[IBinaryResponsePayloadUnpacker] = (
            response_unpacker
        )

    def unpack_ack(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes 2-byte ACK payload into (acked_id, free_slots).

            :param payload: Raw body bytes of RESP_ACK frame.
            :return: Tuple containing (acked_msg_id, free_slots).
            :exceptions: None.
        '''
        return self._response_unpacker.unpack_ack(payload)

    def unpack_nack(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes 2-byte NACK payload into (rejected_id, error_code).

            :param payload: Raw body bytes of RESP_NACK frame.
            :return: Tuple containing (rejected_msg_id, error_code).
            :exceptions: None.
        '''
        return self._response_unpacker.unpack_nack(payload)

    def unpack_status_steps(self, payload: bytes) -> ScaraStepCoords:
        '''
            Deserializes STATUS payload into motor joint step coordinates.

            :param payload: Raw body bytes of RESP_STATUS frame.
            :return: ScaraStepCoords target instance.
            :exceptions: None.
        '''
        if len(payload) < 19:
            return ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0)

        values = unpack(self.STATUS_FORMAT, payload[:19])

        return ScaraStepCoords(
            j1_steps=values[3],
            j2_steps=values[4],
            z_steps=values[5],
            j4_steps=values[6],
        )

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
