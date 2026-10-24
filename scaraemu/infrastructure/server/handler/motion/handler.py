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
    Handler for binary status telemetry queries and joint step motion frames.
'''

from __future__ import annotations

from math import degrees
from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.server.handler.motion.dependencies import MotionHandlerDependencies
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.pose.iholder import IVirtualPlannedPoseHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionHandler:
    '''
        Processes status telemetry queries and joint step motion binary frames.

        It defines:

            :attributes:
                | _emulation_service - Injected emulation twin and telemetry service.
                | _emulation_queue - Injected emulation waypoint queue port.
                | _pose_holder - Injected planned pose state holder.
                | _kinematics - Injected kinematic solver for FK and step conversions.
                | _validator - Injected motion safety and dead zone validator adapter.
                | _response_builder - Injected binary frame builder for wire responses.
                | _decoder - Injected binary payload decoder adapter.
                | _log_listener - Injected server log listener for console diagnostics.
            :methods:
                | __init__ - Initializes motion binary handler with collaborators bundle.
                | can_handle - Checks whether message ID is a motion command.
                | handle - Executes motion command and returns response frames.
                | get_version - Returns handler component version string.
    '''

    _emulation_service: IEmulationService
    _emulation_queue: IEmulationQueue
    _pose_holder: IVirtualPlannedPoseHolder
    _kinematics: IManipulatorKinematics
    _validator: IMotionValidatorAdapter
    _response_builder: IBinaryResponseBuilderAdapter
    _decoder: IBinaryPayloadDecoderAdapter
    _log_listener: IServerLogListener

    def __init__(
        self,
        *,
        dependencies: MotionHandlerDependencies,
    ) -> None:
        '''
            Initializes motion binary handler with collaborators bundle.

            :param dependencies: Injected MotionHandlerDependencies instance.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = dependencies.emulation_service
        self._emulation_queue: Final[IEmulationQueue] = dependencies.emulation_queue
        self._pose_holder: Final[IVirtualPlannedPoseHolder] = dependencies.pose_holder
        self._kinematics: Final[IManipulatorKinematics] = dependencies.kinematics
        self._validator: Final[IMotionValidatorAdapter] = dependencies.validator
        self._response_builder: Final[IBinaryResponseBuilderAdapter] = dependencies.response_builder
        self._decoder: Final[IBinaryPayloadDecoderAdapter] = dependencies.decoder
        self._log_listener: Final[IServerLogListener] = dependencies.log_listener

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Checks whether message ID is a motion command.

            :param msg_id: Binary protocol MessageId enum value.
            :return: True if message ID is handled, False otherwise.
            :exceptions: None.
        '''
        return msg_id in (MessageId.CMD_GET_STATUS, MessageId.CMD_MOVE_JOINT_STEPS)

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Executes motion command and returns response frames.

            :param frame: Inbound BinaryFrame instance.
            :return: List of response BinaryFrame instances.
            :exceptions: None.
        '''
        match frame.msg_id:
            case MessageId.CMD_GET_STATUS:
                pose: ScaraPose = self._emulation_service.get_telemetry().pose
                joints: ScaraJoints = self._kinematics.solve_ik(pose, elbow_left=True)
                step_coords: ScaraStepCoords = self._kinematics.joints_to_steps(joints)

                return [self._response_builder.build_status(
                    seq_num=frame.seq_num,
                    step_coords=step_coords,
                    is_moving=self._emulation_service.get_simulation_state().is_animating,
                )]

            case MessageId.CMD_MOVE_JOINT_STEPS:
                steps: JointSteps = self._decoder.unpack_joint_steps(frame.payload)
                step_coords = ScaraStepCoords(
                    j1_steps=steps.target_j1_steps,
                    j2_steps=steps.target_j2_steps,
                    z_steps=steps.target_z_steps,
                    j4_steps=steps.target_j4_steps,
                )
                joints = self._kinematics.steps_to_joints(step_coords)
                target_pose = self._kinematics.solve_fk(joints)
                current_pose: ScaraPose = self._emulation_service.get_telemetry().pose
                snapshot = self._emulation_queue.get_snapshot(current_pose)
                queue_depth: int = snapshot.queue_depth
                base_pose: ScaraPose = self._pose_holder.get_base_pose(queue_depth, current_pose)

                if not self._validator.is_segment_valid(base_pose, target_pose):
                    self._log_listener.on_server_log(
                        f'❌ [DT-SERVER]: Motion rejected: segment '
                        f'({base_pose.x:.1f}, {base_pose.y:.1f}) -> '
                        f'({target_pose.x:.1f}, {target_pose.y:.1f}) '
                        f'invalid or crosses dead zone!'
                    )

                    return [self._response_builder.build_nack(
                        cmd_id=frame.msg_id, seq_num=frame.seq_num, error_code=2
                    )]

                if queue_depth == 0 and not snapshot.has_target:
                    self._emulation_service.clear_trail()

                self._emulation_queue.enqueue_waypoint(target_pose, seq_num=frame.seq_num)
                self._pose_holder.set_planned_pose(target_pose)

                updated_depth: int = self._emulation_queue.get_snapshot(current_pose).queue_depth
                self._log_listener.on_server_log(
                    f'📍 [DT-SERVER]: Waypoint enqueued: X={target_pose.x:.1f}, '
                    f'Y={target_pose.y:.1f}, Z={target_pose.z:.1f} '
                    f'(J1={degrees(joints.theta1):.1f}°, J2={degrees(joints.theta2):.1f}°) '
                    f'[Queue: {updated_depth}]'
                )

                free_slots: int = max(0, 16 - updated_depth)
                ack_frame: BinaryFrame = self._response_builder.build_ack(
                    cmd_id=MessageId.CMD_MOVE_JOINT_STEPS,
                    seq_num=frame.seq_num,
                    free_slots=free_slots,
                )

                return [ack_frame]

            case _:
                return []

    def get_version(self) -> str:
        '''
            Returns handler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
