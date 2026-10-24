# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for ProtocolProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.provides import ProtocolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocolProvides(TestCase):
    '''
        Validates ProtocolProvides dataclass immutability and attribute access.

        It defines:

            :methods:
                | test_attributes - Verifies encapsulated adapter attributes.
    '''

    def test_attributes(self) -> None:
        '''
            Verifies ProtocolProvides holds the injected protocol adapters.

            :exceptions: None.
        '''
        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        mock_payload_decoder = MagicMock(spec=IBinaryPayloadDecoderAdapter)
        mock_response_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        mock_response_decoder = MagicMock(spec=IBinaryResponseDecoderAdapter)

        provides = ProtocolProvides(
            codec=mock_codec,
            payload_decoder=mock_payload_decoder,
            response_builder=mock_response_builder,
            response_decoder=mock_response_decoder,
        )

        self.assertIs(provides.codec, mock_codec)
        self.assertIs(provides.payload_decoder, mock_payload_decoder)
        self.assertIs(provides.response_builder, mock_response_builder)
        self.assertIs(provides.response_decoder, mock_response_decoder)


if __name__ == '__main__':
    unittest_main()
