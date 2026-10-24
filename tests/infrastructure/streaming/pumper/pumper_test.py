# -*- coding: UTF-8 -*-

'''
Module
    pumper_test.py
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
    Unit tests for QueuePumper.
'''

from __future__ import annotations

from collections import deque
from unittest import TestCase, main as unittest_main

from scaracom.flow.pacing.window import FlowWindow

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.streaming.pumper.dependencies import PumperDependencies
from scaraemu.infrastructure.streaming.pumper.pumper import QueuePumper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockPumperTransport:
    '''
        Mock transport for testing packet pumping operations.
    '''

    def __init__(self, connected: bool = True) -> None:
        '''Initializes mock transport for pumper.'''
        self.connected = connected
        self.written_frames: list[bytes] = []

    def is_connected(self) -> bool:
        '''Checks pumper transport connection.'''
        return self.connected

    def write_bytes(self, data: bytes) -> bool:
        '''Writes raw frame bytes for pumper.'''
        self.written_frames.append(data)
        return True


class _MockPumperLogListener:
    '''
        Mock listener capturing diagnostic log messages for pumper.
    '''

    def __init__(self) -> None:
        '''Initializes mock log listener for pumper.'''
        self.log_entries: list[tuple[str, str]] = []

    def append_log(self, message: str, tag: str) -> None:
        '''Appends log entry for pumper.'''
        self.log_entries.append((message, tag))

    def get_version(self) -> str:
        '''Returns mock listener version.'''
        return '1.0.2'


class _MockPumperKinematics:
    '''
        Mock kinematics calculation adapter for packet pumper verification.
    '''

    def solve_ik(self, pose: ScaraPose, elbow_left: bool = True) -> ScaraJoints:
        '''Solves inverse kinematics for pumper.'''
        _ = elbow_left
        return ScaraJoints(
            theta1=15.0, theta2=25.0, z=pose.z, theta4=pose.phi, reachable=True
        )

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''Solves forward kinematics for pumper.'''
        return ScaraPose(x=15.0, y=25.0, z=joints.z, phi=joints.theta4)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''Converts joint angles to motor step coordinates.'''
        return ScaraStepCoords(
            j1_steps=150, j2_steps=250, z_steps=int(joints.z * 10), j4_steps=0
        )

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''Converts motor step coordinates back to joint angles.'''
        return ScaraJoints(
            theta1=15.0, theta2=25.0, z=steps.z_steps / 10.0, theta4=0.0, reachable=True
        )


class TestQueuePumper(TestCase):
    '''
        Unit tests for QueuePumper.

        It defines:

            :methods:
                | test_pump_when_connected - Tests pumping packets across connected transport within flow slots.
                | test_pump_when_disconnected - Tests that pumping does not transmit when transport is disconnected.
    '''

    def test_pump_when_connected(self) -> None:
        '''
            Tests pumping packets across connected transport within flow slots.

            :exceptions: None.
        '''
        transport = _MockPumperTransport(connected=True)
        log_listener = _MockPumperLogListener()
        window = FlowWindow(max_in_flight=2)
        kinematics = _MockPumperKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumper(dependencies=deps)

        self.assertEqual(pumper.get_version(), '1.0.2')

        queue = deque([
            ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0),
            ScaraPose(x=15.0, y=25.0, z=5.0, phi=0.0),
            ScaraPose(x=20.0, y=30.0, z=5.0, phi=0.0),
        ])

        pumper.pump(queue)
        self.assertEqual(len(transport.written_frames), 2)
        self.assertEqual(len(queue), 1)

    def test_pump_when_disconnected(self) -> None:
        '''
            Tests that pumping does not transmit when transport is disconnected.

            :exceptions: None.
        '''
        transport = _MockPumperTransport(connected=False)
        log_listener = _MockPumperLogListener()
        window = FlowWindow(max_in_flight=2)
        kinematics = _MockPumperKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumper(dependencies=deps)

        queue = deque([ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)])
        pumper.pump(queue)
        self.assertEqual(len(transport.written_frames), 0)
        self.assertEqual(len(queue), 1)


if __name__ == '__main__':
    unittest_main()
