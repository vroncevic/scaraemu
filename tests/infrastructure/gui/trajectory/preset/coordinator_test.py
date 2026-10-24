# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for TrajectoryPresetCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot
from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate
from scaraemu.infrastructure.gui.trajectory.preset.coordinator import TrajectoryPresetCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationService:
    '''
        Mock emulation service for trajectory preset coordinator tests.
    '''

    def get_telemetry(self) -> Telemetry:
        '''
            Returns telemetry.
        '''
        return Telemetry(
            pose=ScaraPose(x=100.0, y=100.0, z=-10.0, phi=0.0),
            joints=ScaraJoints(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0, reachable=True),
            steps=ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0),
            is_hardware_connected=False,
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )

    def step(self, dt: float) -> bool:
        '''
            Steps simulation.
        '''
        _ = dt
        return False

    def get_simulation_state(self) -> SimulationState:
        '''
            Returns simulation state.
        '''
        raise NotImplementedError


class _MockEmulationQueue:
    '''
        Mock emulation queue for trajectory preset coordinator tests.
    '''

    def __init__(self) -> None:
        self.poses: list[ScaraPose] = []

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''
            Enqueues waypoint.
        '''
        _ = seq_num
        self.poses.append(waypoint)
        return True

    def clear_queue(self) -> None:
        '''
            Clears waypoint queue.
        '''
        self.poses.clear()

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''
            Captures queue snapshot.
        '''
        _ = fallback_pose
        raise NotImplementedError


class _MockHardwareMotionPort:
    '''
        Mock motion port capturing hardware trajectory enqueueing.
    '''

    def __init__(self) -> None:
        '''
            Initializes trajectories storage.

            :exceptions: None.
        '''
        self.trajectories: list[list[ScaraPose]] = []

    def enqueue_hardware_trajectory(self, waypoints: list[ScaraPose]) -> None:
        '''
            Captures enqueued hardware trajectory.

            :param waypoints: Enqueued waypoints list.
            :exceptions: None.
        '''
        self.trajectories.append(waypoints)

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockDemoAdapter:
    '''
        Mock demo adapter returning dummy waypoints for circle.
    '''

    def generate(
        self,
        demo_name: str,
        center_x: float = 160.0,
        center_y: float = 0.0,
        z: float = 20.0,
    ) -> list[ScaraPose]:
        '''
            Generates demo poses.
        '''
        if demo_name == 'circle':
            return [ScaraPose(x=center_x, y=center_y, z=z, phi=0.0)]
        return []

    def get_available_demos(self) -> tuple[str, ...]:
        '''
            Returns demo list.
        '''
        return ('circle', 'square')

    def get_version(self) -> str:
        '''
            Returns mock version string.
        '''
        return '1.0.2'


class TestTrajectoryPresetCoordinator(TestCase):
    '''
        Unit tests verifying TrajectoryPresetCoordinator behavior.

        It defines:

            :methods:
                | setUp - Prepares test dependencies.
                | test_structural_protocol_conformance - Verifies TrajectoryPresetCoordinator satisfies ITrajectoryPresetDelegate.
                | test_handle_demo_select_circle - Verifies selecting circle preset enqueues waypoints into queue and motion port.
                | test_handle_demo_select_unknown - Verifies unknown preset does not enqueue waypoints.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares test dependencies.

            :exceptions: None.
        '''
        self.emulation_service = _MockEmulationService()
        self.emulation_queue = _MockEmulationQueue()
        self.motion_port = _MockHardwareMotionPort()
        self.demo_adapter = _MockDemoAdapter()
        self.coordinator = TrajectoryPresetCoordinator(
            emulation_service=self.emulation_service,
            emulation_queue=self.emulation_queue,
            motion_port=self.motion_port,
            demo_adapter=self.demo_adapter,
        )

    def test_structural_protocol_conformance(self) -> None:
        '''
            Verifies TrajectoryPresetCoordinator satisfies ITrajectoryPresetDelegate.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, ITrajectoryPresetDelegate)

    def test_handle_demo_select_circle(self) -> None:
        '''
            Verifies selecting circle preset enqueues waypoints into queue and motion port.

            :exceptions: None.
        '''
        self.coordinator.handle_demo_select('circle')
        self.assertGreater(len(self.emulation_queue.poses), 0)
        self.assertEqual(len(self.motion_port.trajectories), 1)
        self.assertEqual(self.motion_port.trajectories[0], self.emulation_queue.poses)

    def test_handle_demo_select_unknown(self) -> None:
        '''
            Verifies unknown preset does not enqueue waypoints.

            :exceptions: None.
        '''
        self.coordinator.handle_demo_select('nonexistent_preset')
        self.assertEqual(len(self.emulation_queue.poses), 0)
        self.assertEqual(len(self.motion_port.trajectories), 0)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
