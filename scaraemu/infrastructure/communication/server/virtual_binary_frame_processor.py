# -*- coding: UTF-8 -*-

'''
Module
    virtual_binary_frame_processor.py
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
    Binary protocol frame processor executing wire commands and generating responses.
'''

from __future__ import annotations

from struct import pack
from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker
from scaraemu.core.model.kinematics.scara_joints import ScaraJoints
from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.core.model.kinematics.scara_step_coords import ScaraStepCoords
from scaraemu.core.service.kinematics.kinematics_service import KinematicsService
from scaraemu.core.service.simulation.iemulator_service import IEmulatorService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualBinaryFrameProcessor:
    '''
        Dispatches inbound binary protocol frames to emulator service and formats responses.

        It defines:

            :attributes:
                | _emulator - Injected emulator core service.
                | _kinematics - Injected kinematic solver for FK and step conversions.
                | _builder - Injected binary frame builder for wire responses.
            :methods:
                | __init__ - Initializes processor with emulator and collaborators.
                | reset - Clears processor state caches.
                | process_frame - Dispatches inbound binary frame to appropriate handler.
    '''

    _emulator: Final[IEmulatorService]
    _kinematics: Final[KinematicsService]
    _builder: Final[BinaryFrameBuilder]

    def __init__(
        self,
        *,
        emulator: IEmulatorService,
        kinematics: KinematicsService | None = None,
        frame_builder: BinaryFrameBuilder | None = None,
    ) -> None:
        '''
            Initializes processor with injected dependencies.

            :param emulator: SCARA emulator core service instance.
            :param kinematics: Optional KinematicsService instance.
            :param frame_builder: Optional BinaryFrameBuilder instance.
            :exceptions: None.
        '''
        self._emulator = emulator
        self._kinematics = kinematics if kinematics is not None else KinematicsService()
        self._builder = (
            frame_builder if frame_builder is not None
            else BinaryFrameBuilderFactory.create()
        )

    def reset(self) -> None:
        '''
            Clears internal state caches.

            :exceptions: None.
        '''
        pass

    def process_frame(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Dispatches inbound binary frame to appropriate handler.

            :param frame: Decoded BinaryFrame from client.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''
        match frame.msg_id:
            case MessageId.CMD_PING:
                return self._handle_ping(frame=frame)
            case MessageId.CMD_HOME:
                return self._handle_home(frame=frame)
            case MessageId.CMD_ENABLE:
                return self._handle_enable(frame=frame)
            case MessageId.CMD_DISABLE:
                return self._handle_disable(frame=frame)
            case MessageId.CMD_ESTOP:
                return self._handle_stop(frame=frame)
            case MessageId.CMD_CLEAR_FAULT:
                return self._handle_reset_fault(frame=frame)
            case MessageId.CMD_GET_STATUS:
                return self._handle_status(frame=frame)
            case MessageId.CMD_MOVE_JOINT_STEPS:
                return self._handle_joint_move(frame=frame)
            case MessageId.CMD_TOOL_PUMP | MessageId.CMD_TOOL_VALVE:
                return self._handle_tool(frame=frame)
            case _:
                return self._handle_unknown(frame=frame)

    def _handle_ping(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_PING), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_home(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        home_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        self._emulator.set_target_pose(home_pose, direct=True)
        payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_HOME), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_enable(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        self._emulator.set_motors_enabled(True)
        payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_ENABLE), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_disable(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        self._emulator.set_motors_enabled(False)
        payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_DISABLE), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_stop(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        self._emulator.clear_queue()
        self._emulator.set_estop(True)
        payload = pack(BinaryStructFormat.ACK, int(frame.msg_id), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_reset_fault(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        self._emulator.set_estop(False)
        payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_CLEAR_FAULT), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=payload)]

    def _handle_status(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        pose: ScaraPose = self._emulator.get_current_pose()
        joints: ScaraJoints = self._kinematics.solve_ik(pose=pose)
        step_coords: ScaraStepCoords = self._kinematics.joints_to_steps(joints=joints)
        payload = pack(
            BinaryStructFormat.STATUS,
            1,
            0,
            0,
            step_coords.j1_steps,
            step_coords.j2_steps,
            step_coords.z_steps,
            step_coords.j4_steps,
        )
        return [self._builder.build_frame(msg_id=MessageId.RESP_STATUS, seq_num=frame.seq_num, payload=payload)]

    def _handle_joint_move(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        steps: JointSteps = BinaryPayloadUnpacker.unpack_joint_steps(frame.payload)
        step_coords = ScaraStepCoords(
            j1_steps=steps.target_j1_steps,
            j2_steps=steps.target_j2_steps,
            z_steps=steps.target_z_steps,
            j4_steps=steps.target_j4_steps,
        )
        joints: ScaraJoints = self._kinematics.steps_to_joints(steps=step_coords)
        pose: ScaraPose = self._kinematics.solve_fk(joints=joints)
        self._emulator.enqueue_trajectory([pose])

        ack_payload = pack(BinaryStructFormat.ACK, int(MessageId.CMD_MOVE_JOINT_STEPS), 1)
        ack_frame = self._builder.build_frame(
            msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=ack_payload
        )
        move_payload = pack(BinaryStructFormat.MOVE_EVENT, 2, frame.seq_num)
        move_frame = self._builder.build_frame(
            msg_id=MessageId.RESP_MOVE_EVENT, seq_num=frame.seq_num, payload=move_payload
        )
        return [ack_frame, move_frame]

    def _handle_tool(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        BinaryPayloadUnpacker.unpack_tool_cmd(frame.payload)
        ack_payload = pack(BinaryStructFormat.ACK, int(frame.msg_id), 0)
        return [self._builder.build_frame(msg_id=MessageId.RESP_ACK, seq_num=frame.seq_num, payload=ack_payload)]

    def _handle_unknown(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        nack_payload = pack(BinaryStructFormat.NACK, int(frame.msg_id), 1)
        return [self._builder.build_frame(msg_id=MessageId.RESP_NACK, seq_num=frame.seq_num, payload=nack_payload)]
