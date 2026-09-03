# -*- coding: UTF-8 -*-

'''
Module
    emulator_service.py
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
    Core runtime simulation and motion interpolation service implementation.
'''

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from typing import Final

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.core.model.telemetry_dto import TelemetryDTO
from scaraemu.core.model.simulation_state_dto import SimulationStateDTO
from scaraemu.core.service.ikinematics_service import IKinematicsService
from scaraemu.core.service.iemulator_service import IEmulatorService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorService(IEmulatorService):
    '''
        Trajectory queue simulation and real-time motion playback engine.

        It defines:

            :attributes:
                | MAX_TRAIL_LENGTH - Maximum number of historical trajectory points.
                | _kinematics - IKinematicsService forward and inverse solver.
                | _current_pose - Current simulated Cartesian pose.
                | _current_joints - Current calculated joint configuration.
                | _active_target - Current target pose being tracked.
                | _elbow_left - Active elbow orientation configuration flag.
                | _motors_enabled - Stepper motor driver power state.
                | _estop_active - Emergency stop engagement flag.
                | _hold_active - Feed-hold pause engagement flag.
                | _motion_queue - FIFO queue of interpolated waypoint poses.
                | _trail_points - Fixed-size historical XY coordinate trail buffer.
                | _is_hardware_connected - Hardware bridge active status flag.
            :methods:
                | __init__ - Initializes the emulator simulation service.
                | get_current_pose - Returns current Cartesian pose.
                | get_current_joints - Returns current joint positions.
                | set_target_pose - Commands robot to new target pose.
                | enqueue_trajectory - Appends sequence of waypoints to motion queue.
                | step_simulation - Advances motion queue by one simulation step.
                | clear_queue - Clears pending motion queue and path trail.
                | get_telemetry - Returns current TelemetryDTO snapshot.
                | get_simulation_state - Returns SimulationStateDTO.
                | set_elbow_mode - Toggles elbow orientation mode.
                | set_motors_enabled - Enables or disables stepper motor drivers.
                | set_estop - Sets emergency stop state.
                | set_hold - Sets feed-hold pause state.
                | set_hardware_connected - Updates hardware connection state.
                | update_hardware_pose - Updates current robot pose from hardware telemetry.
    '''

    MAX_TRAIL_LENGTH: Final[int] = 1000

    _kinematics: IKinematicsService
    _current_pose: ScaraPose
    _current_joints: ScaraJoints
    _active_target: ScaraPose | None
    _elbow_left: bool
    _motors_enabled: bool
    _estop_active: bool
    _hold_active: bool
    _motion_queue: deque[ScaraPose]
    _trail_points: deque[tuple[float, float]]
    _is_hardware_connected: bool

    def __init__(
        self,
        kinematics: IKinematicsService,
        initial_pose: ScaraPose | None = None
    ) -> None:
        '''
            Initializes the emulator simulation service.

            :param kinematics: IKinematicsService solver instance.
            :param initial_pose: Optional starting Cartesian pose.
            :exceptions: None.
        '''
        self._kinematics = kinematics
        self._elbow_left = False
        self._motors_enabled = True
        self._estop_active = False
        self._hold_active = False
        self._is_hardware_connected = False
        self._active_target = None

        self._current_pose = initial_pose if initial_pose is not None else ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        self._current_joints = self._kinematics.solve_ik(self._current_pose, self._elbow_left)

        self._motion_queue = deque()
        self._trail_points = deque(maxlen=self.MAX_TRAIL_LENGTH)
        self._trail_points.append((self._current_pose.x, self._current_pose.y))

    def get_current_pose(self) -> ScaraPose:
        '''
            Returns current Cartesian pose.

            :return: ScaraPose instance.
            :exceptions: None.
        '''
        return self._current_pose

    def get_current_joints(self) -> ScaraJoints:
        '''
            Returns current joint positions.

            :return: ScaraJoints instance.
            :exceptions: None.
        '''
        return self._current_joints

    def set_target_pose(self, pose: ScaraPose, direct: bool = False) -> bool:
        '''
            Commands robot to new target pose.

            :param pose: Target ScaraPose.
            :param direct: If True, moves immediately without interpolation queue.
            :return: True if target is valid and reachable, False otherwise.
            :exceptions: None.
        '''
        if not self._motors_enabled or self._estop_active:
            return False

        if not self._kinematics.is_reachable(pose.x, pose.y):
            return False

        joints: ScaraJoints = self._kinematics.solve_ik(pose, self._elbow_left)
        if not joints.reachable:
            return False

        self._active_target = pose

        if direct:
            self._current_pose = pose
            self._current_joints = joints
            self._trail_points.append((pose.x, pose.y))
            return True

        if not self._is_hardware_connected:
            sub_points: list[ScaraPose] = self._kinematics.interpolate_linear(
                self._current_pose,
                pose,
                segment_len_mm=1.5
            )
            for pt in sub_points:
                self._motion_queue.append(pt)

        return True

    def enqueue_trajectory(self, poses: Sequence[ScaraPose]) -> int:
        '''
            Appends sequence of waypoints to motion queue with fine linear interpolation.

            :param poses: Sequence of target ScaraPose waypoints.
            :return: Count of successfully enqueued waypoints.
            :exceptions: None.
        '''
        if not self._motors_enabled or self._estop_active or not poses:
            return 0

        if self._is_hardware_connected:
            self._active_target = poses[-1] if poses else None
            return len(poses)

        last_p: ScaraPose = self._motion_queue[-1] if self._motion_queue else self._current_pose
        count: int = 0

        for target in poses:
            if not self._kinematics.is_reachable(target.x, target.y):
                continue

            sub_points: list[ScaraPose] = self._kinematics.interpolate_linear(
                last_p,
                target,
                segment_len_mm=1.5
            )
            for pt in sub_points:
                self._motion_queue.append(pt)
                count += 1

            last_p = target

        return count

    def step_simulation(self) -> bool:
        '''
            Advances motion queue by one simulation step.

            :return: True if robot position changed, False if idle.
            :exceptions: None.
        '''
        if (
            self._is_hardware_connected
            or not self._motion_queue
            or not self._motors_enabled
            or self._estop_active
            or self._hold_active
        ):
            return False

        next_pose: ScaraPose = self._motion_queue.popleft()
        joints: ScaraJoints = self._kinematics.solve_ik(next_pose, self._elbow_left)

        if joints.reachable:
            self._current_pose = next_pose
            self._current_joints = joints
            self._trail_points.append((next_pose.x, next_pose.y))
            return True

        return False

    def clear_queue(self) -> None:
        '''
            Clears pending motion queue and path trail.

            :exceptions: None.
        '''
        self._active_target = None
        self._motion_queue.clear()
        self._trail_points.clear()
        self._trail_points.append((self._current_pose.x, self._current_pose.y))

    def get_telemetry(self) -> TelemetryDTO:
        '''
            Returns current TelemetryDTO snapshot.

            :return: TelemetryDTO instance.
            :exceptions: None.
        '''
        steps = self._kinematics.joints_to_steps(self._current_joints)
        return TelemetryDTO(
            pose=self._current_pose,
            joints=self._current_joints,
            steps=steps,
            is_hardware_connected=self._is_hardware_connected,
            motors_enabled=self._motors_enabled,
            estop_active=self._estop_active,
            hold_active=self._hold_active
        )

    def get_simulation_state(self) -> SimulationStateDTO:
        '''
            Returns SimulationStateDTO.

            :return: SimulationStateDTO instance.
            :exceptions: None.
        '''
        target = self._active_target if self._is_hardware_connected else (
            self._motion_queue[0] if self._motion_queue else None
        )
        return SimulationStateDTO(
            is_animating=len(self._motion_queue) > 0 and not self._is_hardware_connected,
            queue_depth=len(self._motion_queue),
            trail_points=tuple(self._trail_points),
            current_target=target
        )

    def set_elbow_mode(self, elbow_left: bool) -> None:
        '''
            Toggles elbow orientation mode.

            :param elbow_left: True for Lefty mode, False for Righty mode.
            :exceptions: None.
        '''
        self._elbow_left = elbow_left
        self._current_joints = self._kinematics.solve_ik(self._current_pose, self._elbow_left)

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables stepper motor drivers.

            :param enabled: True to enable, False to disable.
            :exceptions: None.
        '''
        self._motors_enabled = enabled

    def set_estop(self, active: bool) -> None:
        '''
            Sets emergency stop state.

            :param active: True to engage E-STOP, False to clear.
            :exceptions: None.
        '''
        self._estop_active = active
        if active:
            self._active_target = None
            self._motion_queue.clear()

    def set_hold(self, active: bool) -> None:
        '''
            Sets feed-hold pause state.

            :param active: True to pause motion queue, False to resume.
            :exceptions: None.
        '''
        self._hold_active = active

    def set_hardware_connected(self, connected: bool) -> None:
        '''
            Updates hardware connection state.

            :param connected: True if serial bridge is active, False otherwise.
            :exceptions: None.
        '''
        self._is_hardware_connected = connected

    def update_hardware_pose(self, pose: ScaraPose) -> None:
        '''
            Updates current robot pose and joints from hardware telemetry.

            :param pose: ScaraPose from hardware.
            :exceptions: None.
        '''
        self._current_pose = pose
        self._current_joints = self._kinematics.solve_ik(pose, self._elbow_left)
        self._trail_points.append((pose.x, pose.y))
