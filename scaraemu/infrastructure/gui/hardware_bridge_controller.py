# -*- coding: UTF-8 -*-

'''
Module
    hardware_bridge_controller.py
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
    Hardware bridge communication controller for GUI adapter.
'''

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from typing import Final, Callable

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.communication.protocol.protocol_parser import ProtocolParser
from scaraemu.infrastructure.communication.protocol.command_formatter import CommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class HardwareBridgeController:
    '''
        Controller managing serial hardware bridge interactions and logging.

        It defines:

            :attributes:
                | MAX_IN_FLIGHT - Maximum concurrent commands dispatched to firmware.
                | _transport - Communication transport layer.
                | _pending_queue - Host motion queue of pending target poses.
                | _in_flight_count - Number of commands currently queued in firmware.
                | _on_state_change - Callback on connection status changes.
                | _on_telemetry - Callback receiving hardware ScaraPose telemetry.
                | _on_log_append - Callback dispatching log message and tag string.
            :methods:
                | __init__ - Initializes hardware bridge controller.
                | set_log_listener - Attaches logging listener callback.
                | handle_connect_toggle - Toggles connection to serial port.
                | handle_manual_send - Sends manual command string to microcontroller.
                | send_hardware_move - Sends point move packet to microcontroller.
                | enqueue_hardware_trajectory - Enqueues multiple waypoints for streaming.
                | clear_queue - Flushes pending host queue and resets flow control.
                | send_hardware_hold - Sends feed-hold pause command to hardware.
                | send_hardware_resume - Sends motion resume command to hardware.
                | on_serial_line_received - Processes incoming serial text line.
                | on_serial_log - Logs transport diagnostic messages.
                | _pump_queue - Streams queued packets within safe flow control window.
    '''

    MAX_IN_FLIGHT: Final[int] = 16

    _transport: Final[ITransport]
    _pending_queue: deque[ScaraPose]
    _firmware_queue_depth: int
    _unacked_sent_count: int
    _on_state_change: Callable[[bool], None] | None
    _on_telemetry: Callable[[ScaraPose], None] | None
    _on_log_append: Callable[[str, str], None] | None
    _on_elbow_change: Callable[[bool], None] | None

    def __init__(
        self,
        transport: ITransport,
        on_state_change: Callable[[bool], None] | None = None,
        on_telemetry: Callable[[ScaraPose], None] | None = None,
        on_log_append: Callable[[str, str], None] | None = None,
        on_elbow_change: Callable[[bool], None] | None = None
    ) -> None:
        '''
            Initializes hardware bridge controller.

            :param transport: Communication transport.
            :param on_state_change: Status change callback.
            :param on_telemetry: Hardware telemetry pose callback.
            :param on_log_append: Log output callback.
            :param on_elbow_change: Hardware elbow mode callback.
            :exceptions: None.
        '''
        self._transport = transport
        self._pending_queue = deque()
        self._firmware_queue_depth = 0
        self._unacked_sent_count = 0
        self._on_state_change = on_state_change
        self._on_telemetry = on_telemetry
        self._on_log_append = on_log_append
        self._on_elbow_change = on_elbow_change

        self._transport.set_callbacks(
            on_line=self.on_serial_line_received,
            on_log=self.on_serial_log
        )

    def set_log_listener(self, on_log_append: Callable[[str, str], None] | None) -> None:
        '''
            Attaches logging listener callback.

            :param on_log_append: Function receiving log text and style tag.
            :exceptions: None.
        '''
        self._on_log_append = on_log_append

    def handle_connect_toggle(self, port: str, baud: int) -> None:
        '''
            Toggles connection to serial port.

            :param port: Target serial port path.
            :param baud: Baudrate.
            :exceptions: None.
        '''
        if self._transport.is_connected():
            self._transport.disconnect()
            self.clear_queue()
            if self._on_state_change is not None:
                self._on_state_change(False)
        else:
            success = self._transport.connect(port, baud)
            if self._on_state_change is not None:
                self._on_state_change(success)
            if success:
                self.clear_queue()
                self.handle_manual_send(CommandFormatter.format_get_position())

    def handle_manual_send(self, cmd: str) -> None:
        '''
            Sends manual command string to microcontroller.

            :param cmd: Raw command string.
            :exceptions: None.
        '''
        self._transport.write_line(cmd)
        if self._on_log_append is not None:
            self._on_log_append(f'TX > {cmd}', 'tx')

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Sends point move packet to microcontroller with flow control.

            :param pose: Target ScaraPose.
            :exceptions: None.
        '''
        if self._transport.is_connected():
            self._pending_queue.append(pose)
            self._pump_queue()

    def enqueue_hardware_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Enqueues multiple waypoints and streams them with flow control.

            :param poses: Sequence of target ScaraPoses.
            :exceptions: None.
        '''
        if self._transport.is_connected():
            self._pending_queue.extend(poses)
            self._pump_queue()

    def clear_queue(self) -> None:
        '''
            Flushes pending host queue and resets flow control state.

            :exceptions: None.
        '''
        self._pending_queue.clear()
        self._firmware_queue_depth = 0
        self._unacked_sent_count = 0

    def send_hardware_hold(self) -> None:
        '''
            Sends feed-hold pause command to hardware microcontroller.

            :exceptions: None.
        '''
        if self._transport.is_connected():
            self.handle_manual_send(CommandFormatter.format_hold())

    def send_hardware_resume(self) -> None:
        '''
            Sends motion resume command to hardware microcontroller.

            :exceptions: None.
        '''
        if self._transport.is_connected():
            self.handle_manual_send(CommandFormatter.format_resume())

    def _pump_queue(self) -> None:
        '''
            Streams queued move packets within safe flow control window.

            :exceptions: None.
        '''
        if not self._transport.is_connected():
            return

        while (
            self._pending_queue
            and (self._firmware_queue_depth + self._unacked_sent_count) < self.MAX_IN_FLIGHT
        ):
            pose = self._pending_queue.popleft()
            packet = CommandFormatter.format_move_pose(pose)
            self._transport.write_line(packet)
            self._unacked_sent_count += 1
            if self._on_log_append is not None:
                self._on_log_append(f'TX > {packet}', 'tx')

    def on_serial_line_received(self, line: str) -> None:
        '''
            Processes incoming serial text line.

            :param line: Received text line.
            :exceptions: None.
        '''
        resp = ProtocolParser.parse_line(line)
        if self._on_log_append is not None:
            tag = 'rx' if resp.is_success else 'err'
            self._on_log_append(f'RX < {line}', tag)

        if (
            resp.response_type in ('ACK', 'NACK', 'BUFFER_FULL')
            or resp.raw_line.startswith(('<RESP:ACK', '<RESP:NACK'))
        ):
            if self._unacked_sent_count > 0:
                self._unacked_sent_count -= 1

        if resp.payload and 'queue_depth' in resp.payload:
            self._firmware_queue_depth = int(resp.payload['queue_depth'])
            self._pump_queue()
        elif resp.response_type == 'BUFFER_FULL':
            self._firmware_queue_depth = self.MAX_IN_FLIGHT
        elif resp.response_type in ('MOVE_DONE', 'MOVE_FAILED') or not resp.is_success:
            if self._firmware_queue_depth > 0:
                self._firmware_queue_depth -= 1
            elif self._unacked_sent_count > 0:
                self._unacked_sent_count -= 1
            self._pump_queue()

        if (
            resp.response_type in ('TELEM', 'MOVE_DONE', 'HOMED_SUCCESS')
            and self._on_telemetry is not None
        ):
            payload = resp.payload
            if 'x' in payload and 'y' in payload and 'z' in payload:
                try:
                    pose = ScaraPose(
                        x=float(payload['x']),
                        y=float(payload['y']),
                        z=float(payload['z']),
                        phi=float(payload.get('phi', 0.0))
                    )
                    self._on_telemetry(pose)
                except (ValueError, TypeError):
                    pass

        if resp.response_type == 'ELBOW' and self._on_elbow_change is not None:
            val = resp.payload.get('elbow') or resp.payload.get('config')
            if isinstance(val, str):
                self._on_elbow_change(val.upper() == 'LEFT')

    def on_serial_log(self, message: str) -> None:
        '''
            Logs transport diagnostic messages.

            :param message: Diagnostic message string.
            :exceptions: None.
        '''
        if self._on_log_append is not None:
            tag = 'err' if message.startswith('[ERR]') else 'host'
            log_msg = message if message.startswith(('[HOST]:', '[ERR]:')) else f'[HOST]: {message}'
            self._on_log_append(log_msg, tag)
