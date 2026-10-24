# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Motion trajectory coordinator dispatching move operations to streamer.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCoordinator:
    '''
        Motion trajectory coordinator dispatching move operations to streamer.

        It defines:

            :attributes:
                | _streamer - Outbound trajectory queue streamer and flow controller.
            :methods:
                | __init__ - Initializes motion coordinator with queue streamer.
                | send_hardware_move - Streams point move target pose to hardware.
                | enqueue_hardware_trajectory - Enqueues waypoints for streaming.
                | get_version - Returns motion coordinator component version.
    '''

    _streamer: IQueueStreamer

    def __init__(self, *, streamer: IQueueStreamer) -> None:
        '''
            Initializes motion coordinator with queue streamer.

            :param streamer: Trajectory queue streamer managing flow control.
            :exceptions: None.
        '''
        self._streamer: Final[IQueueStreamer] = streamer

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Streams point move target pose to hardware.

            :param pose: Target ScaraPose.
            :exceptions: None.
        '''
        self._streamer.stream_trajectory((pose,))

    def enqueue_hardware_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Enqueues waypoints for streaming with flow control.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''
        self._streamer.stream_trajectory(poses)

    def get_version(self) -> str:
        '''
            Returns motion coordinator component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
