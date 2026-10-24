# -*- coding: UTF-8 -*-

'''
Module
    target_action_coordinator_test.py
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
    Unit tests for TargetActionCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.canvas.target.target_action_coordinator import TargetActionCoordinator
from scaraemu.infrastructure.gui.canvas.target.target_dependencies import TargetDependencies

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
        Mock emulation service for target action coordinator tests.
    '''
    def __init__(self) -> None:
        '''
            Initializes mock emulation service.
        '''
        self.current_pose: ScaraPose = ScaraPose(x=100.0, y=50.0, z=20.0, phi=0.0)
        self.motors_enabled: bool = True
        self.estop_active: bool = False

    def get_telemetry(self) -> Telemetry:
        '''
            Returns telemetry.
        '''
        return Telemetry(
            pose=self.current_pose,
            joints=ScaraJoints(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0, reachable=True),
            steps=ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0),
            is_hardware_connected=False,
            motors_enabled=self.motors_enabled,
            estop_active=self.estop_active,
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

    def enqueue_waypoint(self, waypoint: ScaraPose) -> bool:
        '''
            Enqueues waypoint.
        '''
        _ = waypoint
        return True


class _MockValidator:
    '''
        Unit tests for _MockValidator conforming to IMotionValidatorAdapter.
    '''
    is_ok: bool = True

    def is_pose_valid(self, pose: ScaraPose) -> bool:
        '''
            Tests is_pose_valid.
        '''
        _ = pose
        return self.is_ok

    def is_segment_valid(self, start_pose: ScaraPose, end_pose: ScaraPose) -> bool:
        '''
            Tests is_segment_valid.
        '''
        _ = (start_pose, end_pose)
        return self.is_ok

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Tests solve_fk.
        '''
        _ = joints
        return ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)

    def get_safe_radius(self) -> float:
        '''
            Tests get_safe_radius.
        '''
        return 86.08

    def get_version(self) -> str:
        '''
            Tests get_version.
        '''
        return '1.0.2'


class _MockElbowCoordinator:
    '''
        Unit tests for _MockElbowCoordinator.
    '''
    can_switch: bool = False
    switched_poses: list[ScaraPose]

    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.switched_poses = []

    def try_auto_switch(self, target_pose: ScaraPose) -> bool:
        '''
            Tests try auto switch.

            :param target_pose: Input target_pose.
            :exceptions: None.
        '''
        self.switched_poses.append(target_pose)
        return self.can_switch

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockMotionDispatcher:
    '''
        Unit tests for _MockMotionDispatcher.
    '''
    dispatched_poses: list[ScaraPose]

    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.dispatched_poses = []

    def dispatch_motion(self, target_pose: ScaraPose) -> None:
        '''
            Tests dispatch motion.

            :param target_pose: Input target_pose.
            :exceptions: None.
        '''
        self.dispatched_poses.append(target_pose)

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockLogListener:
    '''
        Unit tests for _MockLogListener.
    '''
    logs: list[tuple[str, str]]

    def __init__(self) -> None:
        '''
            Tests   init  .

            :exceptions: None.
        '''
        self.logs = []

    def append_log(self, text: str, tag: str = 'info') -> None:
        '''
            Tests append log.

            :param text: Input text.
            :param tag: Input tag.
            :exceptions: None.
        '''
        self.logs.append((text, tag))

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockDeadZoneBypassAdapter:
    '''
        Mock dead zone bypass adapter for testing TargetActionCoordinator.
    '''
    bypass_poses: list[ScaraPose] | None

    def __init__(self) -> None:
        '''
            Initializes mock bypass adapter.

            :exceptions: None.
        '''
        self.bypass_poses = None

    def plan_bypass(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> list[ScaraPose]:
        '''
            Returns configured bypass poses or direct destination pose.

            :param start_pose: Starting pose.
            :param end_pose: Destination pose.
            :return: List of poses.
            :exceptions: None.
        '''
        _ = start_pose
        if self.bypass_poses is not None:
            return self.bypass_poses
        return [end_pose]

    def is_segment_crossing_dead_zone(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Checks dead zone crossing.

            :param start_pose: Starting pose.
            :param end_pose: Destination pose.
            :return: Boolean flag.
            :exceptions: None.
        '''
        _ = (start_pose, end_pose)
        return False

    def get_safe_radius(self) -> float:
        '''
            Returns safe radius.

            :return: Radius in mm.
            :exceptions: None.
        '''
        return 75.0

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version.
            :exceptions: None.
        '''
        return '1.0.2'


class TestTargetActionCoordinator(TestCase):
    '''
        Unit tests verifying TargetActionCoordinator behavior.

        It defines:

            :methods:
                | setUp - Tests setUp.
                | test_structural_protocol_typing - Verifies TargetActionCoordinator satisfies ITargetClickListener.
                | test_handle_xy_click_valid - Verifies valid XY click dispatches motion to dispatcher.
                | test_handle_xy_click_bypass_dead_zone - Verifies bypass poses are dispatched when detour is required.
                | test_handle_xy_click_auto_switch_elbow - Verifies unreachable pose tries alternate elbow solution and succeeds.
                | test_handle_xy_click_completely_unreachable - Verifies completely unreachable pose triggers canvas flash and error log.
                | test_handle_z_click_valid - Verifies valid Z click dispatches elevation to motion dispatcher.
                | test_handle_z_click_unreachable - Verifies invalid Z elevation logs error and does not dispatch.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Tests setUp.

            :exceptions: None.
        '''
        self.emulation_service = _MockEmulationService()
        self.validator = _MockValidator()
        self.elbow_coordinator = _MockElbowCoordinator()
        self.bypass_adapter = _MockDeadZoneBypassAdapter()
        self.motion_dispatcher = _MockMotionDispatcher()
        self.log_listener = _MockLogListener()

        bundle = TargetDependencies(
            emulation_service=self.emulation_service,
            validator=self.validator,
            elbow_coordinator=self.elbow_coordinator,
            bypass_adapter=self.bypass_adapter,
            motion_dispatcher=self.motion_dispatcher,
            log_listener=self.log_listener,
        )
        self.coordinator = TargetActionCoordinator(dependencies=bundle)

    def test_structural_protocol_typing(self) -> None:
        '''
            Verifies TargetActionCoordinator satisfies ITargetClickListener.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, ITargetClickListener)

    def test_handle_xy_click_valid(self) -> None:
        '''
            Verifies valid XY click dispatches motion to dispatcher.

            :exceptions: None.
        '''
        self.validator.is_ok = True
        success = self.coordinator.handle_xy_click(150.0, 80.0)
        self.assertTrue(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 1)
        self.assertEqual(self.motion_dispatcher.dispatched_poses[0].x, 150.0)
        self.assertEqual(len(self.elbow_coordinator.switched_poses), 0)

    def test_handle_xy_click_bypass_dead_zone(self) -> None:
        '''
            Verifies bypass poses are dispatched when detour is required.

            :exceptions: None.
        '''
        self.validator.is_ok = True
        detour_wp1 = ScaraPose(x=100.0, y=50.0, z=20.0, phi=0.0)
        detour_wp2 = ScaraPose(x=-150.0, y=80.0, z=20.0, phi=0.0)
        self.bypass_adapter.bypass_poses = [detour_wp1, detour_wp2]

        success = self.coordinator.handle_xy_click(-150.0, 80.0)
        self.assertTrue(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 2)
        self.assertEqual(self.motion_dispatcher.dispatched_poses[0].x, 100.0)
        self.assertEqual(self.motion_dispatcher.dispatched_poses[1].x, -150.0)

    def test_handle_xy_click_auto_switch_elbow(self) -> None:
        '''
            Verifies unreachable pose tries alternate elbow solution and succeeds.

            :exceptions: None.
        '''
        self.validator.is_ok = False
        self.elbow_coordinator.can_switch = True

        success = self.coordinator.handle_xy_click(200.0, -100.0)
        self.assertTrue(success)
        self.assertEqual(len(self.elbow_coordinator.switched_poses), 1)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 1)
        self.assertEqual(self.motion_dispatcher.dispatched_poses[0].x, 200.0)

    def test_handle_xy_click_completely_unreachable(self) -> None:
        '''
            Verifies completely unreachable pose returns False and logs error.

            :exceptions: None.
        '''
        self.validator.is_ok = False
        self.elbow_coordinator.can_switch = False

        success = self.coordinator.handle_xy_click(999.0, 999.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_xy_click_motors_disabled(self) -> None:
        '''
            Verifies XY click when motors disabled returns False and logs error.
        '''
        self.emulation_service.motors_enabled = False
        success = self.coordinator.handle_xy_click(150.0, 80.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_xy_click_estop_active(self) -> None:
        '''
            Verifies XY click when E-stop active returns False and logs error.
        '''
        self.emulation_service.estop_active = True
        success = self.coordinator.handle_xy_click(150.0, 80.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_z_click_valid(self) -> None:
        '''
            Verifies valid Z click dispatches elevation to motion dispatcher.

            :exceptions: None.
        '''
        self.validator.is_ok = True
        success = self.coordinator.handle_z_click(45.0)
        self.assertTrue(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 1)
        self.assertEqual(self.motion_dispatcher.dispatched_poses[0].z, 45.0)

    def test_handle_z_click_unreachable(self) -> None:
        '''
            Verifies invalid Z elevation logs error and does not dispatch.

            :exceptions: None.
        '''
        self.validator.is_ok = False
        success = self.coordinator.handle_z_click(-50.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_z_click_motors_disabled(self) -> None:
        '''
            Verifies Z click when motors disabled logs error and does not dispatch.
        '''
        self.emulation_service.motors_enabled = False
        success = self.coordinator.handle_z_click(45.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_z_click_estop_active(self) -> None:
        '''
            Verifies Z click when E-stop active logs error and does not dispatch.
        '''
        self.emulation_service.estop_active = True
        success = self.coordinator.handle_z_click(45.0)
        self.assertFalse(success)
        self.assertEqual(len(self.motion_dispatcher.dispatched_poses), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
