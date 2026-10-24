# -*- coding: UTF-8 -*-

'''
Module
    ipumper.py
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
    Structural protocol for pumping queued motion packets across transport.
'''

from __future__ import annotations

from collections import deque
from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IQueuePumper(Protocol):
    '''
        Structural protocol defining queue packet pumping across transport.

        It defines:

            :methods:
                | pump - Dispatches pending poses within available flow window slots.
                | get_version - Returns queue pumper protocol version.
    '''

    def pump(self, queue: deque[ScaraPose]) -> None:
        '''
            Dispatches pending poses within available flow window slots.

            :param queue: Pending queue of ScaraPose instances.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns queue pumper protocol version.

            :return: Semantic version string.
            :exceptions: None.
        '''
