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
    Structural protocol for binary frame wire parsing and serialization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameCodecAdapter(Protocol):
    '''
        Structural protocol defining binary frame wire parsing and serialization contracts.

        It defines:

            :methods:
                | feed_bytes - Parses incoming raw stream bytes into complete BinaryFrames.
                | pack_frame - Serializes a BinaryFrame into raw wire bytes with framing.
                | reset - Clears underlying parser FSM state machine and buffer.
                | get_version - Returns protocol component version string.
    '''

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Parses incoming stream bytes and returns all assembled BinaryFrames.

            :param data: Contiguous incoming wire bytes.
            :return: Tuple of assembled BinaryFrame instances.
        '''

    def pack_frame(self, frame: BinaryFrame) -> bytes:
        '''
            Serializes a BinaryFrame into wire format bytes.

            :param frame: BinaryFrame instance to encode.
            :return: Formatted wire bytes with delimiters and CRC16.
        '''

    def reset(self) -> None:
        '''
            Clears parser state machine and internal byte buffers.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol component version string.

            :return: Semantic version string.
        '''
