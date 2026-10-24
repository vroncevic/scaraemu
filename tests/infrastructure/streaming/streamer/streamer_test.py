# -*- coding: UTF-8 -*-

'''
Module
    streamer_test.py
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
    Unit tests for QueueStreamer flow window manager.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaracom.flow.pacing.window import FlowWindow

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.streaming.pumper.dependencies import PumperDependencies
from scaraemu.infrastructure.streaming.pumper.factory import QueuePumperFactory
from scaraemu.infrastructure.streaming.streamer.dependencies import StreamerDependencies
from scaraemu.infrastructure.streaming.streamer.streamer import QueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockTransport:
    '''
        Mock transport for testing queue streaming.
    '''

    def __init__(self, connected: bool = True) -> None:
        '''Initializes mock transport.'''
        self.connected = connected
        self.written_packets: list[bytes] = []

    def is_connected(self) -> bool:
        '''Checks connection status.'''
        return self.connected

    def write_bytes(self, data: bytes) -> bool:
        '''Writes bytes.'''
        self.written_packets.append(data)
        return True


class _MockLogListener:
    '''
        Mock listener capturing diagnostic log messages.
    '''

    def __init__(self) -> None:
        '''Initializes mock log listener.'''
        self.logs: list[tuple[str, str]] = []

    def append_log(self, message: str, tag: str) -> None:
        '''Appends log.'''
        self.logs.append((message, tag))

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockKinematics:
    '''
        Mock kinematics solver for testing queue pumper.
    '''

    def solve_ik(self, pose: ScaraPose, elbow_left: bool = True) -> ScaraJoints:
        '''Solves inverse kinematics.'''
        _ = elbow_left
        return ScaraJoints(theta1=10.0, theta2=20.0, z=pose.z, theta4=pose.phi, reachable=True)

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''Solves forward kinematics.'''
        return ScaraPose(x=10.0, y=20.0, z=joints.z, phi=joints.theta4)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''Converts joints to steps.'''
        return ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=int(joints.z * 10), j4_steps=0)

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''Converts steps to joints.'''
        return ScaraJoints(theta1=10.0, theta2=20.0, z=steps.z_steps / 10.0, theta4=0.0, reachable=True)


class TestQueueStreamer(TestCase):
    '''
        Unit tests for QueueStreamer.

        It defines:

            :methods:
                | test_stream_trajectory_when_connected - Tests streaming trajectory waypoints when transport is connected.
                | test_stream_trajectory_when_disconnected - Tests that streaming does not write when transport is disconnected.
                | test_stream_trajectory_and_clear - Tests streaming trajectory waypoints and flushing queue.
                | test_process_ack - Tests updating flow window free slots and pumping queue.
    '''

    def test_stream_trajectory_when_connected(self) -> None:
        '''
            Tests streaming trajectory waypoints when transport is connected.

            :exceptions: None.
        '''
        transport = _MockTransport(connected=True)
        log_listener = _MockLogListener()
        window = FlowWindow()
        kinematics = _MockKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        pumper_deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumperFactory.create(dependencies=pumper_deps)
        streamer_deps = StreamerDependencies(
            transport=transport,
            flow_window=window,
            pumper=pumper,
        )
        streamer = QueueStreamer(dependencies=streamer_deps)

        pose = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        streamer.stream_trajectory([pose])

        self.assertEqual(len(transport.written_packets), 1)
        self.assertEqual(len(log_listener.logs), 1)
        self.assertEqual(streamer.get_version(), '1.0.2')

    def test_stream_trajectory_when_disconnected(self) -> None:
        '''
            Tests that streaming does not write when transport is disconnected.

            :exceptions: None.
        '''
        transport = _MockTransport(connected=False)
        log_listener = _MockLogListener()
        window = FlowWindow()
        kinematics = _MockKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        pumper_deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumperFactory.create(dependencies=pumper_deps)
        streamer_deps = StreamerDependencies(
            transport=transport,
            flow_window=window,
            pumper=pumper,
        )
        streamer = QueueStreamer(dependencies=streamer_deps)

        pose = ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0)
        streamer.stream_trajectory([pose])

        self.assertEqual(len(transport.written_packets), 0)

    def test_stream_trajectory_and_clear(self) -> None:
        '''
            Tests streaming trajectory waypoints and flushing queue.

            :exceptions: None.
        '''
        transport = _MockTransport(connected=True)
        log_listener = _MockLogListener()
        window = FlowWindow()
        kinematics = _MockKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        pumper_deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumperFactory.create(dependencies=pumper_deps)
        streamer_deps = StreamerDependencies(
            transport=transport,
            flow_window=window,
            pumper=pumper,
        )
        streamer = QueueStreamer(dependencies=streamer_deps)

        poses = [
            ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0),
            ScaraPose(x=15.0, y=25.0, z=5.0, phi=0.0),
        ]
        streamer.stream_trajectory(poses)
        self.assertEqual(len(transport.written_packets), 2)

        streamer.clear()
        for _ in range(16):
            self.assertTrue(window.acquire_slot())

    def test_process_ack(self) -> None:
        '''
            Tests updating flow window free slots and pumping queue.

            :exceptions: None.
        '''
        transport = _MockTransport(connected=True)
        log_listener = _MockLogListener()
        window = FlowWindow()
        kinematics = _MockKinematics()
        codec = BinaryFrameCodecAdapterFactory.create()
        pumper_deps = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=window,
            kinematics=kinematics,
            codec=codec,
        )
        pumper = QueuePumperFactory.create(dependencies=pumper_deps)
        streamer_deps = StreamerDependencies(
            transport=transport,
            flow_window=window,
            pumper=pumper,
        )
        streamer = QueueStreamer(dependencies=streamer_deps)

        window.acquire_slot()
        window.acquire_slot()
        streamer.process_ack(free_slots=14)
        self.assertTrue(window.acquire_slot())


if __name__ == '__main__':
    unittest_main()
