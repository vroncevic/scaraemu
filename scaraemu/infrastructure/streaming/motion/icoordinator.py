# -*- coding: UTF-8 -*-

'''
Module
    icoordinator.py
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
    Interface protocol for hardware motion trajectory coordination and point moves.
'''

from __future__ import annotations

from collections.abc import Sequence
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
class IMotionCoordinator(Protocol):
    '''
        Structural protocol defining hardware motion trajectory coordination.

        It defines:

            :methods:
                | send_hardware_move - Streams point move target pose to hardware.
                | enqueue_hardware_trajectory - Enqueues waypoints for streaming with flow control.
                | get_version - Returns interface version string.
    '''

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Streams point move target pose to hardware.

            :param pose: Target ScaraPose.
            :exceptions: None.
        '''

    def enqueue_hardware_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Enqueues waypoints for streaming with flow control.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
