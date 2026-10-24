# -*- coding: UTF-8 -*-

'''
Module
    iadapter.py
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
    Structural protocol for decoding binary protocol response frame payloads.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryResponseDecoderAdapter(Protocol):
    '''
        Structural protocol defining binary wire response payload decoding.

        It defines:

            :methods:
                | unpack_ack - Deserializes 2-byte ACK payload into (acked_id, free_slots).
                | unpack_nack - Deserializes 2-byte NACK payload into (rejected_id, error_code).
                | unpack_status_steps - Deserializes STATUS payload into ScaraStepCoords.
                | get_version - Returns protocol component version string.
    '''

    def unpack_ack(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes 2-byte ACK payload into (acked_id, free_slots).

            :param payload: Raw body bytes of RESP_ACK frame.
            :return: Tuple containing (acked_msg_id, free_slots).
            :exceptions: None.
        '''

    def unpack_nack(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes 2-byte NACK payload into (rejected_id, error_code).

            :param payload: Raw body bytes of RESP_NACK frame.
            :return: Tuple containing (rejected_msg_id, error_code).
            :exceptions: None.
        '''

    def unpack_status_steps(self, payload: bytes) -> ScaraStepCoords:
        '''
            Deserializes STATUS payload into motor joint step coordinates.

            :param payload: Raw body bytes of RESP_STATUS frame.
            :return: ScaraStepCoords target instance.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
