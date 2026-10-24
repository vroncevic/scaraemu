# -*- coding: UTF-8 -*-

'''
Module
    streamer.py
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
    Flow control window manager streaming trajectory waypoints to firmware.
'''

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from typing import Final

from scaracom.flow.pacing.iwindow import IFlowWindow
from scaracom.transport.itransport import ITransport

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.streaming.pumper.ipumper import IQueuePumper
from scaraemu.infrastructure.streaming.streamer.dependencies import StreamerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueStreamer:
    '''
        Flow control window manager streaming trajectory waypoints to firmware.

        It defines:

            :attributes:
                | _transport - Communication transport layer.
                | _flow_window - Flow control window slot tracker.
                | _pumper - Queue packet pumper across transport.
                | _pending_queue - Host motion queue of pending target poses.
            :methods:
                | __init__ - Initializes queue streamer with dependency bundle.
                | stream_trajectory - Streams multiple waypoint poses within flow window.
                | process_ack - Updates flow control state from firmware ACK free slots.
                | clear - Flushes pending host queue and resets flow control window.
                | get_version - Returns streamer component version string.
    '''

    _transport: ITransport
    _flow_window: IFlowWindow
    _pumper: IQueuePumper
    _pending_queue: deque[ScaraPose]

    def __init__(self, dependencies: StreamerDependencies) -> None:
        '''
            Initializes queue streamer with dependency bundle.

            :param dependencies: Encapsulated streamer dependency bundle.
            :exceptions: None.
        '''
        self._transport: Final[ITransport] = dependencies.transport
        self._flow_window: Final[IFlowWindow] = dependencies.flow_window
        self._pumper: Final[IQueuePumper] = dependencies.pumper
        self._pending_queue: Final[deque[ScaraPose]] = deque()

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Streams multiple waypoint poses within flow window.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''
        if self._transport.is_connected():
            self._pending_queue.extend(poses)
            self._pumper.pump(self._pending_queue)

    def process_ack(self, free_slots: int) -> None:
        '''
            Updates flow control state from firmware ACK free slots and pumps pending queue.

            :param free_slots: Available queue buffer slots reported by firmware.
            :exceptions: None.
        '''
        self._flow_window.update_from_slots(free_slots)

        if self._transport.is_connected():
            self._pumper.pump(self._pending_queue)

    def clear(self) -> None:
        '''
            Flushes pending host queue and resets flow control window.

            :exceptions: None.
        '''
        self._pending_queue.clear()
        self._flow_window.reset()

    def get_version(self) -> str:
        '''
            Returns streamer component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
