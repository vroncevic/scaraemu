# -*- coding: UTF-8 -*-

'''
Module
    target_motion_dispatcher.py
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
    Dispatches validated target motions to trajectory queue and hardware motion port.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TargetMotionDispatcher:
    '''
        Enqueues target poses into motion trajectory and sends hardware moves.

        It defines:

            :attributes:
                | _emulation_queue - FIFO motion emulation queue.
                | _motion_port - Hardware bridge motion streaming port.
            :methods:
                | __init__ - Initializes dispatcher with queue and motion port.
                | dispatch_motion - Enqueues pose and sends hardware move command.
                | get_version - Returns dispatcher component version string.
    '''

    _emulation_queue: IEmulationQueue
    _motion_port: IMotionCoordinator

    def __init__(
        self,
        *,
        emulation_queue: IEmulationQueue,
        motion_port: IMotionCoordinator,
    ) -> None:
        '''
            Initializes dispatcher with queue and motion port.

            :param emulation_queue: FIFO motion emulation queue.
            :param motion_port: Hardware bridge motion streaming port.
            :exceptions: None.
        '''
        self._emulation_queue: Final[IEmulationQueue] = emulation_queue
        self._motion_port: Final[IMotionCoordinator] = motion_port

    def dispatch_motion(self, target_pose: ScaraPose) -> None:
        '''
            Enqueues pose and sends hardware move command.

            :param target_pose: Validated target pose to dispatch.
            :exceptions: None.
        '''
        self._emulation_queue.enqueue_waypoint(target_pose)
        self._motion_port.send_hardware_move(target_pose)

    def get_version(self) -> str:
        '''
            Returns dispatcher component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
