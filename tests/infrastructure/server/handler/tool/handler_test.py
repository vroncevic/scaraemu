# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit tests for ToolHandler.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler
from scaraemu.infrastructure.server.handler.tool.dependencies import ToolHandlerDependencies
from scaraemu.infrastructure.server.handler.tool.handler import ToolHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolHandler(TestCase):
    '''
        Unit test cases verifying ToolHandler functionality.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and handler.
                | test_structural_typing - Verifies ToolHandler satisfies IBinaryCommandHandler.
                | test_can_handle - Verifies can_handle accepts tool message IDs.
                | test_tool_pump_command - Verifies tool pump command generates ACK.
                | test_tool_valve_command - Verifies tool valve command generates ACK.
                | test_version - Verifies get_version returns string.
                | test_unhandled_frame - Verifies unhandled message ID returns empty list.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures and handler.

            :exceptions: None.
        '''
        response_builder: IBinaryResponseBuilderAdapter = (
            BinaryResponseBuilderAdapterFactory.create()
        )
        decoder: IBinaryPayloadDecoderAdapter = BinaryPayloadDecoderAdapterFactory.create()
        deps = ToolHandlerDependencies(
            response_builder=response_builder,
            decoder=decoder,
        )
        self.handler = ToolHandler(dependencies=deps)

    def test_structural_typing(self) -> None:
        '''
            Verifies ToolHandler satisfies IBinaryCommandHandler structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler, IBinaryCommandHandler)

    def test_can_handle(self) -> None:
        '''
            Verifies can_handle accepts tool message IDs and rejects others.

            :exceptions: None.
        '''
        self.assertTrue(self.handler.can_handle(MessageId.CMD_TOOL_PUMP))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_TOOL_VALVE))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_PING))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_MOVE_JOINT_STEPS))

    def test_tool_pump_command(self) -> None:
        '''
            Verifies tool pump command generates ACK.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_TOOL_PUMP, seq_num=1, payload=b'\x00\x01', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_ACK)

    def test_tool_valve_command(self) -> None:
        '''
            Verifies tool valve command generates ACK.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_TOOL_VALVE, seq_num=2, payload=b'\x01\x00', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_ACK)

    def test_version(self) -> None:
        '''
            Verifies get_version returns string.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler.get_version(), str)

    def test_unhandled_frame(self) -> None:
        '''
            Verifies wildcard branch returns empty list for unhandled message ID.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_PING, seq_num=99, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest_main()
