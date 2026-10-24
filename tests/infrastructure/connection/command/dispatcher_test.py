# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit tests for CommandDispatcher.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.connection.command.dependencies import CommandDependencies
from scaraemu.infrastructure.connection.command.dispatcher import CommandDispatcher
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory

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
        Mock transport simulating serial communication.
    '''

    def __init__(self) -> None:
        self.written_bytes: list[bytes] = []

    def is_connected(self) -> bool:
        '''Checks if connected.'''
        return True

    def connect(self, port: str, baudrate: int) -> bool:
        '''Connects transport.'''
        _ = (port, baudrate)
        return True

    def disconnect(self) -> None:
        '''Disconnects transport.'''

    def write_bytes(self, data: bytes) -> bool:
        '''Writes bytes to mock transport.'''
        self.written_bytes.append(data)
        return True

    def get_version(self) -> str:
        '''Returns mock version.'''
        return '1.0.2'


class _MockLogListener:
    '''
        Mock log listener capturing diagnostics.
    '''

    def __init__(self) -> None:
        self.logs: list[tuple[str, str]] = []

    def append_log(self, message: str, tag: str) -> None:
        '''Appends diagnostic log.'''
        self.logs.append((message, tag))

    def get_version(self) -> str:
        '''Returns mock version.'''
        return '1.0.2'


class _MockQueueStreamer:
    '''
        Mock queue streamer recording clear calls.
    '''

    def __init__(self) -> None:
        self.cleared: bool = False

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''Streams trajectory.'''
        _ = poses

    def process_ack(self, free_slots: int) -> None:
        '''Processes ack.'''
        _ = free_slots

    def clear(self) -> None:
        '''Clears queue.'''
        self.cleared = True

    def get_version(self) -> str:
        '''Returns mock version.'''
        return '1.0.2'


class TestCommandDispatcher(TestCase):
    '''
        Unit test cases for CommandDispatcher.

        It defines:

            :methods:
                | test_structural_protocol_conformity - Tests structural conformity to ICommandDispatcher.
                | test_send_command - Tests transmitting binary command frame across transport.
                | test_clear_queue - Tests flushing streamer queue.
    '''

    def test_structural_protocol_conformity(self) -> None:
        '''
            Tests structural conformity to ICommandDispatcher.

            :exceptions: None.
        '''
        transport = _MockTransport()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        bundle = CommandDependencies(
            transport=transport,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
        )
        dispatcher = CommandDispatcher(dependencies=bundle)
        self.assertIsInstance(dispatcher, ICommandDispatcher)
        self.assertEqual(dispatcher.get_version(), '1.0.2')

    def test_send_command(self) -> None:
        '''
            Tests transmitting binary command frame across transport.

            :exceptions: None.
        '''
        transport = _MockTransport()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        bundle = CommandDependencies(
            transport=transport,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
        )
        dispatcher = CommandDispatcher(dependencies=bundle)

        dispatcher.send_command(MessageId.CMD_ESTOP)
        self.assertEqual(len(transport.written_bytes), 1)
        self.assertEqual(len(log_listener.logs), 1)
        self.assertIn('CMD_ESTOP', log_listener.logs[0][0])
        self.assertEqual(log_listener.logs[0][1], 'tx')

    def test_clear_queue(self) -> None:
        '''
            Tests flushing streamer queue.

            :exceptions: None.
        '''
        transport = _MockTransport()
        log_listener = _MockLogListener()
        streamer = _MockQueueStreamer()
        codec = BinaryFrameCodecAdapterFactory.create()
        bundle = CommandDependencies(
            transport=transport,
            log_listener=log_listener,
            streamer=streamer,
            codec=codec,
        )
        dispatcher = CommandDispatcher(dependencies=bundle)

        dispatcher.clear_queue()
        self.assertTrue(streamer.cleared)


if __name__ == '__main__':
    unittest_main()
