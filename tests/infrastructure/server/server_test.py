# -*- coding: UTF-8 -*-

'''
Module
    server_test.py
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
    Unit tests for VirtualManipulatorServer digital twin controller.
'''

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket as Socket
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

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
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.server.dependencies import ServerDependencies
from scaraemu.infrastructure.server.factory import ServerFactory
from scaraemu.infrastructure.server.iserver import IVirtualManipulatorServer
from scaraemu.infrastructure.server.provides import ServerProvides
from scaraemu.infrastructure.server.server import VirtualManipulatorServer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualManipulatorServer(TestCase):
    '''
        Test cases verifying VirtualManipulatorServer TCP streaming server.

        It defines:

            :methods:
                | setUp - Prepares domain services and server fixtures.
                | tearDown - Stops running server instance.
                | test_structural_typing - Verifies satisfies IVirtualManipulatorServer.
                | test_start_stop_lifecycle - Verifies starting and stopping server.
                | test_start_when_already_running - Verifies idempotent start.
                | test_start_bind_failure - Verifies start returns False on bind error.
                | test_start_bind_and_close_oserror - Verifies bind failure and close error.
                | test_stop_socket_close_oserror - Verifies stop handles OSError on close.
                | test_client_command_and_motion_flow - Verifies bidirectional command streaming.
    '''

    emu: EmulationService
    server: VirtualManipulatorServer

    def setUp(self) -> None:
        '''
            Prepares domain services and server fixtures.

            :exceptions: None.
        '''
        kin: IManipulatorKinematics = KinematicsAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds(),
            transmission=DefaultScaraProfile.create_transmission(),
        )
        initial_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        emu_deps = EmulationDependencies(
            kinematics=kin,
            initial_pose=initial_pose,
        )
        self.emu_provides = EmulationFactory.create(dependencies=emu_deps)
        self.emu = self.emu_provides.service

        deps = ServerDependencies(
            emulation_controller=self.emu_provides.controller,
            emulation_service=self.emu_provides.service,
            emulation_queue=self.emu_provides.queue,
            motion_notifier=self.emu_provides.notifier,
            home_pose=initial_pose,
            kinematics=kin,
            motion_validator=MotionValidatorAdapterFactory.create(
                bounds=DefaultScaraProfile.create_bounds()
            ),
            response_builder=BinaryResponseBuilderAdapterFactory.create(),
            codec=BinaryFrameCodecAdapterFactory.create(),
            decoder=BinaryPayloadDecoderAdapterFactory.create(),
        )
        provides: ServerProvides = ServerFactory.create(dependencies=deps)
        self.server = provides.server

    def tearDown(self) -> None:
        '''
            Stops running server instance.

            :exceptions: None.
        '''
        self.server.stop()

    def test_structural_typing(self) -> None:
        '''
            Verifies VirtualManipulatorServer satisfies IVirtualManipulatorServer structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.server, IVirtualManipulatorServer)

    def test_start_stop_lifecycle(self) -> None:
        '''
            Verifies starting and stopping server.

            :exceptions: None.
        '''
        success: bool = self.server.start(host='127.0.0.1', port=0)
        self.assertTrue(success)
        self.assertTrue(self.server.is_running())
        self.assertGreater(len(self.server.get_version()), 0)
        self.server.stop()
        self.assertFalse(self.server.is_running())

    def test_start_when_already_running(self) -> None:
        '''
            Verifies start returns True immediately when server is already active.

            :exceptions: None.
        '''
        self.server.start(host='127.0.0.1', port=0)
        self.assertTrue(self.server.start(host='127.0.0.1', port=0))

    def test_start_bind_failure(self) -> None:
        '''
            Verifies start returns False when binding fails with OSError.

            :exceptions: None.
        '''
        self.assertFalse(self.server.start(host='999.999.999.999', port=99999))

    def test_start_bind_and_close_oserror(self) -> None:
        '''
            Verifies start handles OSError during both bind and socket close.

            :exceptions: None.
        '''
        mock_socket = MagicMock()
        mock_socket.bind.side_effect = OSError('bind failed')
        mock_socket.close.side_effect = OSError('close failed')

        with patch('scaraemu.infrastructure.server.server.Socket', return_value=mock_socket):
            self.assertFalse(self.server.start(host='127.0.0.1', port=8888))

    def test_stop_socket_close_oserror(self) -> None:
        '''
            Verifies stop handles OSError when closing server socket.

            :exceptions: None.
        '''
        mock_socket = MagicMock()
        mock_socket.close.side_effect = OSError('close failed')
        mock_socket.accept.side_effect = OSError('closed')
        mock_socket.getsockname.return_value = ('127.0.0.1', 8888)

        with patch('scaraemu.infrastructure.server.server.Socket', return_value=mock_socket):
            self.server.start(host='127.0.0.1', port=8888)

        self.server.stop()
        self.assertFalse(self.server.is_running())

    def test_client_command_and_motion_flow(self) -> None:
        '''
            Verifies bidirectional command and motion streaming.

            :exceptions: None.
        '''
        sock: Socket = Socket(AF_INET, SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        port: int = sock.getsockname()[1]
        sock.close()

        self.server.start(host='127.0.0.1', port=port)

        client: Socket = Socket(AF_INET, SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.settimeout(2.0)

        codec: IBinaryFrameCodecAdapter = (
            BinaryFrameCodecAdapterFactory.create()
        )

        frame1 = BinaryFrame(
            msg_id=MessageId.CMD_ENABLE, seq_num=1, payload=b'', crc16=0
        )
        client.sendall(codec.pack_frame(frame1))
        resp1_bytes: bytes = client.recv(1024)
        resp1_frames = codec.feed_bytes(resp1_bytes)
        self.assertTrue(
            any(f.msg_id == MessageId.RESP_ACK for f in resp1_frames)
        )

        frame2 = BinaryFrame(
            msg_id=MessageId.CMD_HOME, seq_num=2, payload=b'', crc16=0
        )
        client.sendall(codec.pack_frame(frame2))
        resp2_bytes: bytes = client.recv(1024)
        resp2_frames = codec.feed_bytes(resp2_bytes)
        self.assertTrue(
            any(
                f.msg_id in (MessageId.RESP_ACK, MessageId.RESP_HOMING_EVENT)
                for f in resp2_frames
            )
        )

        frame3 = BinaryFrame(
            msg_id=MessageId.CMD_PING, seq_num=3, payload=b'', crc16=0
        )
        client.sendall(codec.pack_frame(frame3))
        resp3_bytes: bytes = client.recv(1024)
        resp3_frames = codec.feed_bytes(resp3_bytes)
        self.assertTrue(
            any(f.msg_id == MessageId.RESP_ACK for f in resp3_frames)
        )

        frame4 = BinaryFrame(
            msg_id=MessageId.CMD_GET_STATUS, seq_num=4, payload=b'', crc16=0
        )
        client.sendall(codec.pack_frame(frame4))
        resp4_bytes: bytes = client.recv(1024)
        resp4_frames = codec.feed_bytes(resp4_bytes)
        self.assertTrue(
            any(f.msg_id == MessageId.RESP_STATUS for f in resp4_frames)
        )

        frame5 = BinaryFrame(
            msg_id=MessageId.CMD_CLEAR_FAULT, seq_num=5, payload=b'', crc16=0
        )
        client.sendall(codec.pack_frame(frame5))
        resp5_bytes: bytes = client.recv(1024)
        resp5_frames = codec.feed_bytes(resp5_bytes)
        self.assertTrue(
            any(f.msg_id == MessageId.RESP_ACK for f in resp5_frames)
        )

        client.close()


if __name__ == '__main__':
    unittest_main()
