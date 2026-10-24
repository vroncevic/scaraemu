# -*- coding: UTF-8 -*-

'''
Module
    pumper.py
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
    Dispatches queued motion packets across transport within flow window limits.
'''

from __future__ import annotations

from collections import deque
from typing import Final

from scaracom.flow.pacing.iwindow import IFlowWindow
from scaracom.transport.itransport import ITransport

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.protocol.imotion_builder import IBinaryMotionFrameBuilder
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.streaming.pumper.dependencies import PumperDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueuePumper:
    '''
        Dispatches queued motion packets across transport within flow window limits.

        It defines:

            :attributes:
                | _transport - Communication transport layer.
                | _log_listener - Logging sink for hardware communications.
                | _flow_window - Flow control window slot manager.
                | _kinematics - Forward and inverse kinematics solver.
                | _codec - Binary wire frame codec adapter.
                | _motion_builder - Injected binary motion frame builder.
                | _seq_num - Cyclic outbound packet sequence counter.
            :methods:
                | __init__ - Initializes queue pumper with dependency bundle.
                | pump - Dispatches pending poses within available flow window slots.
                | get_version - Returns queue pumper component version string.
    '''

    _transport: ITransport
    _log_listener: ILogListener
    _flow_window: IFlowWindow
    _kinematics: IManipulatorKinematics
    _codec: IBinaryFrameCodecAdapter
    _motion_builder: IBinaryMotionFrameBuilder
    _seq_num: int

    def __init__(self, dependencies: PumperDependencies) -> None:
        '''
            Initializes queue pumper with dependency bundle.

            :param dependencies: Encapsulated pumper dependency bundle.
            :exceptions: None.
        '''
        self._transport: Final[ITransport] = dependencies.transport
        self._log_listener: Final[ILogListener] = dependencies.log_listener
        self._flow_window: Final[IFlowWindow] = dependencies.flow_window
        self._kinematics: Final[IManipulatorKinematics] = dependencies.kinematics
        self._codec: Final[IBinaryFrameCodecAdapter] = dependencies.codec
        self._motion_builder: Final[IBinaryMotionFrameBuilder] = (
            BuilderFactory.create().motion
        )
        self._seq_num = 0

    def pump(self, queue: deque[ScaraPose]) -> None:
        '''
            Dispatches pending poses within available flow window slots.

            :param queue: Pending queue of ScaraPose instances.
            :exceptions: None.
        '''
        if not self._transport.is_connected():
            return

        while queue and self._flow_window.acquire_slot():
            pose: ScaraPose = queue.popleft()
            joints: ScaraJoints = self._kinematics.solve_ik(pose, elbow_left=True)
            steps: ScaraStepCoords = self._kinematics.joints_to_steps(joints)
            joint_steps: JointSteps = JointSteps(
                target_j1_steps=steps.j1_steps,
                target_j2_steps=steps.j2_steps,
                target_z_steps=steps.z_steps,
                target_j4_steps=steps.j4_steps,
                duration_us=100000,
                feedrate_scale=100,
            )
            frame: BinaryFrame = self._motion_builder.build_joint_move(
                seq_num=self._seq_num,
                steps=joint_steps,
            )
            wire_packet: bytes = self._codec.pack_frame(frame)
            self._transport.write_bytes(wire_packet)
            self._log_listener.append_log(
                f'TX > CMD_MOVE_JOINT_STEPS seq={self._seq_num} '
                f'[J1={steps.j1_steps} J2={steps.j2_steps} Z={steps.z_steps} J4={steps.j4_steps}]',
                'tx',
            )
            self._seq_num = (self._seq_num + 1) & 0xFF

    def get_version(self) -> str:
        '''
            Returns queue pumper component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
