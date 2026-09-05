# -*- coding: UTF-8 -*-

'''
Module
    virtual_robot_server.py
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
    Implementation of IVirtualRobotServer simulating RP2040 firmware over TCP loopback for scarajectory streaming.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
    socket as Socket,
    timeout as SocketTimeout,
)
from threading import Event, Lock, Thread
from typing import Callable, ClassVar, Final

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.service.iemulator_service import IEmulatorService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualRobotServer:
    '''
        Virtual robot controller TCP server emulating RP2040 firmware execution and protocol responses.

        It defines:

            :attributes:
                | _emulator - SCARA emulator core service instance.
                | _on_log - Optional log message consumer callback.
                | _server_socket - Listening socket handle.
                | _server_thread - Background socket listener thread.
                | _stop_event - Event signaling server shutdown.
                | _lock - Mutex protecting state mutations.
                | _planned_pose - Optional cached target pose for chained trajectory streaming.
                | _port - Active bound listening port.
            :methods:
                | __init__ - Initializes virtual robot server.
                | start - Starts listening for external host connections.
                | stop - Terminates background server and closes client sockets.
                | is_running - Checks whether server is currently active.
                | get_port - Returns the active listening port number.
                | _server_loop - Background accept loop dispatching client sessions.
                | _handle_client - Manages reading lines and responding to connected CAM client.
                | _process_command - Parses individual host command line and returns protocol response.
    '''

    _MOVE_RE: ClassVar[Pattern[str]] = re_compile(
        r'<pt#(?P<x>[-+]?[0-9]*\.?[0-9]+)#(?P<y>[-+]?[0-9]*\.?[0-9]+)#(?P<z>[-+]?[0-9]*\.?[0-9]+)#(?P<phi>[-+]?[0-9]*\.?[0-9]+)'
    )

    _emulator: Final[IEmulatorService]
    _on_log: Callable[[str], None] | None
    _server_socket: Socket | None
    _server_thread: Thread | None
    _stop_event: Final[Event]
    _lock: Final[Lock]
    _planned_pose: ScaraPose | None
    _port: int

    def __init__(
        self,
        emulator: IEmulatorService,
        on_log: Callable[[str], None] | None = None,
    ) -> None:
        '''
            Initializes virtual robot server.

            :param emulator: SCARA emulator core service instance.
            :param on_log: Optional logging callback.
            :exceptions: None.
        '''
        self._emulator = emulator
        self._on_log = on_log
        self._server_socket = None
        self._server_thread = None
        self._stop_event = Event()
        self._lock = Lock()
        self._planned_pose = None
        self._port = 0

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts listening for external host connections.

            :param host: Local IP bind address.
            :param port: TCP listening port number.
            :return: True if server started successfully, False otherwise.
            :exceptions: None.
        '''
        with self._lock:
            if self._server_socket is not None:
                return True

            try:
                srv = Socket(AF_INET, SOCK_STREAM)
                srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                srv.bind((host, port))
                srv.listen(1)
                srv.settimeout(0.5)
                self._server_socket = srv
                self._port = srv.getsockname()[1]
                self._stop_event.clear()
                self._server_thread = Thread(target=self._server_loop, daemon=True)
                self._server_thread.start()
                if self._on_log is not None:
                    self._on_log(f'✅ Virtual Robot Controller listening on {host}:{self._port}')
                return True
            except OSError as exc:
                if self._on_log is not None:
                    self._on_log(f'❌ Failed to start Virtual Robot Server: {exc}')
                return False

    def stop(self) -> None:
        '''
            Terminates background server and closes client sockets.

            :exceptions: None.
        '''
        with self._lock:
            self._stop_event.set()
            if self._server_socket is not None:
                try:
                    self._server_socket.close()
                except OSError:
                    pass
                self._server_socket = None
                self._port = 0
                if self._on_log is not None:
                    self._on_log('ℹ️ Virtual Robot Controller stopped.')

    def is_running(self) -> bool:
        '''
            Checks whether server is currently active.

            :return: True if listening, False otherwise.
            :exceptions: None.
        '''
        return self._server_socket is not None and not self._stop_event.is_set()

    def get_port(self) -> int:
        '''
            Returns the active listening port number.

            :return: Port integer.
            :exceptions: None.
        '''
        return self._port

    def _server_loop(self) -> None:
        '''
            Background accept loop dispatching client sessions.

            :exceptions: None.
        '''
        while not self._stop_event.is_set():
            try:
                if self._server_socket is None:
                    break
                client_sock, client_addr = self._server_socket.accept()
                if self._on_log is not None:
                    self._on_log(f'🔗 Digital Twin client connected from {client_addr[0]}:{client_addr[1]}')
                self._handle_client(client_sock=client_sock)
            except SocketTimeout:
                continue
            except OSError:
                break

    def _handle_client(self, *, client_sock: Socket) -> None:
        '''
            Manages reading lines and responding to connected CAM client.

            :param client_sock: Connected client socket.
            :exceptions: None.
        '''
        client_sock.settimeout(0.5)
        buffer = ''
        try:
            while not self._stop_event.is_set():
                try:
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    buffer += data.decode('utf-8', errors='replace')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line:
                            responses = self._process_command(cmd=line)
                            for resp in responses:
                                client_sock.sendall((resp + '\n').encode('utf-8'))
                except SocketTimeout:
                    continue
        except OSError:
            pass
        finally:
            try:
                client_sock.close()
            except OSError:
                pass
            if self._on_log is not None:
                self._on_log('🔌 Digital Twin client disconnected.')

    def _process_command(self, *, cmd: str) -> list[str]:
        '''
            Parses individual host command line and returns protocol responses.

            :param cmd: Raw command string from host.
            :return: List of ASCII response strings.
        '''
        responses: list[str] = []
        if cmd.startswith('<pt#'):
            match = self._MOVE_RE.search(cmd)
            if match:
                x = float(match.group('x'))
                y = float(match.group('y'))
                z = float(match.group('z'))
                phi = float(match.group('phi'))
                pose = ScaraPose(x=x, y=y, z=z, phi=phi)
                self._emulator.enqueue_trajectory([pose])
                self._planned_pose = pose
                responses.append('<RESP:ACK#QUEUE=1>')
                responses.append(f'<RESP:MOVE_DONE#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}>')
            else:
                responses.append('<RESP:NACK#INVALID_POINT>')
            return responses

        if cmd.startswith('<CMD:'):
            body = cmd[5:].rstrip('>')
            parts = body.split('#')
            op = parts[0].upper()

            match op:
                case 'ENABLE':
                    self._emulator.set_motors_enabled(True)
                    responses.append('<RESP:ACK#MOTORS_ENABLED>')
                case 'DISABLE':
                    self._emulator.set_motors_enabled(False)
                    responses.append('<RESP:ACK#MOTORS_DISABLED>')
                case 'HOME':
                    home_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
                    self._emulator.set_target_pose(home_pose, direct=True)
                    self._planned_pose = home_pose
                    responses.append('<RESP:HOMED_SUCCESS#RIGHT>')
                case 'HOLD' | 'PAUSE':
                    self._emulator.set_hold(True)
                    responses.append('<RESP:ACK#HOLD>')
                case 'RESUME':
                    self._emulator.set_hold(False)
                    responses.append('<RESP:ACK#RESUME>')
                case 'ESTOP':
                    self._emulator.set_estop(True)
                    responses.append('<RESP:ACK#ESTOP>')
                case 'PUMP':
                    state = parts[1] if len(parts) > 1 else '0'
                    tag = 'PUMP_ON' if state == '1' else 'PUMP_OFF'
                    responses.append(f'<RESP:ACK#{tag}>')
                case 'VALVE':
                    state = parts[1] if len(parts) > 1 else '0'
                    tag = 'VALVE_ON' if state == '1' else 'VALVE_OFF'
                    responses.append(f'<RESP:ACK#{tag}>')
                case 'WAIT':
                    ms_val = parts[1] if len(parts) > 1 else '0'
                    responses.append(f'<RESP:ACK#WAIT_DONE#{ms_val}>')
                case 'OVERRIDE':
                    pct = parts[1] if len(parts) > 1 else '100'
                    responses.append(f'<RESP:ACK#OVERRIDE#{pct}>')
                case 'GET_POS' | 'GETPOS':
                    curr = self._emulator.get_current_pose()
                    responses.append(f'<RESP:POS#{curr.x:.2f}#{curr.y:.2f}#{curr.z:.2f}#{curr.phi:.2f}>')
                case 'STATUS':
                    curr = self._emulator.get_current_pose()
                    responses.append(
                        f'<RESP:STATUS#STATE=IDLE#X={curr.x:.2f}#Y={curr.y:.2f}#Z={curr.z:.2f}#PHI={curr.phi:.2f}>'
                    )
                case 'JOG':
                    if len(parts) >= 3:
                        axis = parts[1].upper()
                        try:
                            step = float(parts[2])
                        except ValueError:
                            step = 0.0

                        sim_state = self._emulator.get_simulation_state()
                        base = (
                            self._planned_pose
                            if (self._planned_pose is not None and sim_state.queue_depth > 0)
                            else self._emulator.get_current_pose()
                        )
                        new_x, new_y, new_z, new_phi = base.x, base.y, base.z, base.phi
                        if axis == 'X':
                            new_x += step
                        elif axis == 'Y':
                            new_y += step
                        elif axis == 'Z':
                            new_z += step
                        elif axis in ('PHI', 'P'):
                            new_phi += step

                        target = ScaraPose(x=new_x, y=new_y, z=new_z, phi=new_phi)
                        enqueued = self._emulator.enqueue_trajectory([target])
                        if enqueued > 0:
                            self._planned_pose = target
                            responses.append(f'<RESP:ACK#JOG_QUEUED#QUEUE={enqueued}>')
                            responses.append(
                                f'<RESP:MOVE_DONE#{new_x:.2f}#{new_y:.2f}#{new_z:.2f}#{new_phi:.2f}>'
                            )
                        else:
                            responses.append('<RESP:NACK#OUT_OF_BOUNDS>')
                    else:
                        responses.append('<RESP:NACK#INVALID_JOG>')
                case _:
                    responses.append(f'<RESP:ACK#{op}>')
            return responses

        responses.append('<RESP:ACK#UNKNOWN>')
        return responses
