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
    Unit tests for JogActionCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot
from scaraemu.infrastructure.gui.jog.action.coordinator import JogActionCoordinator
from scaraemu.infrastructure.gui.jog.action.dependencies import JogDependencies
from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationService:
    '''
        Mock emulation service for jog coordinator tests.
    '''
    def __init__(self) -> None:
        '''
            Initializes mock emulation service.

            :exceptions: None.
        '''
        self.current_pose: ScaraPose = ScaraPose(x=120.0, y=60.0, z=30.0, phi=0.0)
        self.motors_enabled: bool = True
        self.estop_active: bool = False

    def get_telemetry(self) -> Telemetry:
        '''
            Returns telemetry.

            :return: Telemetry instance.
            :exceptions: None.
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

            :param dt: Time delta.
            :return: Step flag.
            :exceptions: None.
        '''
        _ = dt
        return False

    def get_simulation_state(self) -> SimulationState:
        '''
            Returns simulation state.

            :return: Simulation state.
            :exceptions: None.
        '''
        raise NotImplementedError


class _MockEmulationQueue:
    '''
        Mock emulation queue for jog coordinator tests.
    '''
    def __init__(self) -> None:
        '''
            Initializes mock emulation queue.

            :exceptions: None.
        '''
        self.poses: list[ScaraPose] = []

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''
            Enqueues waypoint.

            :param waypoint: Waypoint pose.
            :param seq_num: Sequence number.
            :return: Success flag.
            :exceptions: None.
        '''
        _ = seq_num
        self.poses.append(waypoint)
        return True

    def clear_queue(self) -> None:
        '''
            Clears waypoint queue.

            :exceptions: None.
        '''
        self.poses.clear()

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''
            Captures queue snapshot.

            :param fallback_pose: Fallback pose.
            :return: Queue snapshot.
            :exceptions: None.
        '''
        _ = fallback_pose
        raise NotImplementedError


class _MockValidator:
    '''
        Mock validator conforming to IMotionValidatorAdapter.
    '''
    is_ok: bool = True

    def is_pose_valid(self, pose: ScaraPose) -> bool:
        '''
            Tests is_pose_valid.

            :param pose: Input pose.
            :return: Validity flag.
            :exceptions: None.
        '''
        _ = pose
        return self.is_ok

    def is_segment_valid(self, start_pose: ScaraPose, end_pose: ScaraPose) -> bool:
        '''
            Tests is_segment_valid.

            :param start_pose: Start pose.
            :param end_pose: End pose.
            :return: Validity flag.
            :exceptions: None.
        '''
        _ = (start_pose, end_pose)
        return self.is_ok

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Tests solve_fk.

            :param joints: Joints.
            :return: Forward kinematics pose.
            :exceptions: None.
        '''
        _ = joints
        return ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)

    def get_safe_radius(self) -> float:
        '''
            Tests get_safe_radius.

            :return: Safe radius.
            :exceptions: None.
        '''
        return 86.08

    def get_version(self) -> str:
        '''
            Tests get_version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockMotionPort:
    '''
        Mock motion port.
    '''
    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.moves: list[ScaraPose] = []

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Tests send hardware move.

            :param pose: Input pose.
            :exceptions: None.
        '''
        self.moves.append(pose)

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockLogListener:
    '''
        Mock log listener.
    '''
    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.logs: list[tuple[str, str]] = []

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

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestJogActionCoordinator(TestCase):
    '''
        Unit tests verifying JogActionCoordinator behavior.

        It defines:

            :methods:
                | setUp - Tests setUp.
                | test_structural_protocol_typing - Verifies JogActionCoordinator satisfies IJogActionDelegate.
                | test_handle_jog_success - Verifies incremental jog displaces from current pose and sends move.
                | test_handle_jog_unreachable - Verifies unreachable jog displacement logs error and skips move.
                | test_handle_jog_motors_disabled - Verifies jog displacement when motors disabled logs error and skips move.
                | test_handle_jog_estop_active - Verifies jog displacement when E-stop active logs error and skips move.
                | test_handle_home_xy - Verifies homing xy axis enqueues reach target with current z.
                | test_handle_home_z - Verifies homing z axis preserves planar xy and updates elevation.
                | test_handle_home_all - Verifies homing all axes resets xy and z.
                | test_handle_home_unreachable - Verifies homing target unreachable logs error.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Tests setUp.

            :exceptions: None.
        '''
        self.emulation_service = _MockEmulationService()
        self.emulation_queue = _MockEmulationQueue()
        self.validator = _MockValidator()
        self.home_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        self.motion_port = _MockMotionPort()
        self.log_listener = _MockLogListener()

        bundle = JogDependencies(
            emulation_service=self.emulation_service,
            emulation_queue=self.emulation_queue,
            validator=self.validator,
            home_pose=self.home_pose,
            motion_port=self.motion_port,
            log_listener=self.log_listener,
        )
        self.coordinator = JogActionCoordinator(dependencies=bundle)

    def test_structural_protocol_typing(self) -> None:
        '''
            Verifies JogActionCoordinator satisfies IJogActionDelegate.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IJogActionDelegate)

    def test_handle_jog_success(self) -> None:
        '''
            Verifies incremental jog displaces from current pose and sends move.

            :exceptions: None.
        '''
        self.validator.is_ok = True
        self.coordinator.handle_jog(10.0, -5.0, 2.0, 0.1)
        self.assertEqual(len(self.emulation_queue.poses), 1)
        self.assertAlmostEqual(self.emulation_queue.poses[0].x, 130.0)
        self.assertAlmostEqual(self.emulation_queue.poses[0].y, 55.0)
        self.assertEqual(len(self.motion_port.moves), 1)

    def test_handle_jog_unreachable(self) -> None:
        '''
            Verifies unreachable jog displacement logs error and skips move.

            :exceptions: None.
        '''
        self.validator.is_ok = False
        self.coordinator.handle_jog(500.0, 500.0, 0.0, 0.0)
        self.assertEqual(len(self.emulation_queue.poses), 0)
        self.assertEqual(len(self.motion_port.moves), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_jog_motors_disabled(self) -> None:
        '''
            Verifies jog displacement when motors disabled logs error and skips move.

            :exceptions: None.
        '''
        self.emulation_service.motors_enabled = False
        self.coordinator.handle_jog(10.0, 0.0, 0.0, 0.0)
        self.assertEqual(len(self.emulation_queue.poses), 0)
        self.assertEqual(len(self.motion_port.moves), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_jog_estop_active(self) -> None:
        '''
            Verifies jog displacement when E-stop active logs error and skips move.

            :exceptions: None.
        '''
        self.emulation_service.estop_active = True
        self.coordinator.handle_jog(10.0, 0.0, 0.0, 0.0)
        self.assertEqual(len(self.emulation_queue.poses), 0)
        self.assertEqual(len(self.motion_port.moves), 0)
        self.assertEqual(len(self.log_listener.logs), 1)

    def test_handle_home_xy(self) -> None:
        '''
            Verifies homing xy axis enqueues reach target with current z.

            :exceptions: None.
        '''
        self.coordinator.handle_home('xy')
        self.assertEqual(len(self.emulation_queue.poses), 1)
        self.assertEqual(self.emulation_queue.poses[0].x, 180.0)
        self.assertEqual(self.emulation_queue.poses[0].y, 0.0)
        self.assertEqual(self.emulation_queue.poses[0].z, 30.0)

    def test_handle_home_z(self) -> None:
        '''
            Verifies homing z axis preserves planar xy and updates elevation.

            :exceptions: None.
        '''
        self.coordinator.handle_home('z')
        self.assertEqual(len(self.emulation_queue.poses), 1)
        self.assertEqual(self.emulation_queue.poses[0].x, 120.0)
        self.assertEqual(self.emulation_queue.poses[0].y, 60.0)
        self.assertEqual(self.emulation_queue.poses[0].z, 20.0)

    def test_handle_home_all(self) -> None:
        '''
            Verifies homing all axes resets xy and z.

            :exceptions: None.
        '''
        self.coordinator.handle_home('all')
        self.assertEqual(len(self.emulation_queue.poses), 1)
        self.assertEqual(self.emulation_queue.poses[0].x, 180.0)
        self.assertEqual(self.emulation_queue.poses[0].y, 0.0)
        self.assertEqual(self.emulation_queue.poses[0].z, 20.0)
        self.assertEqual(self.emulation_queue.poses[0].phi, 0.0)

    def test_handle_home_unreachable(self) -> None:
        '''
            Verifies homing target unreachable logs error.

            :exceptions: None.
        '''
        self.validator.is_ok = False
        self.coordinator.handle_home('all')
        self.assertEqual(len(self.emulation_queue.poses), 0)
        self.assertIn(('[HOST]: Homing target unreachable', 'err'), self.log_listener.logs)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
