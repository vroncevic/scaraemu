# -*- coding: UTF-8 -*-

'''
Module
    queue.py
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
    Emulation motion queue management.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationQueue:
    '''
        Manages Cartesian target waypoints FIFO queue and active target progression.

        It defines:

            :attributes:
                | _flags - Emulation state flags reference.
                | _queue - Internal FIFO queue of waypoints and sequence numbers.
                | _active_waypoint - Active target Cartesian waypoint tuple being approached.
                | _planned_path - Historical list of planned trajectory coordinates.
            :methods:
                | __init__ - Initializes the emulation queue.
                | enqueue_waypoint - Appends a target Cartesian waypoint to the motion queue.
                | clear_queue - Clears all pending and active waypoints.
                | get_active_or_next - Retrieves active target or dequeues next waypoint.
                | complete_active - Clears active target upon arrival.
                | get_snapshot - Captures snapshot of queue state.
    '''

    _flags: EmulationFlags
    _queue: list[tuple[ScaraPose, int]]
    _active_waypoint: tuple[ScaraPose, int] | tuple[()]
    _planned_path: list[tuple[float, float]]

    def __init__(self, *, flags: EmulationFlags) -> None:
        '''
            Initializes the emulation queue.

            :param flags: Emulation state flags reference.
            :exceptions: None.
        '''
        self._flags: Final[EmulationFlags] = flags
        self._queue = []
        self._active_waypoint = ()
        self._planned_path = []

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''
            Appends a target Cartesian waypoint to the motion queue.

            :param waypoint: Target Cartesian pose to reach.
            :param seq_num: Optional sequence number associated with waypoint.
            :return: True if successfully enqueued, False if stopped.
            :exceptions: None.
        '''
        if self._flags.estop_active or not self._flags.motors_enabled:
            return False

        if not self._active_waypoint and not self._queue:
            self._planned_path.clear()

        self._queue.append((waypoint, seq_num))
        self._planned_path.append((waypoint.x, waypoint.y))

        return True

    def clear_queue(self) -> None:
        '''
            Clears all pending target waypoints from the motion queue.

            :exceptions: None.
        '''
        self._queue.clear()
        self._active_waypoint = ()
        self._planned_path.clear()

    def get_active_or_next(self) -> tuple[ScaraPose, int] | tuple[()]:
        '''
            Retrieves active target waypoint or dequeues next waypoint.

            :return: Active waypoint tuple (pose, seq_num) or empty tuple if idle.
            :exceptions: None.
        '''
        if not self._active_waypoint:
            if not self._queue:
                return ()

            self._active_waypoint = self._queue.pop(0)

        return self._active_waypoint

    def complete_active(self) -> None:
        '''
            Clears active target upon waypoint arrival.

            :exceptions: None.
        '''
        self._active_waypoint = ()

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''
            Captures current snapshot of queue state.

            :param fallback_pose: Fallback pose if no target is active.
            :return: EmulationQueueSnapshot instance.
            :exceptions: None.
        '''
        has_target: bool = bool(self._active_waypoint)
        target: ScaraPose = (
            self._active_waypoint[0] if self._active_waypoint else fallback_pose
        )

        return EmulationQueueSnapshot(
            queue_depth=len(self._queue),
            has_target=has_target,
            current_target=target,
            planned_path=tuple(self._planned_path),
        )
