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
    Unit tests for BinaryFrameCodecAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import Mock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser

from scaraemu.infrastructure.scaralang.protocol.codec.adapter import BinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameCodecAdapter(TestCase):
    '''
        Validates BinaryFrameCodecAdapter methods.

        It defines:

            :methods:
                | test_feed_bytes - Verifies delegating to parser.
                | test_pack_frame - Verifies delegating to builder.
                | test_reset - Verifies delegating reset to parser.
                | test_get_version - Verifies component version string.
    '''

    def test_feed_bytes(self) -> None:
        '''
            Verifies delegating to parser.

            :exceptions: None.
        '''
        mock_parser: Mock = Mock(spec=IBinaryFrameParser)
        mock_builder: Mock = Mock(spec=IBinaryFramePacker)
        expected_frame = BinaryFrame(
            msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=0
        )
        mock_parser.feed_bytes.return_value = (expected_frame,)

        adapter = BinaryFrameCodecAdapter(parser=mock_parser, builder=mock_builder)
        self.assertIsInstance(adapter, IBinaryFrameCodecAdapter)

        result = adapter.feed_bytes(b'\x01\x02')
        self.assertEqual(result, (expected_frame,))
        mock_parser.feed_bytes.assert_called_once_with(b'\x01\x02')

    def test_pack_frame(self) -> None:
        '''
            Verifies delegating to builder.

            :exceptions: None.
        '''
        mock_parser: Mock = Mock(spec=IBinaryFrameParser)
        mock_builder: Mock = Mock(spec=IBinaryFramePacker)
        test_frame = BinaryFrame(
            msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=12345
        )
        mock_builder.pack_frame.return_value = b'\xaa\x55\x01\x01\x00'

        adapter = BinaryFrameCodecAdapter(parser=mock_parser, builder=mock_builder)
        result = adapter.pack_frame(test_frame)

        self.assertEqual(result, b'\xaa\x55\x01\x01\x00')
        mock_builder.pack_frame.assert_called_once_with(frame=test_frame)

    def test_pack_frame_computes_crc_when_zero(self) -> None:
        '''
            Verifies computing CRC via builder when crc16 is zero.

            :exceptions: None.
        '''
        mock_parser: Mock = Mock(spec=IBinaryFrameParser)
        mock_builder: Mock = Mock(spec=IBinaryFramePacker)
        test_frame = BinaryFrame(
            msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=0
        )
        built_frame = BinaryFrame(
            msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=5555
        )
        mock_builder.build_frame.return_value = built_frame
        mock_builder.pack_frame.return_value = b'\xaa\x55\x01\x01\x00'

        adapter = BinaryFrameCodecAdapter(parser=mock_parser, builder=mock_builder)
        result = adapter.pack_frame(test_frame)

        self.assertEqual(result, b'\xaa\x55\x01\x01\x00')
        mock_builder.build_frame.assert_called_once_with(
            msg_id=MessageId.CMD_PING, seq_num=1, payload=b''
        )
        mock_builder.pack_frame.assert_called_once_with(frame=built_frame)

    def test_reset(self) -> None:
        '''
            Verifies delegating reset to parser.

            :exceptions: None.
        '''
        mock_parser: Mock = Mock(spec=IBinaryFrameParser)
        mock_builder: Mock = Mock(spec=IBinaryFramePacker)

        adapter = BinaryFrameCodecAdapter(parser=mock_parser, builder=mock_builder)
        adapter.reset()

        mock_parser.reset.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        mock_parser: Mock = Mock(spec=IBinaryFrameParser)
        mock_builder: Mock = Mock(spec=IBinaryFramePacker)

        adapter = BinaryFrameCodecAdapter(parser=mock_parser, builder=mock_builder)
        self.assertEqual(adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
