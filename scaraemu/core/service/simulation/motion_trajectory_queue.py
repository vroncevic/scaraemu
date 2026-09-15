# -*- coding: UTF-8 -*-

'''
Module
    motion_trajectory_queue.py
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
    FIFO motion trajectory queue and historical path trail buffer manager.
'''

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from typing import Final

from scaraemu.core.model.kinematics.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionTrajectoryQueue:
    '''
        Manages the FIFO queue of interpolated waypoint poses and historical path trail.

        It defines:

            :attributes:
                | MAX_TRAIL_LENGTH - Maximum number of historical trajectory points.
                | _motion_queue - FIFO queue of pending Cartesian waypoints.
                | _trail_points - Fixed-size historical XY coordinate trail buffer.
            :methods:
                | __init__ - Initializes queue and trail buffer with starting point.
                | append - Appends a waypoint to the motion queue.
                | extend - Appends multiple waypoints to the motion queue.
                | pop_next - Pops the next waypoint from the queue.
                | append_trail - Appends a point to the historical trail.
                | clear - Empties the queue and resets trail to given point.
                | clear_queue_only - Empties only the motion queue.
                | get_queue_depth - Returns the number of items in the queue.
                | get_trail_points - Returns an immutable snapshot of trail points.
                | get_peek_target - Returns the next waypoint without popping, if any.
                | get_last_pose - Returns the last enqueued waypoint or fallback pose.
    '''

    MAX_TRAIL_LENGTH: Final[int] = 1000

    _motion_queue: deque[ScaraPose]
    _trail_points: deque[tuple[float, float]]

    def __init__(self, initial_x: float = 180.0, initial_y: float = 0.0) -> None:
        '''
            Initializes queue and trail buffer with starting point.

            :param initial_x: Starting X coordinate in mm.
            :param initial_y: Starting Y coordinate in mm.
            :exceptions: None.
        '''
        self._motion_queue = deque()
        self._trail_points = deque(maxlen=self.MAX_TRAIL_LENGTH)
        self._trail_points.append((initial_x, initial_y))

    def append(self, pose: ScaraPose) -> None:
        '''
            Appends a waypoint to the motion queue.

            :param pose: Target ScaraPose.
            :exceptions: None.
        '''
        self._motion_queue.append(pose)

    def extend(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Appends multiple waypoints to the motion queue.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''
        self._motion_queue.extend(poses)

    def pop_next(self) -> ScaraPose:
        '''
            Pops the next waypoint from the queue.

            :return: Next ScaraPose from the queue.
            :exceptions: IndexError if queue is empty.
        '''
        return self._motion_queue.popleft()

    def append_trail(self, x: float, y: float) -> None:
        '''
            Appends an XY coordinate to the historical trail buffer.

            :param x: X coordinate in mm.
            :param y: Y coordinate in mm.
            :exceptions: None.
        '''
        self._trail_points.append((x, y))

    def clear(self, current_pose: ScaraPose) -> None:
        '''
            Clears pending motion queue and resets path trail.

            :param current_pose: Current robot pose to seed new trail.
            :exceptions: None.
        '''
        self._motion_queue.clear()
        self._trail_points.clear()
        self._trail_points.append((current_pose.x, current_pose.y))

    def clear_queue_only(self) -> None:
        '''
            Clears only the pending motion queue without touching the trail.

            :exceptions: None.
        '''
        self._motion_queue.clear()

    def get_queue_depth(self) -> int:
        '''
            Returns the number of waypoints waiting in the motion queue.

            :return: Integer count of queued poses.
            :exceptions: None.
        '''
        return len(self._motion_queue)

    def get_trail_points(self) -> tuple[tuple[float, float], ...]:
        '''
            Returns an immutable snapshot of historical XY trail points.

            :return: Tuple of (x, y) coordinate pairs.
            :exceptions: None.
        '''
        return tuple(self._trail_points)

    def get_peek_target(self) -> ScaraPose | None:
        '''
            Returns the next waypoint without popping, or None if queue is empty.

            :return: Next ScaraPose or None.
            :exceptions: None.
        '''
        return self._motion_queue[0] if self._motion_queue else None

    def get_last_pose(self, fallback: ScaraPose) -> ScaraPose:
        '''
            Returns the last enqueued waypoint, or fallback pose if queue is empty.

            :param fallback: Pose to return if queue is empty.
            :return: Last enqueued ScaraPose or fallback.
            :exceptions: None.
        '''
        return self._motion_queue[-1] if self._motion_queue else fallback
