# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for BinaryResponseBuilderAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.scaralang.protocol.builder.adapter import BinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryResponseBuilderAdapter(TestCase):
    '''
        Validates BinaryResponseBuilderAdapter methods.

        It defines:

            :methods:
                | test_build_ack - Verifies ACK frame construction.
                | test_build_nack - Verifies NACK frame construction.
                | test_build_status - Verifies STATUS frame construction.
                | test_build_move_event - Verifies RESP_MOVE_EVENT frame construction.
                | test_get_version - Verifies component version string.
    '''

    def test_build_ack(self) -> None:
        '''
            Verifies ACK frame construction.

            :exceptions: None.
        '''
        builder = BuilderFactory.create().packer
        adapter = BinaryResponseBuilderAdapter(builder=builder)
        self.assertIsInstance(adapter, IBinaryResponseBuilderAdapter)

        frame: BinaryFrame = adapter.build_ack(
            cmd_id=MessageId.CMD_PING, seq_num=5, free_slots=12
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_ACK)
        self.assertEqual(frame.seq_num, 5)
        self.assertEqual(len(frame.payload), 2)

    def test_build_nack(self) -> None:
        '''
            Verifies NACK frame construction.

            :exceptions: None.
        '''
        builder = BuilderFactory.create().packer
        adapter = BinaryResponseBuilderAdapter(builder=builder)

        frame: BinaryFrame = adapter.build_nack(
            cmd_id=MessageId.CMD_PING, seq_num=3, error_code=1
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_NACK)
        self.assertEqual(frame.seq_num, 3)
        self.assertEqual(len(frame.payload), 2)

    def test_build_status(self) -> None:
        '''
            Verifies STATUS frame construction.

            :exceptions: None.
        '''
        builder = BuilderFactory.create().packer
        adapter = BinaryResponseBuilderAdapter(builder=builder)
        coords = ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=300, j4_steps=400)

        frame: BinaryFrame = adapter.build_status(
            seq_num=7, step_coords=coords, is_moving=False
        )
        self.assertEqual(frame.msg_id, MessageId.RESP_STATUS)
        self.assertEqual(frame.seq_num, 7)
        self.assertGreater(len(frame.payload), 0)

    def test_build_move_event(self) -> None:
        '''
            Verifies RESP_MOVE_EVENT frame construction.

            :exceptions: None.
        '''
        builder = BuilderFactory.create().packer
        adapter = BinaryResponseBuilderAdapter(builder=builder)

        frame: BinaryFrame = adapter.build_move_event(seq_num=9, event_type=2)
        self.assertEqual(frame.msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertEqual(frame.seq_num, 9)
        self.assertGreater(len(frame.payload), 0)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        builder = BuilderFactory.create().packer
        adapter = BinaryResponseBuilderAdapter(builder=builder)
        self.assertEqual(adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
