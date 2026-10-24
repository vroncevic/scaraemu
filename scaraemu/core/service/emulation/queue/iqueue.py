# -*- coding: UTF-8 -*-

'''
Module
    iqueue.py
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
    Interface protocol defining motion queue operations for digital twin emulation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEmulationQueue(Protocol):
    '''
        Structural interface protocol defining motion queue operations.

        It defines:

            :methods:
                | enqueue_waypoint - Appends a target Cartesian waypoint to the motion queue.
                | clear_queue - Clears all pending target waypoints from the motion queue.
                | get_snapshot - Captures snapshot of queue state.
    '''

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''
            Appends a target Cartesian waypoint to the motion queue.

            :param waypoint: Target Cartesian pose to reach.
            :param seq_num: Optional sequence number associated with waypoint.
            :return: True if enqueued successfully, False if rejected.
        '''

    def clear_queue(self) -> None:
        '''
            Clears all pending target waypoints from the motion queue.
        '''

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''
            Captures snapshot of queue state.

            :param fallback_pose: Fallback pose if no target is active.
            :return: EmulationQueueSnapshot instance.
        '''
