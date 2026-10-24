# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit test cases for JogHandler component.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler
from scaraemu.infrastructure.server.handler.jog.dependencies import JogHandlerDependencies
from scaraemu.infrastructure.server.handler.jog.handler import JogHandler
from scaraemu.infrastructure.server.pose.factory import VirtualPlannedPoseHolderFactory
from scaraemu.infrastructure.server.pose.iholder import IVirtualPlannedPoseHolder

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
        Mock emulation service for jog handler tests.
    '''

    def __init__(self, initial_pose: ScaraPose) -> None:
        self.pose = initial_pose

    def step(self, dt: float) -> None:
        '''Simulates step.'''
        _ = dt

    def get_telemetry(self) -> Telemetry:
        '''Returns mock telemetry.'''
        return Telemetry(
            pose=self.pose,
            joints=ScaraJoints(theta1=0.1, theta2=0.2, z=10.0, theta4=0.0, reachable=True),
            steps=ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0),
            is_hardware_connected=False,
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )


class _MockEmulationQueue:
    '''
        Mock emulation queue for jog handler tests.
    '''

    def __init__(self) -> None:
        self.enqueued_waypoints: list[ScaraPose] = []
        self.queue_depth: int = 0

    def enqueue_waypoint(self, waypoint: ScaraPose, seq_num: int = 0) -> bool:
        '''Enqueues waypoint.'''
        _ = seq_num
        self.enqueued_waypoints.append(waypoint)
        return True

    def get_snapshot(self, fallback_pose: ScaraPose) -> EmulationQueueSnapshot:
        '''Returns mock snapshot.'''
        return EmulationQueueSnapshot(
            queue_depth=self.queue_depth,
            has_target=bool(self.enqueued_waypoints),
            current_target=self.enqueued_waypoints[-1] if self.enqueued_waypoints else fallback_pose,
            planned_path=(),
        )


class TestJogHandler(TestCase):
    '''
        Unit test cases verifying JogHandler functionality.

        It defines:

            :methods:
                | setUp - Initializes test mocks and handler instance.
                | test_structural_typing - Verifies handler satisfies IBinaryCommandHandler.
                | test_can_handle - Verifies can_handle accepts CMD_JOG_JOINT.
                | test_handle_jog_axes - Verifies jog command increments for each axis.
                | test_handle_chained_jog - Verifies chained jog moves accumulate.
                | test_handle_jog_blocked_dead_zone - Verifies NACK on unreachable target.
                | test_handle_payload_too_short - Verifies NACK on invalid payload length.
                | test_handle_unknown_joint_id - Verifies NACK on unknown joint identifier.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes test mocks and handler instance.

            :exceptions: None.
        '''
        self._kinematics: MagicMock = MagicMock(spec=IManipulatorKinematics)
        self._kinematics.solve_ik.return_value = ScaraJoints(
            theta1=0.1, theta2=0.2, z=10.0, theta4=0.0, reachable=True
        )
        self._emulation_service = _MockEmulationService(ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0))
        self._emulation_queue = _MockEmulationQueue()
        self._pose_holder: IVirtualPlannedPoseHolder = VirtualPlannedPoseHolderFactory.create()
        self._response_builder: IBinaryResponseBuilderAdapter = (
            BinaryResponseBuilderAdapterFactory.create()
        )
        self._decoder: IBinaryPayloadDecoderAdapter = BinaryPayloadDecoderAdapterFactory.create()
        deps = JogHandlerDependencies(
            emulation_service=self._emulation_service,
            emulation_queue=self._emulation_queue,
            pose_holder=self._pose_holder,
            kinematics=self._kinematics,
            response_builder=self._response_builder,
            decoder=self._decoder,
        )
        self._handler = JogHandler(dependencies=deps)

    def test_structural_typing(self) -> None:
        '''
            Verifies handler satisfies IBinaryCommandHandler protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._handler, IBinaryCommandHandler)

    def test_can_handle(self) -> None:
        '''
            Verifies can_handle accepts CMD_JOG_JOINT and rejects others.

            :exceptions: None.
        '''
        self.assertTrue(self._handler.can_handle(MessageId.CMD_JOG_JOINT))
        self.assertFalse(self._handler.can_handle(MessageId.CMD_PING))
        self.assertFalse(self._handler.can_handle(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertFalse(self._handler.can_handle(MessageId.CMD_GET_STATUS))

    def test_handle_jog_axes(self) -> None:
        '''
            Verifies jog command increments for each joint/axis.

            :exceptions: None.
        '''
        # Test Joint 0 (X axis): +10 mm
        payload_x: bytes = pack('<BiI', 0, 10, 2000)
        frame_x = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=1, payload=payload_x, crc16=0)
        responses_x = self._handler.handle(frame_x)

        self.assertEqual(len(responses_x), 2)
        self.assertEqual(responses_x[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(responses_x[1].msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertEqual(
            self._emulation_queue.enqueued_waypoints[-1],
            ScaraPose(x=110.0, y=50.0, z=10.0, phi=0.0),
        )

        # Test Joint 1 (Y axis): -5 mm
        payload_y: bytes = pack('<BiI', 1, -5, 2000)
        frame_y = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=2, payload=payload_y, crc16=0)
        responses_y = self._handler.handle(frame_y)

        self.assertEqual(len(responses_y), 2)
        self.assertEqual(responses_y[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(
            self._emulation_queue.enqueued_waypoints[-1],
            ScaraPose(x=100.0, y=45.0, z=10.0, phi=0.0),
        )

        # Test Joint 2 (Z axis): +2 mm
        payload_z: bytes = pack('<BiI', 2, 2, 2000)
        frame_z = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=3, payload=payload_z, crc16=0)
        responses_z = self._handler.handle(frame_z)

        self.assertEqual(len(responses_z), 2)
        self.assertEqual(responses_z[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(
            self._emulation_queue.enqueued_waypoints[-1],
            ScaraPose(x=100.0, y=50.0, z=12.0, phi=0.0),
        )

        # Test Joint 3 (PHI axis): +1 rad/deg
        payload_phi: bytes = pack('<BiI', 3, 1, 2000)
        frame_phi = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=4, payload=payload_phi, crc16=0)
        responses_phi = self._handler.handle(frame_phi)

        self.assertEqual(len(responses_phi), 2)
        self.assertEqual(responses_phi[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(
            self._emulation_queue.enqueued_waypoints[-1],
            ScaraPose(x=100.0, y=50.0, z=10.0, phi=1.0),
        )

    def test_handle_chained_jog(self) -> None:
        '''
            Verifies chained jog moves accumulate from planned pose holder.

            :exceptions: None.
        '''
        self._emulation_queue.queue_depth = 1
        self._pose_holder.set_planned_pose(ScaraPose(x=150.0, y=70.0, z=20.0, phi=5.0))

        payload: bytes = pack('<BiI', 0, 10, 2000)
        frame = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=10, payload=payload, crc16=0)
        responses = self._handler.handle(frame)

        self.assertEqual(len(responses), 2)
        self.assertEqual(
            self._emulation_queue.enqueued_waypoints[-1],
            ScaraPose(x=160.0, y=70.0, z=20.0, phi=5.0),
        )

    def test_handle_jog_blocked_dead_zone(self) -> None:
        '''
            Verifies NACK response when jog target is unreachable in dead zone.

            :exceptions: None.
        '''
        self._kinematics.solve_ik.return_value = ScaraJoints(
            theta1=0.0,
            theta2=0.0,
            z=0.0,
            theta4=0.0,
            reachable=False,
        )
        payload: bytes = pack('<BiI', 0, 10, 2000)
        frame = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=5, payload=payload, crc16=0)
        responses = self._handler.handle(frame)

        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].msg_id, MessageId.RESP_NACK)
        self.assertEqual(len(self._emulation_queue.enqueued_waypoints), 0)

    def test_handle_payload_too_short(self) -> None:
        '''
            Verifies NACK response when payload length is invalid.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=1, payload=b'\x00\x01', crc16=0)
        responses = self._handler.handle(frame)

        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].msg_id, MessageId.RESP_NACK)

    def test_handle_unknown_joint_id(self) -> None:
        '''
            Verifies NACK response when joint identifier is unknown.

            :exceptions: None.
        '''
        payload: bytes = pack('<BiI', 99, 10, 2000)
        frame = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=1, payload=payload, crc16=0)
        responses = self._handler.handle(frame)

        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].msg_id, MessageId.RESP_NACK)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(self._handler.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
