# -*- coding: UTF-8 -*-

'''
Module
    iemulator_service.py
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
    Defines interface for SCARA trajectory simulation and emulator core service.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.scara_joints import ScaraJoints
from scaraemu.core.model.telemetry_dto import TelemetryDTO
from scaraemu.core.model.simulation_state_dto import SimulationStateDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEmulatorService(Protocol):
    '''
        Interface for SCARA motion emulation and queue interpolation.

        It defines:

            :methods:
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
                | set_hardware_connected - Sets hardware bridge connection state.
                | update_hardware_pose - Updates current robot pose from hardware telemetry.
    '''

    def update_hardware_pose(self, pose: ScaraPose) -> None:
        '''
            Updates current robot pose from hardware telemetry.

            :param pose: ScaraPose from hardware.
            :exceptions: None.
        '''

    def get_current_pose(self) -> ScaraPose:
        '''
            Returns current Cartesian pose.

            :return: ScaraPose instance.
            :exceptions: None.
        '''

    def get_current_joints(self) -> ScaraJoints:
        '''
            Returns current joint positions.

            :return: ScaraJoints instance.
            :exceptions: None.
        '''

    def set_target_pose(self, pose: ScaraPose, direct: bool = False) -> bool:
        '''
            Commands robot to new target pose.

            :param pose: Target ScaraPose.
            :param direct: If True, moves immediately without interpolation queue.
            :return: True if target is valid and reachable, False otherwise.
            :exceptions: None.
        '''

    def enqueue_trajectory(self, poses: Sequence[ScaraPose]) -> int:
        '''
            Appends sequence of waypoints to motion queue.

            :param poses: Sequence of target ScaraPose waypoints.
            :return: Count of successfully enqueued waypoints.
            :exceptions: None.
        '''

    def step_simulation(self) -> bool:
        '''
            Advances motion queue by one simulation step.

            :return: True if robot position changed, False if idle.
            :exceptions: None.
        '''

    def clear_queue(self) -> None:
        '''
            Clears pending motion queue and path trail.

            :exceptions: None.
        '''

    def get_telemetry(self) -> TelemetryDTO:
        '''
            Returns current TelemetryDTO snapshot.

            :return: TelemetryDTO instance.
            :exceptions: None.
        '''

    def get_simulation_state(self) -> SimulationStateDTO:
        '''
            Returns SimulationStateDTO.

            :return: SimulationStateDTO instance.
            :exceptions: None.
        '''

    def set_elbow_mode(self, elbow_left: bool) -> None:
        '''
            Toggles elbow orientation mode.

            :param elbow_left: True for Lefty mode, False for Righty mode.
            :exceptions: None.
        '''

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables stepper motor drivers.

            :param enabled: True to enable, False to disable.
            :exceptions: None.
        '''

    def set_estop(self, active: bool) -> None:
        '''
            Sets emergency stop state.

            :param active: True to engage E-STOP, False to clear.
            :exceptions: None.
        '''

    def set_hold(self, active: bool) -> None:
        '''
            Sets feed-hold pause state.

            :param active: True to pause motion queue, False to resume.
            :exceptions: None.
        '''

    def set_hardware_connected(self, connected: bool) -> None:
        '''
            Sets hardware bridge connection state.

            :param connected: True if connected, False otherwise.
            :exceptions: None.
        '''
