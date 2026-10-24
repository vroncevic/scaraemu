# -*- coding: UTF-8 -*-

'''
Module
    outbound_queue.py
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
    Thread-safe outbound frame queue implementation for virtual manipulator server.
'''

from __future__ import annotations

from queue import Empty, Queue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class OutboundFrameQueue:
    '''
        Thread-safe FIFO queue holding outbound binary frames for client transmission.

        It defines:

            :attributes:
                | _queue - Internal thread-safe FIFO queue instance.
            :methods:
                | push - Enqueues a packed binary frame for transmission.
                | pop_all - Drains and returns all queued binary frame byte packets.
                | clear - Empties all queued outbound frames.
                | get_version - Returns queue component version string.
    '''

    _queue: Queue[bytes]

    def __init__(self) -> None:
        '''
            Initializes empty thread-safe outbound frame queue.

            :exceptions: None.
        '''
        self._queue = Queue()

    def push(self, data: bytes) -> None:
        '''
            Enqueues a packed binary frame for transmission.

            :param data: Packed binary frame bytes.
            :exceptions: None.
        '''
        self._queue.put(data)

    def pop_all(self) -> tuple[bytes, ...]:
        '''
            Drains and returns all queued binary frame byte packets.

            :return: Tuple of queued binary frame bytes.
            :exceptions: None.
        '''
        items: list[bytes] = []

        while not self._queue.empty():
            try:
                items.append(self._queue.get_nowait())

            except Empty:
                break

        return tuple(items)

    def clear(self) -> None:
        '''
            Empties all queued outbound frames.

            :exceptions: None.
        '''
        while not self._queue.empty():
            try:
                self._queue.get_nowait()

            except Empty:
                break

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
