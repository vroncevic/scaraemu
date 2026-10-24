# -*- coding: UTF-8 -*-

'''
Module
    snapshot.py
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
    State snapshot of emulation motion queue.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class EmulationQueueSnapshot:
    '''
        State snapshot of emulation motion queue.

        It defines:

            :attributes:
                | queue_depth - Number of pending waypoints in queue.
                | has_target - Indicates if active target waypoint is being pursued.
                | current_target - Active target pose or fallback pose.
                | planned_path - Immutable tuple of planned (x, y) coordinates.
            :methods: None.
    '''

    queue_depth: int
    has_target: bool
    current_target: ScaraPose
    planned_path: tuple[tuple[float, float], ...]
