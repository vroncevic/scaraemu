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
    Unit tests for ResponseHandler.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.connection.handler.dependencies import HandlerDependencies
from scaraemu.infrastructure.connection.handler.handler import ResponseHandler
from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.response.factory import BinaryResponseDecoderAdapterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockBridgeListener:
    '''
        Mock listener capturing telemetry and elbow events.
    '''

    def __init__(self) -> None:
        '''Initializes mock bridge listener.'''
        self.telemetry_poses: list[ScaraPose] = []

    def on_state_change(self, connected: bool) -> None:
        '''Handles state change.'''
        _ = connected

    def on_telemetry(self, pose: ScaraPose) -> None:
        '''Handles telemetry pose.'''
        self.telemetry_poses.append(pose)

    def on_elbow_clearance(self, clearance: float) -> None:
        '''Handles elbow clearance.'''
        _ = clearance


class _MockLogListener:
    '''
        Mock log listener capturing dispatched communication entries.
    '''

    def __init__(self) -> None:
        '''Initializes mock log listener.'''
        self.logs: list[tuple[str, str]] = []

    def append_log(self, message: str, tag: str) -> None:
        '''Appends log message.'''
        self.logs.append((message, tag))

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockQueueStreamer:
    '''
        Mock queue streamer recording processed flow acknowledgments.
    '''

    def __init__(self) -> None:
        '''Initializes mock queue streamer.'''
        self.processed_acks: list[int] = []

    def process_ack(self, free_slots: int) -> None:
        '''Processes ack with free slots.'''
        self.processed_acks.append(free_slots)

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockKinematics:
    '''
        Mock kinematics solver transforming joint steps to dummy poses.
    '''

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''Transforms steps to joints.'''
        _ = steps
        return ScaraJoints(
            theta1=10.0, theta2=20.0, z=30.0, theta4=0.0, reachable=True
        )

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''Solves forward kinematics.'''
        _ = joints
        return ScaraPose(x=150.0, y=75.0, z=30.0, phi=0.0)


class TestResponseHandler(TestCase):
    '''
        Unit tests verifying ResponseHandler packet decoding and telemetry dispatching.

        It defines:

            :methods:
                | test_structural_protocol_conformity - Tests IResponseHandler conformity.
                | test_on_bytes_status_and_ack - Tests processing binary STATUS and ACK frames.
                | test_on_bytes_nack_and_events - Tests processing NACK, MOVE_EVENT, and unhandled frames.
                | test_on_log - Tests formatting and routing diagnostic log messages.
    '''

    def test_structural_protocol_conformity(self) -> None:
        '''
            Tests structural conformity to IResponseHandler.

            :exceptions: None.
        '''
        listener = _MockBridgeListener()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        kinematics = _MockKinematics()
        decoder = BinaryResponseDecoderAdapterFactory.create()

        bundle = HandlerDependencies(
            listener=listener,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
            kinematics=kinematics,
            response_decoder=decoder,
        )

        handler = ResponseHandler(dependencies=bundle)
        self.assertIsInstance(handler, IResponseHandler)
        self.assertEqual(handler.get_version(), '1.0.2')

    def test_on_bytes_status_and_ack(self) -> None:
        '''
            Tests processing binary STATUS and ACK frames.

            :exceptions: None.
        '''
        listener = _MockBridgeListener()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        kinematics = _MockKinematics()
        decoder = BinaryResponseDecoderAdapterFactory.create()
        builder = BinaryResponseBuilderAdapterFactory.create()

        bundle = HandlerDependencies(
            listener=listener,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
            kinematics=kinematics,
            response_decoder=decoder,
        )

        handler = ResponseHandler(dependencies=bundle)

        status_frame: BinaryFrame = builder.build_status(
            seq_num=1,
            step_coords=ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=50, j4_steps=0),
            is_moving=False,
        )
        wire_bytes: bytes = codec.pack_frame(status_frame)
        handler.on_bytes(wire_bytes)

        self.assertEqual(len(listener.telemetry_poses), 1)
        self.assertAlmostEqual(listener.telemetry_poses[0].x, 150.0)

        ack_frame: BinaryFrame = builder.build_ack(
            cmd_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=2,
            free_slots=12,
        )
        wire_ack: bytes = codec.pack_frame(ack_frame)
        handler.on_bytes(wire_ack)

        self.assertEqual(streamer.processed_acks, [12])

    def test_on_bytes_nack_and_events(self) -> None:
        '''
            Tests processing NACK, MOVE_EVENT, and unhandled frame types.

            :exceptions: None.
        '''
        listener = _MockBridgeListener()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        kinematics = _MockKinematics()
        decoder = BinaryResponseDecoderAdapterFactory.create()
        builder = BinaryResponseBuilderAdapterFactory.create()

        bundle = HandlerDependencies(
            listener=listener,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
            kinematics=kinematics,
            response_decoder=decoder,
        )

        handler = ResponseHandler(dependencies=bundle)

        nack_frame = builder.build_nack(
            cmd_id=MessageId.CMD_HOME,
            seq_num=3,
            error_code=1,
        )
        handler.on_bytes(codec.pack_frame(nack_frame))
        self.assertIn(('RX < RESP_NACK msg=6 err=1', 'err'), log_listener.logs)

        move_event = BinaryFrame(
            msg_id=MessageId.RESP_MOVE_EVENT,
            seq_num=4,
            payload=b'',
            crc16=0,
        )
        handler.on_bytes(codec.pack_frame(move_event))
        self.assertIn(('RX < RESP_MOVE_EVENT seq=4', 'rx'), log_listener.logs)

        other_frame = BinaryFrame(
            msg_id=MessageId.CMD_GET_STATUS,
            seq_num=5,
            payload=b'',
            crc16=0,
        )
        handler.on_bytes(codec.pack_frame(other_frame))
        self.assertIn(('RX < CMD_GET_STATUS seq=5', 'rx'), log_listener.logs)

    def test_on_log(self) -> None:
        '''
            Tests formatting and routing diagnostic log messages.

            :exceptions: None.
        '''
        listener = _MockBridgeListener()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        kinematics = _MockKinematics()
        decoder = BinaryResponseDecoderAdapterFactory.create()

        bundle = HandlerDependencies(
            listener=listener,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
            kinematics=kinematics,
            response_decoder=decoder,
        )

        handler = ResponseHandler(dependencies=bundle)

        handler.on_log('[HOST]: Test diagnostic message')
        self.assertEqual(
            log_listener.logs[-1], ('[HOST]: Test diagnostic message', 'host')
        )

        handler.on_log('[ERR]: Connection dropped')
        self.assertEqual(
            log_listener.logs[-1], ('[ERR]: Connection dropped', 'err')
        )


if __name__ == '__main__':
    unittest_main()
