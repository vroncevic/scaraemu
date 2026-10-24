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
    Concrete adapter wrapping scaralang binary frame parser and builder.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameCodecAdapter:
    '''
        Adapter delegating stream decoding and wire encoding to scaralang protocol services.

        It defines:

            :attributes:
                | _parser - Injected scaralang binary frame parser.
                | _builder - Injected scaralang binary frame packer.
            :methods:
                | __init__ - Initializes adapter with parser and builder services.
                | feed_bytes - Parses incoming stream bytes into BinaryFrames.
                | pack_frame - Serializes BinaryFrame into formatted wire bytes.
                | reset - Clears parser state machine and internal buffers.
                | get_version - Returns adapter component version string.
    '''

    _parser: IBinaryFrameParser
    _builder: IBinaryFramePacker

    def __init__(
        self,
        *,
        parser: IBinaryFrameParser,
        builder: IBinaryFramePacker,
    ) -> None:
        '''
            Initializes adapter with parser and builder services.

            :param parser: Injected IBinaryFrameParser instance.
            :param builder: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._parser: Final[IBinaryFrameParser] = parser
        self._builder: Final[IBinaryFramePacker] = builder

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Parses incoming stream bytes into BinaryFrames.

            :param data: Incoming raw stream bytes.
            :return: Tuple of assembled BinaryFrame instances.
            :exceptions: None.
        '''
        return self._parser.feed_bytes(data)

    def pack_frame(self, frame: BinaryFrame) -> bytes:
        '''
            Serializes BinaryFrame into formatted wire bytes.

            :param frame: BinaryFrame instance to encode.
            :return: Encoded wire bytes.
            :exceptions: None.
        '''
        target_frame: BinaryFrame = frame

        if target_frame.crc16 == 0:
            target_frame = self._builder.build_frame(
                msg_id=frame.msg_id,
                seq_num=frame.seq_num,
                payload=frame.payload,
            )

        return self._builder.pack_frame(frame=target_frame)

    def reset(self) -> None:
        '''
            Clears parser state machine and internal buffers.

            :exceptions: None.
        '''
        self._parser.reset()

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
