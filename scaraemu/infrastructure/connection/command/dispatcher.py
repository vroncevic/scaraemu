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
    Hardware command dispatcher managing binary command frame dispatch and queue flushing.
'''

from __future__ import annotations

from typing import Final

from scaracom.transport.itransport import ITransport
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.connection.command.dependencies import CommandDependencies
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandDispatcher:
    '''
        Hardware command dispatcher managing binary command frame dispatch and queue flushing.

        It defines:

            :attributes:
                | _transport - Communication transport layer.
                | _log_listener - Logging sink for hardware communications.
                | _streamer - Outbound trajectory queue streamer.
                | _codec - Binary wire frame encoder adapter.
                | _seq_num - Cyclic outbound packet sequence counter.
            :methods:
                | __init__ - Initializes command dispatcher with dependency bundle.
                | send_command - Transmits a binary protocol command frame to hardware.
                | clear_queue - Flushes pending host queue and resets flow control.
                | get_version - Returns command dispatcher component version.
    '''

    _transport: ITransport
    _log_listener: ILogListener
    _streamer: IQueueStreamer
    _codec: IBinaryFrameCodecAdapter
    _seq_num: int

    def __init__(self, dependencies: CommandDependencies) -> None:
        '''
            Initializes command dispatcher with dependency bundle.

            :param dependencies: Encapsulated command dispatcher dependency bundle.
            :exceptions: None.
        '''
        self._transport: Final[ITransport] = dependencies.transport
        self._log_listener: Final[ILogListener] = dependencies.log_listener
        self._streamer: Final[IQueueStreamer] = dependencies.streamer
        self._codec: Final[IBinaryFrameCodecAdapter] = dependencies.codec
        self._seq_num = 0

    def send_command(self, msg_id: MessageId, payload: bytes = b'') -> None:
        '''
            Transmits a binary protocol command frame to hardware.

            :param msg_id: Binary protocol MessageId identifier.
            :param payload: Optional packed command payload bytes.
            :exceptions: None.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=msg_id,
            seq_num=self._seq_num,
            payload=payload,
            crc16=0,
        )
        wire_bytes: bytes = self._codec.pack_frame(frame)
        self._transport.write_bytes(wire_bytes)
        self._log_listener.append_log(f'TX > {msg_id.name} seq={self._seq_num}', 'tx')
        self._seq_num = (self._seq_num + 1) & 0xFF

    def clear_queue(self) -> None:
        '''
            Flushes pending host queue and resets flow control.

            :exceptions: None.
        '''
        self._streamer.clear()

    def get_version(self) -> str:
        '''
            Returns command dispatcher component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
