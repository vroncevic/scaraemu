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
    Coordinates manual jog displacement and homing operations.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.gui.jog.action.dependencies import JogDependencies
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogActionCoordinator:
    '''
        Coordinates incremental jog displacement and homing motion operations.

        It defines:

            :attributes:
                | _emulation_service - Active emulation and telemetry query port.
                | _emulation_queue - FIFO motion emulation waypoint queue.
                | _validator - Motion safety and reachability validator adapter.
                | _home_pose - Canonical home pose.
                | _motion_port - Hardware bridge motion streaming port.
                | _log_listener - Logging sink for host diagnostics.
            :methods:
                | handle_jog - Handles incremental jog displacement across axes.
                | handle_home - Handles homing motion command for specified axis.
                | get_version - Returns coordinator component version string.
    '''

    _emulation_service: IEmulationService
    _emulation_queue: IEmulationQueue
    _validator: IMotionValidatorAdapter
    _home_pose: ScaraPose
    _motion_port: IMotionCoordinator
    _log_listener: ILogListener

    def __init__(
        self,
        dependencies: JogDependencies,
    ) -> None:
        '''
            Initializes jog action coordinator with dependencies bundle.

            :param dependencies: Jog action coordinator dependencies bundle.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = (
            dependencies.emulation_service
        )
        self._emulation_queue: Final[IEmulationQueue] = (
            dependencies.emulation_queue
        )
        self._validator: Final[IMotionValidatorAdapter] = dependencies.validator
        self._home_pose: Final[ScaraPose] = dependencies.home_pose
        self._motion_port: Final[IMotionCoordinator] = dependencies.motion_port
        self._log_listener: Final[ILogListener] = dependencies.log_listener

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Handles manual incremental jog displacement.

            :param dx: Delta X in mm.
            :param dy: Delta Y in mm.
            :param dz: Delta Z in mm.
            :param dphi: Delta Phi in radians.
            :exceptions: None.
        '''
        telem = self._emulation_service.get_telemetry()

        if not telem.motors_enabled:
            self._log_listener.append_log(
                '[HOST]: Jog displacement unreachable: Motors disabled',
                'err',
            )
            return

        if telem.estop_active:
            self._log_listener.append_log(
                '[HOST]: Jog displacement unreachable: E-Stop active',
                'err',
            )
            return

        target: ScaraPose = ScaraPose(
            x=telem.pose.x + dx,
            y=telem.pose.y + dy,
            z=telem.pose.z + dz,
            phi=telem.pose.phi + dphi,
        )

        if self._validator.is_pose_valid(target):
            self._emulation_queue.enqueue_waypoint(target)
            self._motion_port.send_hardware_move(target)
        else:
            self._log_listener.append_log(
                '[HOST]: Jog displacement unreachable: Outside reachable workspace',
                'err',
            )

    def handle_home(self, axis: str) -> None:
        '''
            Handles homing motion for specified axis.

            :param axis: Target axis ('xy', 'z', or 'all').
            :exceptions: None.
        '''
        curr: ScaraPose = self._emulation_service.get_telemetry().pose

        match axis.lower():
            case 'xy':
                target = ScaraPose(
                    x=self._home_pose.x,
                    y=self._home_pose.y,
                    z=curr.z,
                    phi=curr.phi,
                )

            case 'z':
                target = ScaraPose(
                    x=curr.x,
                    y=curr.y,
                    z=self._home_pose.z,
                    phi=curr.phi,
                )

            case _:
                target = ScaraPose(
                    x=self._home_pose.x,
                    y=self._home_pose.y,
                    z=self._home_pose.z,
                    phi=self._home_pose.phi,
                )

        if self._validator.is_pose_valid(target):
            self._emulation_queue.enqueue_waypoint(target)
            self._motion_port.send_hardware_move(target)
        else:
            self._log_listener.append_log(
                '[HOST]: Homing target unreachable',
                'err',
            )

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
