# -*- coding: UTF-8 -*-

'''
Module
    test_hardware_bridge_controller.py
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
    Unit tests for HardwareBridgeController with mock transport and listeners.
'''

from __future__ import annotations

import unittest
from typing import Callable

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.transport.serial_transport import SerialTransport
from scaraemu.infrastructure.gui.hardware_bridge_controller import HardwareBridgeController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockTransport:
    '''Mock ITransport implementation for testing HardwareBridgeController.'''

    def __init__(self) -> None:
        self.connected: bool = True
        self.written_lines: list[str] = []
        self.on_line: Callable[[str], None] | None = None
        self.on_log: Callable[[str], None] | None = None

    def is_connected(self) -> bool:
        return self.connected

    def connect(self, port: str, baudrate: int) -> bool:
        self.connected = True
        return True

    def disconnect(self) -> None:
        self.connected = False

    def write_line(self, data: str) -> bool:
        self.written_lines.append(data)
        return True

    def set_callbacks(
        self,
        on_line: Callable[[str], None] | None = None,
        on_log: Callable[[str], None] | None = None
    ) -> None:
        self.on_line = on_line
        self.on_log = on_log


class TestHardwareBridgeController(unittest.TestCase):
    '''Unit test cases for decoupled HardwareBridgeController.'''

    def test_bridge_lifecycle_and_callbacks(self) -> None:
        '''Tests connection callbacks and telemetry dispatching.'''
        state_changes: list[bool] = []
        telemetries: list[ScaraPose] = []
        logs: list[tuple[str, str]] = []

        transport = SerialTransport()
        bridge = HardwareBridgeController(
            transport=transport,
            on_state_change=state_changes.append,
            on_telemetry=telemetries.append,
            on_log_append=lambda msg, tag: logs.append((msg, tag))
        )

        bridge.handle_manual_send('<CMD:STATUS>')
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0][0], 'TX > <CMD:STATUS>')
        self.assertEqual(logs[0][1], 'tx')

        bridge.on_serial_log('Device disconnected')
        self.assertEqual(len(logs), 2)
        self.assertIn('Device disconnected', logs[1][0])

        bridge.on_serial_line_received('<POS#X=150.00#Y=20.00#Z=10.00#PHI=0.00#J1=0#J2=0#Z_STEP=0#J4=0>')
        self.assertEqual(len(telemetries), 1)
        self.assertAlmostEqual(telemetries[0].x, 150.0)
        self.assertAlmostEqual(telemetries[0].y, 20.0)

    def test_set_log_listener(self) -> None:
        '''Tests updating log listener dynamically.'''
        transport = SerialTransport()
        bridge = HardwareBridgeController(transport=transport)
        logs: list[str] = []
        bridge.set_log_listener(lambda msg, tag: logs.append(msg))
        bridge.handle_manual_send('<CMD:ENABLE>')
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0], 'TX > <CMD:ENABLE>')

    def test_flow_control_streaming(self) -> None:
        '''Tests flow control streaming without buffer overflow.'''
        mock_transport = MockTransport()
        bridge = HardwareBridgeController(transport=mock_transport)

        # Enqueue 30 waypoints
        poses = [ScaraPose(x=float(i), y=0.0, z=20.0) for i in range(30)]
        bridge.enqueue_hardware_trajectory(poses)

        # Should only dispatch up to MAX_IN_FLIGHT (16)
        self.assertEqual(len(mock_transport.written_lines), HardwareBridgeController.MAX_IN_FLIGHT)

        # Simulate firmware completing 1 move
        bridge.on_serial_line_received('<RESP:MOVE_DONE#X=0.00#Y=0.00#Z=20.00#PHI=0.00>')

        # Should now have dispatched 17 moves (1 more streamed)
        self.assertEqual(len(mock_transport.written_lines), HardwareBridgeController.MAX_IN_FLIGHT + 1)

        # Clear queue
        bridge.clear_queue()
        # Another MOVE_DONE should not send anything more
        bridge.on_serial_line_received('<RESP:MOVE_DONE#X=1.00#Y=0.00#Z=20.00#PHI=0.00>')
        self.assertEqual(len(mock_transport.written_lines), HardwareBridgeController.MAX_IN_FLIGHT + 1)


if __name__ == '__main__':
    unittest.main()
