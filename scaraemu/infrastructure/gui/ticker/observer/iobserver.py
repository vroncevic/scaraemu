# -*- coding: UTF-8 -*-

'''
Module
    iobserver.py
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
    Interface protocol for composite simulation UI view observers.
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
class ISimulationViewObserver(Protocol):
    '''
        Defines structural contract for refreshing UI presentation views on simulation ticks.

        It defines:

            :methods:
                | update_views - Dispatches updated telemetry and simulation state to views.
                | get_version - Returns protocol version string.
    '''

    def update_views(
        self,
        telemetry: Telemetry,
        simulation_state: SimulationState,
    ) -> None:
        '''
            Dispatches updated telemetry and simulation state to views.

            :param telemetry: Current manipulator telemetry snapshot.
            :param simulation_state: Current simulation stepper state snapshot.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
            :exceptions: None.
        '''
