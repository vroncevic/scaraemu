# -*- coding: UTF-8 -*-

'''
Module
    istreamer.py
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
    Structural protocol for hardware trajectory streaming and flow control windowing.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IQueueStreamer(Protocol):
    '''
        Structural protocol defining outbound hardware trajectory queue streaming.

        It defines:

            :methods:
                | stream_trajectory - Streams multiple waypoint poses within flow window.
                | process_ack - Updates flow control state from firmware ACK free slots.
                | clear - Flushes pending host queue and resets flow control window.
                | get_version - Returns streamer protocol version string.
    '''

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Streams multiple waypoint poses within flow window.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''

    def process_ack(self, free_slots: int) -> None:
        '''
            Updates flow control state from firmware ACK free slots and pumps pending queue.

            :param free_slots: Available queue buffer slots reported by firmware.
            :exceptions: None.
        '''

    def clear(self) -> None:
        '''
            Flushes pending host queue and resets flow control window.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns streamer protocol version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
