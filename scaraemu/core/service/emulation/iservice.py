# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Interface protocol defining core digital twin manipulator emulation operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEmulationService(Protocol):
    '''
        Structural interface protocol for manipulator simulation and telemetry.

        It defines:

            :methods:
                | step - Advances simulation by time delta in seconds.
                | get_telemetry - Returns live telemetry snapshot DTO.
                | get_simulation_state - Returns animation and queue state snapshot DTO.
                | clear_trail - Clears historical motion trail coordinates.
    '''

    def step(self, dt: float) -> bool:
        '''
            Advances simulation by delta time in seconds.

            :param dt: Time delta in seconds.
            :return: True if motion occurred, False if idle or stopped.
        '''

    def get_telemetry(self) -> Telemetry:
        '''
            Builds and returns comprehensive live telemetry snapshot.

            :return: Live Telemetry snapshot DTO.
        '''

    def get_simulation_state(self) -> SimulationState:
        '''
            Builds and returns simulation queue and trail state snapshot.

            :return: Live SimulationState snapshot DTO.
        '''

    def clear_trail(self) -> None:
        '''
            Clears historical motion trail coordinates and resets to current pose.
        '''
