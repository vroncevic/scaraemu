# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for IBinaryResponseBuilderAdapter Protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockResponseBuilder:
    def build_ack(self, *, cmd_id: MessageId, seq_num: int, free_slots: int) -> BinaryFrame:
        return BinaryFrame(msg_id=MessageId.RESP_ACK, seq_num=seq_num, payload=b'', crc16=0)

    def build_nack(self, *, cmd_id: MessageId, seq_num: int, error_code: int) -> BinaryFrame:
        return BinaryFrame(msg_id=MessageId.RESP_NACK, seq_num=seq_num, payload=b'', crc16=0)

    def build_status(self, *, seq_num: int, step_coords: ScaraStepCoords, is_moving: bool) -> BinaryFrame:
        return BinaryFrame(msg_id=MessageId.RESP_STATUS, seq_num=seq_num, payload=b'', crc16=0)

    def build_move_event(self, *, seq_num: int, event_type: int) -> BinaryFrame:
        return BinaryFrame(msg_id=MessageId.RESP_MOVE_EVENT, seq_num=seq_num, payload=b'', crc16=0)

    def get_version(self) -> str:
        return '1.0.2'


class TestIBinaryResponseBuilderAdapter(TestCase):
    '''
        Validates IBinaryResponseBuilderAdapter protocol conformance.

        It defines:

            :methods:
                | test_conforming_class_satisfies_protocol - Verifies structural typing.
                | test_non_conforming_class_fails_protocol - Verifies non-conforming fails.
    '''

    def test_conforming_class_satisfies_protocol(self) -> None:
        '''
            Verifies structural typing.

            :exceptions: None.
        '''
        builder = _MockResponseBuilder()
        self.assertIsInstance(builder, IBinaryResponseBuilderAdapter)

    def test_non_conforming_class_fails_protocol(self) -> None:
        '''
            Verifies non-conforming fails.

            :exceptions: None.
        '''
        class _Bad:
            pass

        self.assertNotIsInstance(_Bad(), IBinaryResponseBuilderAdapter)


if __name__ == '__main__':
    unittest_main()
