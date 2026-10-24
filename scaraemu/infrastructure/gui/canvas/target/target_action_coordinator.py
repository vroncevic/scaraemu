# -*- coding: UTF-8 -*-

'''
Module
    target_action_coordinator.py
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
    Coordinates canvas target click interactions and inverse kinematics resolution.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.target.ielbow_auto_switch_coordinator import IElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.itarget_motion_dispatcher import ITargetMotionDispatcher
from scaraemu.infrastructure.gui.canvas.target.target_dependencies import TargetDependencies
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TargetActionCoordinator:
    '''
        Coordinates planar XY and elevation Z canvas click events with kinematics and safety validation.

        It defines:

            :attributes:
                | _emulation_service - Active emulation and telemetry query port.
                | _validator - Motion safety and reachability validator adapter.
                | _elbow_coordinator - Elbow auto-switch coordinator.
                | _motion_dispatcher - Target motion queue and stream dispatcher.
                | _log_listener - Logging sink for host diagnostics.
                | _bypass_adapter - Dead zone avoidance bypass trajectory adapter port.
            :methods:
                | handle_xy_click - Handles click on planar XY canvas.
                | handle_z_click - Handles click on vertical Z canvas.
                | get_version - Returns coordinator component version.
    '''

    _emulation_service: IEmulationService
    _validator: IMotionValidatorAdapter
    _elbow_coordinator: IElbowAutoSwitchCoordinator
    _motion_dispatcher: ITargetMotionDispatcher
    _log_listener: ILogListener
    _bypass_adapter: IDeadZoneBypassAdapter

    def __init__(
        self,
        dependencies: TargetDependencies,
    ) -> None:
        '''
            Initializes canvas target action coordinator with dependencies bundle.

            :param dependencies: Target action coordinator dependencies bundle.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = (
            dependencies.emulation_service
        )
        self._validator: Final[IMotionValidatorAdapter] = dependencies.validator
        self._elbow_coordinator: Final[IElbowAutoSwitchCoordinator] = (
            dependencies.elbow_coordinator
        )
        self._motion_dispatcher: Final[ITargetMotionDispatcher] = (
            dependencies.motion_dispatcher
        )
        self._log_listener: Final[ILogListener] = dependencies.log_listener
        self._bypass_adapter: Final[IDeadZoneBypassAdapter] = (
            dependencies.bypass_adapter
        )

    def handle_xy_click(self, x: float, y: float) -> bool:
        '''
            Handles click on XY planar canvas.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :return: True if target dispatched, False if rejected or unreachable.
            :exceptions: None.
        '''
        telem = self._emulation_service.get_telemetry()

        if not telem.motors_enabled:
            self._log_listener.append_log(
                f'[HOST]: Target ({x:.1f}, {y:.1f}) unreachable: Motors disabled',
                'err',
            )

            return False

        if telem.estop_active:
            self._log_listener.append_log(
                f'[HOST]: Target ({x:.1f}, {y:.1f}) unreachable: E-Stop active',
                'err',
            )

            return False

        curr: ScaraPose = telem.pose
        new_pose: ScaraPose = ScaraPose(x=x, y=y, z=curr.z, phi=curr.phi)
        ok: bool = self._validator.is_pose_valid(new_pose)

        if not ok:
            ok = self._elbow_coordinator.try_auto_switch(new_pose)

        if ok:
            bypass_poses: list[ScaraPose] = self._bypass_adapter.plan_bypass(curr, new_pose)

            for pose in bypass_poses:
                self._motion_dispatcher.dispatch_motion(pose)

            return True

        self._log_listener.append_log(
            f'[HOST]: Target ({x:.1f}, {y:.1f}) unreachable: Outside reachable workspace',
            'err',
        )

        return False

    def handle_z_click(self, z: float) -> bool:
        '''
            Handles click on Z vertical canvas.

            :param z: Target Z in mm.
            :return: True if target dispatched, False if rejected or unreachable.
            :exceptions: None.
        '''
        telem = self._emulation_service.get_telemetry()

        if not telem.motors_enabled:
            self._log_listener.append_log(
                f'[HOST]: Elevation Z={z:.1f} unreachable: Motors disabled',
                'err',
            )

            return False

        if telem.estop_active:
            self._log_listener.append_log(
                f'[HOST]: Elevation Z={z:.1f} unreachable: E-Stop active',
                'err',
            )

            return False

        curr: ScaraPose = telem.pose
        new_pose: ScaraPose = ScaraPose(x=curr.x, y=curr.y, z=z, phi=curr.phi)

        if self._validator.is_pose_valid(new_pose):
            self._motion_dispatcher.dispatch_motion(new_pose)

            return True

        self._log_listener.append_log(
            f'[HOST]: Elevation Z={z:.1f} unreachable: Outside reachable workspace',
            'err',
        )

        return False

    def get_version(self) -> str:
        '''
            Returns coordinator component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
