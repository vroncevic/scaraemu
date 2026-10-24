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
    Hardware serial response handler parsing inbound binary frames and diagnostic logs.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.connection.handler.dependencies import HandlerDependencies
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseHandler:
    '''
        Hardware serial response handler parsing inbound binary frames and diagnostic logs.

        It defines:

            :attributes:
                | _listener - Hardware bridge status and telemetry synchronizer.
                | _log_listener - Logging sink for hardware communications.
                | _streamer - Outbound trajectory queue streamer and flow controller.
                | _codec - Binary wire frame parser and stream decoder.
                | _kinematics - Kinematics solver for joint step to pose transformations.
                | _response_decoder - Binary wire response payload unpacker adapter.
            :methods:
                | __init__ - Initializes response handler with injected dependencies bundle.
                | on_bytes - Processes received raw bytes and updates telemetry.
                | on_log - Processes transport diagnostic message.
                | get_version - Returns response handler component version.
    '''

    _listener: IBridgeSynchronizer
    _log_listener: ILogListener
    _streamer: IQueueStreamer
    _codec: IBinaryFrameCodecAdapter
    _kinematics: IManipulatorKinematics
    _response_decoder: IBinaryResponseDecoderAdapter

    def __init__(
        self,
        dependencies: HandlerDependencies,
    ) -> None:
        '''
            Initializes response handler with injected dependencies bundle.

            :param dependencies: Encapsulated response handler dependencies.
            :exceptions: None.
        '''
        self._listener: Final[IBridgeSynchronizer] = dependencies.listener
        self._log_listener: Final[ILogListener] = dependencies.log_listener
        self._streamer: Final[IQueueStreamer] = dependencies.streamer
        self._codec: Final[IBinaryFrameCodecAdapter] = dependencies.codec
        self._kinematics: Final[IManipulatorKinematics] = dependencies.kinematics
        self._response_decoder: Final[IBinaryResponseDecoderAdapter] = (
            dependencies.response_decoder
        )

    def on_bytes(self, data: bytes) -> None:
        '''
            Processes received binary stream bytes and updates telemetry.

            :param data: Inbound wire bytes.
            :exceptions: None.
        '''
        frames: tuple[BinaryFrame, ...] = self._codec.feed_bytes(data)

        for frame in frames:
            match frame.msg_id:
                case MessageId.RESP_ACK:
                    acked_id, free_slots = self._response_decoder.unpack_ack(frame.payload)
                    self._log_listener.append_log(
                        f'RX < RESP_ACK msg={acked_id} free={free_slots}', 'rx'
                    )
                    self._streamer.process_ack(free_slots)

                case MessageId.RESP_NACK:
                    rej_id, err_code = self._response_decoder.unpack_nack(frame.payload)
                    self._log_listener.append_log(
                        f'RX < RESP_NACK msg={rej_id} err={err_code}', 'err'
                    )

                case MessageId.RESP_STATUS:
                    step_coords: ScaraStepCoords = (
                        self._response_decoder.unpack_status_steps(frame.payload)
                    )
                    joints: ScaraJoints = self._kinematics.steps_to_joints(step_coords)
                    pose: ScaraPose = self._kinematics.solve_fk(joints)
                    self._listener.on_telemetry(pose)
                    self._log_listener.append_log(
                        f'RX < RESP_STATUS pos=({pose.x:.2f}, {pose.y:.2f}, {pose.z:.2f})',
                        'rx',
                    )

                case MessageId.RESP_MOVE_EVENT:
                    self._log_listener.append_log(
                        f'RX < RESP_MOVE_EVENT seq={frame.seq_num}', 'rx'
                    )

                case _:
                    self._log_listener.append_log(
                        f'RX < {frame.msg_id.name} seq={frame.seq_num}', 'rx'
                    )

    def on_log(self, message: str) -> None:
        '''
            Processes transport diagnostic message.

            :param message: Log message string.
            :exceptions: None.
        '''
        tag: str = 'err' if message.startswith('[ERR]') else 'host'
        log_msg: str = (
            message
            if message.startswith(('[HOST]:', '[ERR]:'))
            else f'[HOST]: {message}'
        )
        self._log_listener.append_log(log_msg, tag)

    def get_version(self) -> str:
        '''
            Returns response handler component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
