# -*- coding: UTF-8 -*-

'''
Module
    ifactory.py
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
    Abstract factory protocol for creating simulation ticker instances.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
from scaraemu.infrastructure.gui.ticker.iticker import ISimulationTicker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISimulationTickerFactory(Protocol):
    '''
        Defines abstract factory protocol for assembling simulation ticker instances.

        It defines:

            :methods:
                | create - Assembles and returns an ISimulationTicker instance.
                | get_version - Returns factory protocol version string.
    '''

    def create(
        self,
        dependencies: SimulationTickerDependencies,
    ) -> ISimulationTicker:
        '''
            Assembles and returns an ISimulationTicker instance.

            :param dependencies: Parameter bundle containing external collaborators.
            :return: Configured simulation ticker instance.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns factory protocol version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
