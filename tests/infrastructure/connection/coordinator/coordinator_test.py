# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for ConnectionCoordinator.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator as IComConnectionCoordinator
from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.connection.coordinator.coordinator import ConnectionCoordinator
from scaraemu.infrastructure.connection.coordinator.dependencies import CoordinatorDependencies
from scaraemu.infrastructure.connection.coordinator.icoordinator import IConnectionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockConnection:
    '''
        Mock connection coordinator simulating serial connection state.
    '''

    def __init__(self, connected: bool = False, connect_result: bool = True) -> None:
        '''Initializes mock connection coordinator.'''
        self.connected: bool = connected
        self.connect_result: bool = connect_result

    def is_connected(self) -> bool:
        '''Checks if connected.'''
        return self.connected

    def connect(self, port: str, baudrate: int) -> bool:
        '''Connects mock connection.'''
        _ = (port, baudrate)
        if self.connect_result:
            self.connected = True
        return self.connect_result

    def disconnect(self) -> None:
        '''Disconnects mock connection.'''
        self.connected = False

    def set_listener(self, listener: object) -> None:
        '''Sets listener.'''
        _ = listener

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockBridgeListener:
    '''
        Mock listener capturing connection state changes.
    '''

    def __init__(self) -> None:
        '''Initializes mock listener.'''
        self.state_changes: list[bool] = []

    def on_state_change(self, connected: bool) -> None:
        '''Captures state change.'''
        self.state_changes.append(connected)

    def on_telemetry(self, pose: ScaraPose) -> None:
        '''Handles telemetry.'''
        _ = pose

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockQueueStreamer:
    '''
        Mock queue streamer recording clear operations.
    '''

    def __init__(self) -> None:
        '''Initializes mock queue streamer.'''
        self.clear_count: int = 0

    def stream_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''Streams trajectory poses.'''
        _ = poses

    def process_ack(self, free_slots: int) -> None:
        '''Processes ack with free slots.'''
        _ = free_slots

    def clear(self) -> None:
        '''Clears streamer.'''
        self.clear_count += 1

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockCommandDispatcher:
    '''
        Mock command dispatcher recording sent commands.
    '''

    def __init__(self) -> None:
        '''Initializes mock command dispatcher.'''
        self.sent_commands: list[MessageId] = []

    def send_command(self, msg_id: MessageId, payload: bytes = b'') -> None:
        '''Records sent command.'''
        _ = payload
        self.sent_commands.append(msg_id)

    def clear_queue(self) -> None:
        '''Clears command queue.'''

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class TestConnectionCoordinator(TestCase):
    '''
        Unit test cases for ConnectionCoordinator.

        It defines:

            :methods:
                | test_structural_protocol_conformity - Tests structural conformity to IConnectionCoordinator.
                | test_handle_connect_toggle_when_disconnected_success - Tests connecting when disconnected.
                | test_handle_connect_toggle_when_disconnected_failure - Tests failed connection attempt.
                | test_handle_connect_toggle_when_connected - Tests disconnecting when connected.
    '''

    def test_structural_protocol_conformity(self) -> None:
        '''
            Tests structural conformity to IConnectionCoordinator.

            :exceptions: None.
        '''
        connection = _MockConnection()
        listener = _MockBridgeListener()
        streamer = _MockQueueStreamer()
        command_dispatcher = _MockCommandDispatcher()
        bundle = CoordinatorDependencies(
            connection=connection,
            listener=listener,
            streamer=streamer,
            command_dispatcher=command_dispatcher,
        )
        coordinator = ConnectionCoordinator(dependencies=bundle)
        self.assertIsInstance(coordinator, IConnectionCoordinator)
        self.assertIsInstance(connection, IComConnectionCoordinator)
        self.assertEqual(coordinator.get_version(), '1.0.2')

    def test_handle_connect_toggle_when_disconnected_success(self) -> None:
        '''
            Tests connecting when disconnected: connects, notifies, clears, and queries status.

            :exceptions: None.
        '''
        connection = _MockConnection(connected=False, connect_result=True)
        listener = _MockBridgeListener()
        streamer = _MockQueueStreamer()
        command_dispatcher = _MockCommandDispatcher()
        bundle = CoordinatorDependencies(
            connection=connection,
            listener=listener,
            streamer=streamer,
            command_dispatcher=command_dispatcher,
        )
        coordinator = ConnectionCoordinator(dependencies=bundle)

        coordinator.handle_connect_toggle('/dev/ttyUSB0', 115200)
        self.assertTrue(connection.is_connected())
        self.assertEqual(listener.state_changes, [True])
        self.assertEqual(streamer.clear_count, 1)
        self.assertIn(MessageId.CMD_GET_STATUS, command_dispatcher.sent_commands)

    def test_handle_connect_toggle_when_disconnected_failure(self) -> None:
        '''
            Tests connection failure: notifies False, does not send status.

            :exceptions: None.
        '''
        connection = _MockConnection(connected=False, connect_result=False)
        listener = _MockBridgeListener()
        streamer = _MockQueueStreamer()
        command_dispatcher = _MockCommandDispatcher()
        bundle = CoordinatorDependencies(
            connection=connection,
            listener=listener,
            streamer=streamer,
            command_dispatcher=command_dispatcher,
        )
        coordinator = ConnectionCoordinator(dependencies=bundle)

        coordinator.handle_connect_toggle('/dev/ttyUSB0', 115200)
        self.assertFalse(connection.is_connected())
        self.assertEqual(listener.state_changes, [False])
        self.assertEqual(command_dispatcher.sent_commands, [])

    def test_handle_connect_toggle_when_connected(self) -> None:
        '''
            Tests disconnecting when connected: disconnects, clears, and notifies.

            :exceptions: None.
        '''
        connection = _MockConnection(connected=True)
        listener = _MockBridgeListener()
        streamer = _MockQueueStreamer()
        command_dispatcher = _MockCommandDispatcher()
        bundle = CoordinatorDependencies(
            connection=connection,
            listener=listener,
            streamer=streamer,
            command_dispatcher=command_dispatcher,
        )
        coordinator = ConnectionCoordinator(dependencies=bundle)

        coordinator.handle_connect_toggle('/dev/ttyUSB0', 115200)
        self.assertFalse(connection.is_connected())
        self.assertEqual(listener.state_changes, [False])
        self.assertEqual(streamer.clear_count, 1)
        self.assertEqual(command_dispatcher.sent_commands, [])


if __name__ == '__main__':
    unittest_main()
