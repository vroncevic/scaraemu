# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit tests for ServerFrameDispatcher.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.server.dispatcher.dispatcher import ServerFrameDispatcher
from scaraemu.infrastructure.server.processor.iprocessor import IVirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerFrameDispatcher(TestCase):
    '''
        Test cases verifying ServerFrameDispatcher processing and decoding.

        It defines:

            :methods:
                | setUp - Initializes mock processor and codec adapter.
                | test_dispatch_binary - Verifies binary frame ingestion.
                | test_reset - Verifies parser buffer reset.
                | test_get_version - Verifies component version string.
    '''

    bin_proc: MagicMock
    codec: IBinaryFrameCodecAdapter
    dispatcher: ServerFrameDispatcher

    def setUp(self) -> None:
        '''
            Initializes mock processor and codec adapter.

            :exceptions: None.
        '''
        self.bin_proc = MagicMock(spec=IVirtualBinaryFrameProcessor)
        self.codec = BinaryFrameCodecAdapterFactory.create()
        self.dispatcher = ServerFrameDispatcher(
            binary_processor=self.bin_proc,
            codec=self.codec,
        )

    def test_dispatch_binary(self) -> None:
        '''
            Verifies binary frame ingestion.

            :exceptions: None.
        '''
        ping_frame = BinaryFrame(msg_id=MessageId.CMD_PING, seq_num=10, payload=b'', crc16=0)
        ack_frame = BinaryFrame(msg_id=MessageId.RESP_ACK, seq_num=10, payload=b'', crc16=0)
        self.bin_proc.process_frame.return_value = [ack_frame]
        wire_bytes = self.codec.pack_frame(frame=ping_frame)
        response_bytes = self.dispatcher.dispatch_binary(wire_bytes)
        self.assertGreater(len(response_bytes), 0)
        self.bin_proc.process_frame.assert_called_once()

    def test_reset(self) -> None:
        '''
            Verifies parser buffer reset.

            :exceptions: None.
        '''
        self.dispatcher.reset()
        self.bin_proc.reset.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.dispatcher.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
