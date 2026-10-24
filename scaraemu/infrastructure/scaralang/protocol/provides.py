# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Outbound provides dataclass for scaralang protocol adapters.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ProtocolProvides:
    '''
        Encapsulates binary protocol adapters provided by the protocol subpackage.

        It defines:

            :attributes:
                | codec - Wire frame codec adapter for binary serialization/parsing.
                | payload_decoder - Payload decoder for inbound command payloads.
                | response_builder - Response frame builder for wire responses.
                | response_decoder - Response decoder for inbound wire response payloads.
    '''

    codec: IBinaryFrameCodecAdapter
    payload_decoder: IBinaryPayloadDecoderAdapter
    response_builder: IBinaryResponseBuilderAdapter
    response_decoder: IBinaryResponseDecoderAdapter
