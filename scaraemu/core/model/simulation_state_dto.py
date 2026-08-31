# -*- coding: UTF-8 -*-

'''
Module
    simulation_state_dto.py
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
    Defines SCARA animation and simulation engine state Data Transfer Object.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class SimulationStateDTO:
    '''
        State of emulator simulation queue and motion rendering.

        It defines:

            :attributes:
                | is_animating - True if background interpolation loop is active.
                | queue_depth - Number of pending target poses in motion queue.
                | trail_points - Trajectory trail historical path coordinates.
                | current_target - Active target pose or None if idle.
    '''

    is_animating: bool
    queue_depth: int
    trail_points: tuple[tuple[float, float], ...]
    current_target: ScaraPose | None = None
