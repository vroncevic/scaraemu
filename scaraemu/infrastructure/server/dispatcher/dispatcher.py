# -*- coding: UTF-8 -*-

'''
Module
    dispatcher.py
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
    Dispatches incoming binary frames to virtual processors.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame

from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.server.processor.iprocessor import IVirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerFrameDispatcher:
    '''
        Dispatches incoming binary frames to virtual binary processors.

        It defines:

            :attributes:
                | _binary_processor - Injected IVirtualBinaryFrameProcessor binary frame dispatcher.
                | _codec - Injected IBinaryFrameCodecAdapter binary frame parser and serializer.
            :methods:
                | __init__ - Initializes dispatcher with binary processor and codec adapter.
                | dispatch_binary - Parses raw bytes and returns packed binary frame responses.
                | reset - Resets underlying protocol parsers and command state.
                | get_version - Returns dispatcher component version.
    '''

    _binary_processor: IVirtualBinaryFrameProcessor
    _codec: IBinaryFrameCodecAdapter

    def __init__(
        self,
        *,
        binary_processor: IVirtualBinaryFrameProcessor,
        codec: IBinaryFrameCodecAdapter,
    ) -> None:
        '''
            Initializes dispatcher with binary processor and codec adapter.

            :param binary_processor: Injected IVirtualBinaryFrameProcessor instance.
            :param codec: Injected IBinaryFrameCodecAdapter instance.
            :exceptions: None.
        '''
        self._binary_processor: Final[IVirtualBinaryFrameProcessor] = binary_processor
        self._codec: Final[IBinaryFrameCodecAdapter] = codec

    def dispatch_binary(self, data: bytes) -> tuple[bytes, ...]:
        '''
            Parses raw bytes and returns packed binary frame responses.

            :param data: Incoming raw byte buffer.
            :return: Tuple of packed response byte payloads.
            :exceptions: None.
        '''
        frames: tuple[BinaryFrame, ...] = self._codec.feed_bytes(data)
        out: list[bytes] = []

        for frame in frames:
            resp_frames: list[BinaryFrame] = self._binary_processor.process_frame(
                frame=frame
            )

            for resp in resp_frames:
                out.append(self._codec.pack_frame(resp))

        return tuple(out)

    def reset(self) -> None:
        '''
            Resets underlying protocol parsers and command state.

            :exceptions: None.
        '''
        self._binary_processor.reset()
        self._codec.reset()

    def get_version(self) -> str:
        '''
            Returns dispatcher component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
