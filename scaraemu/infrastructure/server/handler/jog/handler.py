# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Handler for binary manual joint and Cartesian jog commands.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.server.handler.jog.dependencies import JogHandlerDependencies
from scaraemu.infrastructure.server.pose.iholder import IVirtualPlannedPoseHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogHandler:
    '''
        Processes manual joint and Cartesian jog binary frames.

        It defines:

            :attributes:
                | _emulation_service - Injected emulation twin and telemetry service.
                | _emulation_queue - Injected emulation waypoint queue port.
                | _pose_holder - Injected planned pose state holder.
                | _kinematics - Injected manipulator kinematics solver.
                | _response_builder - Injected binary frame builder for wire responses.
                | _decoder - Injected binary payload decoder adapter.
            :methods:
                | __init__ - Initializes jog binary handler with collaborators bundle.
                | can_handle - Checks whether message ID is a jog command.
                | handle - Executes jog command and returns response frames.
                | get_version - Returns handler component version string.
    '''

    _emulation_service: IEmulationService
    _emulation_queue: IEmulationQueue
    _pose_holder: IVirtualPlannedPoseHolder
    _kinematics: IManipulatorKinematics
    _response_builder: IBinaryResponseBuilderAdapter
    _decoder: IBinaryPayloadDecoderAdapter

    def __init__(
        self,
        *,
        dependencies: JogHandlerDependencies,
    ) -> None:
        '''
            Initializes jog binary handler with collaborators bundle.

            :param dependencies: Injected JogHandlerDependencies instance.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = dependencies.emulation_service
        self._emulation_queue: Final[IEmulationQueue] = dependencies.emulation_queue
        self._pose_holder: Final[IVirtualPlannedPoseHolder] = dependencies.pose_holder
        self._kinematics: Final[IManipulatorKinematics] = dependencies.kinematics
        self._response_builder: Final[IBinaryResponseBuilderAdapter] = dependencies.response_builder
        self._decoder: Final[IBinaryPayloadDecoderAdapter] = dependencies.decoder

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Checks whether message ID is a jog command.

            :param msg_id: Binary protocol MessageId enum value.
            :return: True if message ID is handled, False otherwise.
            :exceptions: None.
        '''
        return msg_id == MessageId.CMD_JOG_JOINT

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Executes jog command and returns response frames.

            :param frame: Inbound BinaryFrame instance.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''
        if len(frame.payload) < 5:
            return [self._response_builder.build_nack(
                cmd_id=frame.msg_id, seq_num=frame.seq_num, error_code=1
            )]

        joint_id, step = self._decoder.unpack_jog_joint(frame.payload)

        current_pose: ScaraPose = self._emulation_service.get_telemetry().pose
        queue_depth: int = self._emulation_queue.get_snapshot(current_pose).queue_depth
        base: ScaraPose = self._pose_holder.get_base_pose(queue_depth, current_pose)

        new_x: float = base.x
        new_y: float = base.y
        new_z: float = base.z
        new_phi: float = base.phi

        match joint_id:
            case 0:
                new_x += float(step)
            case 1:
                new_y += float(step)
            case 2:
                new_z += float(step)
            case 3:
                new_phi += float(step)
            case _:
                return [self._response_builder.build_nack(
                    cmd_id=frame.msg_id, seq_num=frame.seq_num, error_code=1
                )]

        target: ScaraPose = ScaraPose(x=new_x, y=new_y, z=new_z, phi=new_phi)
        joints_left: ScaraJoints = self._kinematics.solve_ik(target, True)
        joints_right: ScaraJoints = self._kinematics.solve_ik(target, False)

        if not joints_left.reachable and not joints_right.reachable:
            return [self._response_builder.build_nack(
                cmd_id=frame.msg_id, seq_num=frame.seq_num, error_code=2
            )]

        self._emulation_queue.enqueue_waypoint(target)
        self._pose_holder.set_planned_pose(target)

        free_slots: int = max(0, 16 - self._emulation_queue.get_snapshot(current_pose).queue_depth)
        ack_frame: BinaryFrame = self._response_builder.build_ack(
            cmd_id=MessageId.CMD_JOG_JOINT, seq_num=frame.seq_num, free_slots=free_slots
        )
        move_frame: BinaryFrame = self._response_builder.build_move_event(
            seq_num=frame.seq_num, event_type=2
        )

        return [ack_frame, move_frame]

    def get_version(self) -> str:
        '''
            Returns handler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
