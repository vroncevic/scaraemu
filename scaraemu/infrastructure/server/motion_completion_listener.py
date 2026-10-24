# -*- coding: UTF-8 -*-

'''
Module
    motion_completion_listener.py
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
    Virtual manipulator server motion waypoint completion event notifier.
'''

from __future__ import annotations

from typing import Final

from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.session.ioutbound_queue import IOutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerMotionCompletionListener:
    '''
        Listens for completed simulation waypoints and enqueues RESP_MOVE_EVENT frames.

        It defines:

            :attributes:
                | _outbound_queue - Outbound frame queue for connected client.
                | _response_builder - Wire protocol response frame builder.
                | _codec - Binary frame codec adapter.
                | _log_listener - Server log listener.
            :methods:
                | __init__ - Initializes listener with queue, response builder, codec and log listener.
                | on_waypoint_completed - Builds and pushes RESP_MOVE_EVENT when waypoint finishes.
                | get_version - Returns component version string.
    '''

    _outbound_queue: IOutboundFrameQueue
    _response_builder: IBinaryResponseBuilderAdapter
    _codec: IBinaryFrameCodecAdapter
    _log_listener: IServerLogListener

    def __init__(
        self,
        *,
        outbound_queue: IOutboundFrameQueue,
        response_builder: IBinaryResponseBuilderAdapter,
        codec: IBinaryFrameCodecAdapter,
        log_listener: IServerLogListener,
    ) -> None:
        '''
            Initializes server motion completion listener with collaborators.

            :param outbound_queue: Injected IOutboundFrameQueue instance.
            :param response_builder: Injected IBinaryResponseBuilderAdapter instance.
            :param codec: Injected IBinaryFrameCodecAdapter instance.
            :param log_listener: Injected IServerLogListener instance.
            :exceptions: None.
        '''
        self._outbound_queue: Final[IOutboundFrameQueue] = outbound_queue
        self._response_builder: Final[IBinaryResponseBuilderAdapter] = response_builder
        self._codec: Final[IBinaryFrameCodecAdapter] = codec
        self._log_listener: Final[IServerLogListener] = log_listener

    def on_waypoint_completed(self, seq_num: int) -> None:
        '''
            Builds and pushes RESP_MOVE_EVENT when waypoint finishes.

            :param seq_num: Sequence number of completed waypoint motion.
            :exceptions: None.
        '''
        if seq_num > 0:
            frame = self._response_builder.build_move_event(
                seq_num=seq_num,
                event_type=2,
            )
            packed: bytes = self._codec.pack_frame(frame)
            self._outbound_queue.push(packed)
            self._log_listener.on_server_log(
                f'🏁 [DT-SERVER]: Waypoint reached (seq={seq_num})'
            )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
