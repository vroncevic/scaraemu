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
    Unit tests for MotionHandler.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler
from scaraemu.infrastructure.server.handler.motion.dependencies import MotionHandlerDependencies
from scaraemu.infrastructure.server.handler.motion.handler import MotionHandler
from scaraemu.infrastructure.server.pose.factory import VirtualPlannedPoseHolderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockServerLogListener:
    '''
        Mock server log listener collecting logged messages for test verification.
    '''

    messages: list[str]

    def __init__(self) -> None:
        self.messages = []

    def on_server_log(self, message: str) -> None:
        '''Records server log message.'''
        self.messages.append(message)

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class TestMotionHandler(TestCase):
    '''
        Unit test cases verifying MotionHandler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures and dependencies.
                | test_structural_typing - Verifies MotionHandler satisfies IBinaryCommandHandler.
                | test_can_handle - Verifies can_handle accepts motion message IDs.
                | test_get_status_command - Verifies status command generates RESP_STATUS.
                | test_joint_move_command - Verifies joint move enqueues pose and returns ACK.
                | test_joint_move_rejected_when_violating_dead_zone - Verifies rejected move returns NACK.
                | test_version - Verifies get_version returns string.
                | test_unhandled_frame - Verifies wildcard branch returns empty list.
    '''

    log_listener: _MockServerLogListener

    def setUp(self) -> None:
        '''
            Prepares test fixtures and dependencies.

            :exceptions: None.
        '''
        self.kin: IManipulatorKinematics = KinematicsAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds(),
            transmission=DefaultScaraProfile.create_transmission(),
        )
        self.initial_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        emu_deps = EmulationDependencies(
            kinematics=self.kin,
            initial_pose=self.initial_pose,
        )
        emu_provides = EmulationFactory.create(dependencies=emu_deps)
        self.emu = emu_provides.service
        self.queue = emu_provides.queue
        self.response_builder: IBinaryResponseBuilderAdapter = (
            BinaryResponseBuilderAdapterFactory.create()
        )
        self.decoder: IBinaryPayloadDecoderAdapter = BinaryPayloadDecoderAdapterFactory.create()
        self.pose_holder = VirtualPlannedPoseHolderFactory.create()
        self.validator = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        self.log_listener = _MockServerLogListener()
        deps = MotionHandlerDependencies(
            emulation_service=self.emu,
            emulation_queue=self.queue,
            pose_holder=self.pose_holder,
            kinematics=self.kin,
            validator=self.validator,
            response_builder=self.response_builder,
            decoder=self.decoder,
            log_listener=self.log_listener,
        )
        self.handler = MotionHandler(dependencies=deps)

    def test_structural_typing(self) -> None:
        '''
            Verifies MotionHandler satisfies IBinaryCommandHandler structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler, IBinaryCommandHandler)

    def test_can_handle(self) -> None:
        '''
            Verifies can_handle accepts motion message IDs and rejects others.

            :exceptions: None.
        '''
        self.assertTrue(self.handler.can_handle(MessageId.CMD_GET_STATUS))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_PING))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_TOOL_PUMP))

    def test_get_status_command(self) -> None:
        '''
            Verifies status command generates RESP_STATUS.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_GET_STATUS, seq_num=1, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_STATUS)

    def test_joint_move_command(self) -> None:
        '''
            Verifies joint move enqueues pose and returns ACK.

            :exceptions: None.
        '''
        safe_target = ScaraPose(x=190.0, y=10.0, z=20.0, phi=0.0)
        joints = self.kin.solve_ik(safe_target, elbow_left=True)
        step_coords = self.kin.joints_to_steps(joints)
        payload = pack(
            '<iiiiIH',
            step_coords.j1_steps,
            step_coords.j2_steps,
            step_coords.z_steps,
            step_coords.j4_steps,
            10000,
            100,
        )
        frame = BinaryFrame(msg_id=MessageId.CMD_MOVE_JOINT_STEPS, seq_num=2, payload=payload, crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 1)
        self.assertEqual(len(self.log_listener.messages), 1)
        self.assertIn('Waypoint enqueued', self.log_listener.messages[0])

    def test_joint_move_rejected_when_violating_dead_zone(self) -> None:
        '''
            Verifies joint move crossing dead zone returns RESP_NACK and does not enqueue.

            :exceptions: None.
        '''
        opposite_target = ScaraPose(x=-180.0, y=0.0, z=20.0, phi=0.0)
        joints = self.kin.solve_ik(opposite_target, elbow_left=True)
        step_coords = self.kin.joints_to_steps(joints)
        payload = pack(
            '<iiiiIH',
            step_coords.j1_steps,
            step_coords.j2_steps,
            step_coords.z_steps,
            step_coords.j4_steps,
            10000,
            200,
        )
        frame = BinaryFrame(msg_id=MessageId.CMD_MOVE_JOINT_STEPS, seq_num=3, payload=payload, crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_NACK)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 0)
        self.assertEqual(len(self.log_listener.messages), 1)
        self.assertIn('Motion rejected', self.log_listener.messages[0])

    def test_version(self) -> None:
        '''
            Verifies get_version returns string.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler.get_version(), str)

    def test_unhandled_frame(self) -> None:
        '''
            Verifies wildcard branch returns empty list for unhandled message ID.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_TOOL_PUMP, seq_num=99, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest_main()
