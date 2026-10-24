# -*- coding: UTF-8 -*-

'''
Module
    processor_test.py
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
    Unit tests for VirtualBinaryFrameProcessor.
'''

from __future__ import annotations

from struct import pack, unpack
from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.service import EmulationService
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.server.processor.dependencies import BinaryProcessorDependencies
from scaraemu.infrastructure.server.processor.factory import VirtualBinaryFrameProcessorFactory
from scaraemu.infrastructure.server.processor.iprocessor import IVirtualBinaryFrameProcessor
from scaraemu.infrastructure.server.processor.processor import VirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyServerLogListener:
    '''
        Dummy server log listener for tests.
    '''

    def on_server_log(self, message: str) -> None:
        '''Handles log message.'''
        _ = message

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class TestVirtualBinaryFrameProcessor(TestCase):
    '''
        Unit tests for VirtualBinaryFrameProcessor.

        It defines:

            :methods:
                | setUp - Prepares emulation and processor dependencies.
                | test_structural_typing - Verifies satisfies IVirtualBinaryFrameProcessor.
                | test_reset - Verifies reset executes without exceptions.
                | test_unknown_frame_nack - Verifies unhandled message ID produces RESP_NACK.
                | test_ping_command - Verifies CMD_PING produces RESP_ACK.
                | test_enable_disable_commands - Verifies motor enable/disable frames.
                | test_home_command - Verifies CMD_HOME executes homing and acks.
                | test_status_command - Verifies CMD_STATUS returns valid ScaraStatus frame.
                | test_joint_move_command - Verifies CMD_MOVE_JOINT_STEPS enqueues pose.
                | test_jog_command - Verifies CMD_JOG_JOINT moves robot and returns ACK.
                | test_tool_command - Verifies tool pump/valve commands.
                | test_stop_and_reset_fault - Verifies estop and clear fault commands.
                | test_version - Verifies get_version returns string.
    '''

    kin: IManipulatorKinematics
    emu: EmulationService
    response_builder: IBinaryResponseBuilderAdapter
    codec: IBinaryFrameCodecAdapter
    processor: VirtualBinaryFrameProcessor

    def setUp(self) -> None:
        '''
            Prepares emulation and processor dependencies.

            :exceptions: None.
        '''
        self.kin = KinematicsAdapterFactory.create(
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
        self.response_builder = BinaryResponseBuilderAdapterFactory.create()
        self.codec = BinaryFrameCodecAdapterFactory.create()
        self.decoder = BinaryPayloadDecoderAdapterFactory.create()

        motion_validator = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        dependencies = BinaryProcessorDependencies(
            emulation_controller=emu_provides.controller,
            emulation_service=emu_provides.service,
            emulation_queue=emu_provides.queue,
            kinematics=self.kin,
            response_builder=self.response_builder,
            decoder=self.decoder,
            home_pose=self.initial_pose,
            motion_validator=motion_validator,
            log_listener=_DummyServerLogListener(),
        )
        self.processor = VirtualBinaryFrameProcessorFactory.create(
            dependencies=dependencies,
        )

    def test_structural_typing(self) -> None:
        '''
            Verifies VirtualBinaryFrameProcessor satisfies IVirtualBinaryFrameProcessor.

            :exceptions: None.
        '''
        self.assertIsInstance(self.processor, IVirtualBinaryFrameProcessor)

    def test_reset(self) -> None:
        '''
            Verifies reset executes without exceptions.

            :exceptions: None.
        '''
        self.processor.reset()

    def test_unknown_frame_nack(self) -> None:
        '''
            Verifies unhandled message ID produces RESP_NACK.

            :exceptions: None.
        '''
        unknown_frame = BinaryFrame(msg_id=MessageId.RESP_NACK, seq_num=99, payload=b'', crc16=0)
        resps = self.processor.process_frame(frame=unknown_frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_NACK)

    def test_ping_command(self) -> None:
        '''
            Verifies CMD_PING produces RESP_ACK.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=0)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        acked_id, _ = unpack('<BB', resps[0].payload[:2])
        self.assertEqual(acked_id, int(MessageId.CMD_PING))

    def test_enable_disable_commands(self) -> None:
        '''
            Verifies motor enable/disable frames.

            :exceptions: None.
        '''
        frame_en = BinaryFrame(msg_id=MessageId.CMD_ENABLE, seq_num=2, payload=b'', crc16=0)
        resps_en: list[BinaryFrame] = self.processor.process_frame(frame=frame_en)
        self.assertEqual(resps_en[0].msg_id, MessageId.RESP_ACK)
        acked_id, q_count = unpack('<BB', resps_en[0].payload[:2])
        self.assertEqual(acked_id, int(MessageId.CMD_ENABLE))
        self.assertEqual(q_count, 16)
        self.assertTrue(self.emu.get_telemetry().motors_enabled)

        frame_dis = BinaryFrame(msg_id=MessageId.CMD_DISABLE, seq_num=3, payload=b'', crc16=0)
        resps_dis: list[BinaryFrame] = self.processor.process_frame(frame=frame_dis)
        self.assertEqual(resps_dis[0].msg_id, MessageId.RESP_ACK)
        self.assertFalse(self.emu.get_telemetry().motors_enabled)

    def test_home_command(self) -> None:
        '''
            Verifies CMD_HOME executes homing and acks.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_HOME, seq_num=4, payload=b'', crc16=0)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 1)

    def test_status_command(self) -> None:
        '''
            Verifies CMD_STATUS returns valid ScaraStatus frame.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_GET_STATUS, seq_num=5, payload=b'', crc16=0)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_STATUS)
        is_moving = resps[0].payload[0]
        self.assertEqual(is_moving, 0)

    def test_joint_move_command(self) -> None:
        '''
            Verifies CMD_MOVE_JOINT_STEPS enqueues pose.

            :exceptions: None.
        '''
        payload = pack('<iiiiIH', -971, 3886, 8000, -729, 10000, 100)
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS, seq_num=6, payload=payload, crc16=0
        )
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 1)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        acked_id, q_count = unpack('<BB', resps[0].payload[:2])
        self.assertEqual(acked_id, int(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertEqual(q_count, 15)
        self.assertGreater(self.emu.get_simulation_state().queue_depth, 0)

    def test_jog_command(self) -> None:
        '''
            Verifies CMD_JOG_JOINT moves robot and returns ACK and MOVE_EVENT.

            :exceptions: None.
        '''
        payload: bytes = pack('<BiI', 0, 15, 2000)
        frame = BinaryFrame(msg_id=MessageId.CMD_JOG_JOINT, seq_num=15, payload=payload, crc16=0)
        resps: list[BinaryFrame] = self.processor.process_frame(frame=frame)
        self.assertEqual(len(resps), 2)
        self.assertEqual(resps[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(resps[1].msg_id, MessageId.RESP_MOVE_EVENT)
        self.assertGreater(self.emu.get_simulation_state().queue_depth, 0)

    def test_tool_command(self) -> None:
        '''
            Verifies tool pump/valve commands.

            :exceptions: None.
        '''
        frame_pump = BinaryFrame(
            msg_id=MessageId.CMD_TOOL_PUMP, seq_num=7, payload=b'\x00\x01', crc16=0
        )
        resps_pump = self.processor.process_frame(frame=frame_pump)
        self.assertEqual(resps_pump[0].msg_id, MessageId.RESP_ACK)
        frame_valve = BinaryFrame(
            msg_id=MessageId.CMD_TOOL_VALVE, seq_num=8, payload=b'\x01\x00', crc16=0
        )
        resps_valve = self.processor.process_frame(frame=frame_valve)
        self.assertEqual(resps_valve[0].msg_id, MessageId.RESP_ACK)

    def test_stop_and_reset_fault(self) -> None:
        '''
            Verifies estop and clear fault commands.

            :exceptions: None.
        '''
        frame_stop = BinaryFrame(msg_id=MessageId.CMD_ESTOP, seq_num=9, payload=b'', crc16=0)
        resps_stop: list[BinaryFrame] = self.processor.process_frame(frame=frame_stop)
        self.assertEqual(resps_stop[0].msg_id, MessageId.RESP_ACK)
        self.assertTrue(self.emu.get_telemetry().estop_active)

        frame_reset = BinaryFrame(
            msg_id=MessageId.CMD_CLEAR_FAULT, seq_num=10, payload=b'', crc16=0
        )
        resps_reset: list[BinaryFrame] = self.processor.process_frame(frame=frame_reset)
        self.assertEqual(resps_reset[0].msg_id, MessageId.RESP_ACK)
        self.assertFalse(self.emu.get_telemetry().estop_active)

    def test_version(self) -> None:
        '''
            Verifies get_version returns string.

            :exceptions: None.
        '''
        self.assertIsInstance(self.processor.get_version(), str)


if __name__ == '__main__':
    unittest_main()
