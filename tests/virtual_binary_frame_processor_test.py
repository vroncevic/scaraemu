# -*- coding: UTF-8 -*-

'''
Module
    virtual_binary_frame_processor_test.py
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
    Unit tests for VirtualBinaryFrameProcessor and binary streaming on VirtualRobotServer.
'''

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket as Socket
from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder import (
    BinaryFrameBuilder,
)
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import (
    BinaryFrameBuilderFactory,
)
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import (
    BinaryFrameParser,
)
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import (
    BinaryFrameParserFactory,
)
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import (
    BinaryPayloadUnpacker,
)
from scaraemu.core.model.kinematics.scara_geometry import ScaraGeometry
from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.core.model.simulation.simulation_state import SimulationState
from scaraemu.core.service.kinematics.kinematics_service import KinematicsService
from scaraemu.core.service.simulation.emulator_service import EmulatorService
from scaraemu.infrastructure.communication.server.virtual_binary_frame_processor import (
    VirtualBinaryFrameProcessor,
)
from scaraemu.infrastructure.communication.server.virtual_binary_frame_processor_factory import (
    VirtualBinaryFrameProcessorFactory,
)
from scaraemu.infrastructure.communication.server.virtual_robot_server import (
    VirtualRobotServer,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualBinaryFrameProcessor(TestCase):
    '''
        Test cases for VirtualBinaryFrameProcessor and binary wire stream processing.

        It defines:

            :methods:
                | setUp - Initializes test environment and emulator collaborators.
                | tearDown - Cleans up active server if running.
                | test_ping_command - Verifies CMD_PING produces RESP_ACK.
                | test_enable_disable_commands - Verifies motor enable/disable frames.
                | test_home_command - Verifies CMD_HOME executes homing and acks.
                | test_status_command - Verifies CMD_STATUS returns valid ScaraStatus frame.
                | test_joint_move_command - Verifies CMD_MOVE_JOINT_STEPS enqueues pose.
                | test_tool_command - Verifies tool pump/valve commands.
                | test_binary_streaming_over_socket - Verifies socket streaming of binary frames.
    '''

    def setUp(self) -> None:
        self.geom = ScaraGeometry(l1=150.0, l2=120.0)
        self.kin = KinematicsService(geometry=self.geom)
        self.emu = EmulatorService(kinematics=self.kin, initial_pose=ScaraPose(x=180.0, y=0.0, z=20.0))
        self.processor: VirtualBinaryFrameProcessor = (
            VirtualBinaryFrameProcessor(emulator=self.emu, kinematics=self.kin)
        )
        self.builder: BinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.parser: BinaryFrameParser = BinaryFrameParserFactory.create()
        self.server: VirtualRobotServer | None = None

    def tearDown(self) -> None:
        if self.server is not None:
            self.server.stop()
            self.server = None

    def test_factory_creation(self) -> None:
        proc = VirtualBinaryFrameProcessorFactory.create(emulator=self.emu, kinematics=self.kin)
        self.assertIsNotNone(proc)
        self.assertIsInstance(VirtualBinaryFrameProcessorFactory.get_version(), str)

    def test_ping_command(self) -> None:
        frame: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_PING, seq_num=1)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        acked_id, q_count = BinaryPayloadUnpacker.unpack_ack(resps[0].payload)
        self.assertEqual(acked_id, int(MessageId.CMD_PING))

    def test_enable_disable_commands(self) -> None:
        frame_en: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_ENABLE, seq_num=2)
        resps_en: list[BinaryFrame] = self.processor.process_frame(frame=frame_en)
        self.assertEqual(resps_en[0].msg_id, MessageId.RESP_ACK)
        self.assertTrue(self.emu.get_telemetry().motors_enabled)

        frame_dis: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_DISABLE, seq_num=3)
        resps_dis: list[BinaryFrame] = self.processor.process_frame(frame=frame_dis)
        self.assertEqual(resps_dis[0].msg_id, MessageId.RESP_ACK)
        self.assertFalse(self.emu.get_telemetry().motors_enabled)

    def test_home_command(self) -> None:
        frame: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=4)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(self.emu.get_current_pose(), ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0))

    def test_status_command(self) -> None:
        frame: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_GET_STATUS, seq_num=5)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_STATUS)
        status = BinaryPayloadUnpacker.unpack_scara_status(resps[0].payload)
        self.assertEqual(status.system_state, 1)

    def test_joint_move_command(self) -> None:
        steps = JointSteps(
            target_j1_steps=-971,
            target_j2_steps=3886,
            target_z_steps=8000,
            target_j4_steps=-729,
            duration_us=10000,
            feedrate_scale=100,
        )
        frame: BinaryFrame = self.builder.build_joint_move(seq_num=6, steps=steps)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 2)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(resps[1].msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertGreater(self.emu.get_simulation_state().queue_depth, 0)

    def test_tool_command(self) -> None:
        frame_pump: BinaryFrame = self.builder.build_tool_cmd(seq_num=7, tool_id=0, state=True)
        resps_pump: list[BinaryFrame] = self.processor.process_frame(frame=frame_pump)
        self.assertEqual(resps_pump[0].msg_id, MessageId.RESP_ACK)

        frame_valve: BinaryFrame = self.builder.build_tool_cmd(seq_num=8, tool_id=1, state=False)
        resps_valve: list[BinaryFrame] = self.processor.process_frame(frame=frame_valve)
        self.assertEqual(resps_valve[0].msg_id, MessageId.RESP_ACK)

    def test_stop_and_reset_fault(self) -> None:
        frame_stop: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_ESTOP, seq_num=9)
        resps_stop: list[BinaryFrame] = self.processor.process_frame(frame=frame_stop)
        self.assertEqual(resps_stop[0].msg_id, MessageId.RESP_ACK)
        self.assertTrue(self.emu.get_telemetry().estop_active)

        frame_reset: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_CLEAR_FAULT, seq_num=10)
        resps_reset: list[BinaryFrame] = self.processor.process_frame(frame=frame_reset)
        self.assertEqual(resps_reset[0].msg_id, MessageId.RESP_ACK)
        self.assertFalse(self.emu.get_telemetry().estop_active)

    def test_binary_streaming_over_socket(self) -> None:
        self.server = VirtualRobotServer(emulator=self.emu)
        self.server.start(host='127.0.0.1', port=0)
        port: int = self.server.get_port()

        client: Socket = Socket(AF_INET, SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.settimeout(2.0)

        # Send binary CMD_PING
        ping_frame: BinaryFrame = self.builder.build_system_cmd(msg_id=MessageId.CMD_PING, seq_num=21)
        wire_bytes: bytes = self.builder.pack_frame(frame=ping_frame)
        client.sendall(wire_bytes)

        recv_bytes: bytes = client.recv(1024)
        parsed_frames = self.parser.feed_bytes(recv_bytes)
        self.assertGreaterEqual(len(parsed_frames), 1)
        self.assertEqual(parsed_frames[0].msg_id, MessageId.RESP_ACK)

        client.close()


if __name__ == '__main__':
    unittest_main()
