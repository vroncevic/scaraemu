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
    Unit tests for SystemHandler.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.service import EmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler
from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies
from scaraemu.infrastructure.server.handler.system.handler import SystemHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSystemHandler(TestCase):
    '''
        Unit test cases verifying SystemHandler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures and dependencies.
                | test_structural_typing - Verifies SystemHandler satisfies IBinaryCommandHandler.
                | test_can_handle - Verifies can_handle accepts system message IDs.
                | test_ping_command - Verifies ping command generates ACK.
                | test_home_command - Verifies home command enqueues home waypoint.
                | test_enable_disable_commands - Verifies enable/disable commands update state.
                | test_estop_and_clear_fault - Verifies estop clears queue and sets fault.
                | test_version - Verifies get_version returns string.
                | test_unhandled_frame - Verifies unhandled message ID returns empty list.
    '''

    emu: EmulationService
    queue: IEmulationQueue
    handler: SystemHandler

    def setUp(self) -> None:
        '''
            Prepares test fixtures and dependencies.

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
        emu_provides = EmulationFactory.create(dependencies=emu_deps)
        self.emu = emu_provides.service
        self.queue = emu_provides.queue
        response_builder: IBinaryResponseBuilderAdapter = (
            BinaryResponseBuilderAdapterFactory.create()
        )
        dependencies = SystemHandlerDependencies(
            emulation_controller=emu_provides.controller,
            emulation_queue=emu_provides.queue,
            response_builder=response_builder,
            home_pose=initial_pose,
        )
        self.handler = SystemHandler(dependencies=dependencies)

    def test_structural_typing(self) -> None:
        '''
            Verifies SystemHandler satisfies IBinaryCommandHandler structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler, IBinaryCommandHandler)

    def test_can_handle(self) -> None:
        '''
            Verifies can_handle accepts system message IDs and rejects others.

            :exceptions: None.
        '''
        self.assertTrue(self.handler.can_handle(MessageId.CMD_PING))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_HOME))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_ENABLE))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_DISABLE))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_ESTOP))
        self.assertTrue(self.handler.can_handle(MessageId.CMD_CLEAR_FAULT))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertFalse(self.handler.can_handle(MessageId.CMD_GET_STATUS))

    def test_ping_command(self) -> None:
        '''
            Verifies ping command generates ACK.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_PING, seq_num=1, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_ACK)

    def test_home_command(self) -> None:
        '''
            Verifies home command enqueues home waypoint and returns ACK.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_HOME, seq_num=2, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].msg_id, MessageId.RESP_ACK)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 1)

    def test_enable_disable_commands(self) -> None:
        '''
            Verifies enable and disable commands update motor state.

            :exceptions: None.
        '''
        frame_en = BinaryFrame(msg_id=MessageId.CMD_ENABLE, seq_num=3, payload=b'', crc16=0)
        res = self.handler.handle(frame_en)
        self.assertEqual(len(res), 1)
        self.assertTrue(self.emu.get_telemetry().motors_enabled)

        frame_dis = BinaryFrame(msg_id=MessageId.CMD_DISABLE, seq_num=4, payload=b'', crc16=0)
        res_dis = self.handler.handle(frame_dis)
        self.assertEqual(len(res_dis), 1)
        self.assertFalse(self.emu.get_telemetry().motors_enabled)

    def test_estop_and_clear_fault(self) -> None:
        '''
            Verifies estop clears queue and sets fault, clear fault clears it.

            :exceptions: None.
        '''
        self.queue.enqueue_waypoint(ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0))
        frame_estop = BinaryFrame(msg_id=MessageId.CMD_ESTOP, seq_num=5, payload=b'', crc16=0)
        self.handler.handle(frame_estop)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 0)
        self.assertTrue(self.emu.get_telemetry().estop_active)

        frame_clear = BinaryFrame(msg_id=MessageId.CMD_CLEAR_FAULT, seq_num=6, payload=b'', crc16=0)
        self.handler.handle(frame_clear)
        self.assertFalse(self.emu.get_telemetry().estop_active)

    def test_version(self) -> None:
        '''
            Verifies get_version returns string.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler.get_version(), str)

    def test_unhandled_frame(self) -> None:
        '''
            Verifies wildcard branch returns empty list for unhandled message ID.

            :exceptions: None.
        '''
        frame = BinaryFrame(msg_id=MessageId.CMD_TOOL_PUMP, seq_num=99, payload=b'', crc16=0)
        res = self.handler.handle(frame)
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest_main()
