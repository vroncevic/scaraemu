# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Coordinates trajectory demonstration preset generation and enqueuing actions.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPresetCoordinator:
    '''
        Coordinates trajectory demonstration preset generation and enqueuing actions.

        It defines:

            :attributes:
                | _emulation_service - Active emulation and telemetry query port.
                | _emulation_queue - FIFO motion emulation waypoint queue.
                | _motion_port - Hardware bridge motion streaming port.
                | _demo_adapter - Demonstration trajectory generator adapter port.
            :methods:
                | __init__ - Initializes preset coordinator with collaborators.
                | handle_demo_select - Generates and queues demo trajectory waypoints.
                | get_version - Returns coordinator component version string.
    '''

    _emulation_service: IEmulationService
    _emulation_queue: IEmulationQueue
    _motion_port: IMotionCoordinator
    _demo_adapter: ITrajectoryDemoAdapter

    def __init__(
        self,
        *,
        emulation_service: IEmulationService,
        emulation_queue: IEmulationQueue,
        motion_port: IMotionCoordinator,
        demo_adapter: ITrajectoryDemoAdapter,
    ) -> None:
        '''
            Initializes preset coordinator with emulation service, queue, motion port, and demo adapter.

            :param emulation_service: Active emulation service port.
            :param emulation_queue: Active emulation waypoint queue port.
            :param motion_port: Hardware bridge motion streaming port.
            :param demo_adapter: Demonstration trajectory generator adapter port.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = emulation_service
        self._emulation_queue: Final[IEmulationQueue] = emulation_queue
        self._motion_port: Final[IMotionCoordinator] = motion_port
        self._demo_adapter: Final[ITrajectoryDemoAdapter] = demo_adapter

    def handle_demo_select(self, preset_name: str) -> None:
        '''
            Generates and queues demo trajectory waypoints.

            :param preset_name: Demo trajectory preset name.
            :exceptions: None.
        '''
        curr: ScaraPose = self._emulation_service.get_telemetry().pose
        poses: list[ScaraPose] = self._demo_adapter.generate(
            preset_name, center_x=curr.x, center_y=curr.y, z=curr.z
        )

        if poses:
            for pose in poses:
                self._emulation_queue.enqueue_waypoint(pose)

            self._motion_port.enqueue_hardware_trajectory(poses)

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
