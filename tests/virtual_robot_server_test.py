# -*- coding: UTF-8 -*-

'''
Module
    virtual_robot_server_test.py
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
    Unit tests for VirtualRobotServer digital twin controller.
'''

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket as Socket
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.service.emulator_service import EmulatorService
from scaraemu.core.service.kinematics_service import KinematicsService
from scaraemu.infrastructure.communication.transport.virtual_robot_server import VirtualRobotServer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVirtualRobotServer(TestCase):
    '''
        Test cases verifying VirtualRobotServer TCP streaming server.

        It defines:

            :methods:
                | setUp - Prepares emulator and server fixtures.
                | tearDown - Stops running server instance.
                | test_start_stop_lifecycle - Verifies starting and stopping server.
                | test_client_command_and_motion_flow - Verifies bidirectional command and motion streaming.
    '''

    def setUp(self) -> None:
        '''
            Prepares emulator and server fixtures.
        '''
        geom = ScaraGeometry(l1=150.0, l2=120.0)
        kin = KinematicsService(geometry=geom)
        self.emu = EmulatorService(kinematics=kin, initial_pose=ScaraPose(x=180.0, y=0.0, z=20.0))
        self.server = VirtualRobotServer(emulator=self.emu)

    def tearDown(self) -> None:
        '''
            Stops running server instance.
        '''
        self.server.stop()

    def test_start_stop_lifecycle(self) -> None:
        '''
            Verifies starting and stopping server.
        '''
        success = self.server.start(host='127.0.0.1', port=0)
        self.assertTrue(success)
        self.assertTrue(self.server.is_running())
        self.assertGreater(self.server.get_port(), 0)
        self.server.stop()
        self.assertFalse(self.server.is_running())

    def test_client_command_and_motion_flow(self) -> None:
        '''
            Verifies bidirectional command and motion streaming.
        '''
        self.server.start(host='127.0.0.1', port=0)
        port = self.server.get_port()

        client = Socket(AF_INET, SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.settimeout(2.0)

        # 1. Enable motors
        client.sendall(b'<CMD:ENABLE>\n')
        resp1 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:ACK#MOTORS_ENABLED>', resp1)

        # 2. Homing
        client.sendall(b'<CMD:HOME>\n')
        resp2 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:HOMED_SUCCESS#RIGHT>', resp2)

        # 3. Stream point move
        client.sendall(b'<pt#150.00#50.00#20.00#0.0#end>\n')
        resp3 = client.recv(1024).decode('utf-8')
        if 'MOVE_DONE' not in resp3:
            resp3 += client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:ACK#QUEUE=1>', resp3)
        self.assertIn('<RESP:MOVE_DONE#150.00#50.00#20.00#0.00>', resp3)

        # 4. Pump and wait commands
        client.sendall(b'<CMD:PUMP#1>\n')
        resp4 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:ACK#PUMP_ON>', resp4)

        client.sendall(b'<CMD:WAIT#50>\n')
        resp5 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:ACK#WAIT_DONE#50>', resp5)

        # 5. Manual JOG command
        client.sendall(b'<CMD:JOG#X#25.0>\n')
        resp6 = client.recv(1024).decode('utf-8')
        if 'MOVE_DONE' not in resp6:
            resp6 += client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:ACK#JOG_QUEUED', resp6)
        self.assertIn('<RESP:MOVE_DONE#', resp6)
        self.assertGreater(self.emu.get_simulation_state().queue_depth, 0)

        # 6. Status and GetPos query
        client.sendall(b'<CMD:STATUS>\n')
        resp7 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:STATUS#STATE=IDLE', resp7)

        client.sendall(b'<CMD:GETPOS>\n')
        resp8 = client.recv(1024).decode('utf-8')
        self.assertIn('<RESP:POS#', resp8)

        client.close()


if __name__ == '__main__':
    unittest_main()
