# -*- coding: UTF-8 -*-

'''
Module
    virtual_command_processor.py
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
    ASCII protocol parser and command dispatcher for the virtual robot server.
'''

from __future__ import annotations

from re import compile as re_compile, Pattern
from typing import ClassVar, Final

from scaraemu.core.model.kinematics.scara_pose import ScaraPose
from scaraemu.core.service.simulation.iemulator_service import IEmulatorService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VirtualCommandProcessor:
    '''
        Processes ASCII protocol commands and generates firmware-compatible responses.

        It defines:

            :attributes:
                | _MOVE_RE - Regex pattern matching point movement commands.
                | _emulator - SCARA emulator core service instance.
                | _planned_pose - Optional cached target pose for chained moves.
            :methods:
                | __init__ - Initializes the virtual command processor.
                | process_command - Parses a host command line and returns ASCII responses.
                | reset - Clears the internal planned pose state.
    '''

    _MOVE_RE: ClassVar[Pattern[str]] = re_compile(
        r'<pt#(?P<x>[-+]?[0-9]*\.?[0-9]+)#(?P<y>[-+]?[0-9]*\.?[0-9]+)#'
        r'(?P<z>[-+]?[0-9]*\.?[0-9]+)#(?P<phi>[-+]?[0-9]*\.?[0-9]+)'
    )

    _emulator: Final[IEmulatorService]
    _planned_pose: ScaraPose | None

    def __init__(self, emulator: IEmulatorService) -> None:
        '''
            Initializes the virtual command processor with an emulator service.

            :param emulator: SCARA emulator core service instance.
            :exceptions: None.
        '''
        self._emulator = emulator
        self._planned_pose = None

    def reset(self) -> None:
        '''
            Clears cached planned target pose.

            :exceptions: None.
        '''
        self._planned_pose = None

    def process_command(self, cmd: str) -> list[str]:
        '''
            Parses an individual host command line and returns protocol responses.

            :param cmd: Raw command string from host.
            :return: List of ASCII response strings.
            :exceptions: None.
        '''
        if cmd.startswith('<pt#'):
            return self._handle_point_move(cmd)

        if cmd.startswith('<CMD:'):
            return self._handle_cmd(cmd)

        return ['<RESP:ACK#UNKNOWN>']

    def _handle_point_move(self, cmd: str) -> list[str]:
        '''
            Processes <pt#...> trajectory point command.

            :param cmd: Point command string.
            :return: List of response strings.
            :exceptions: None.
        '''
        match = self._MOVE_RE.search(cmd)
        if match:
            x: float = float(match.group('x'))
            y: float = float(match.group('y'))
            z: float = float(match.group('z'))
            phi: float = float(match.group('phi'))
            pose: ScaraPose = ScaraPose(x=x, y=y, z=z, phi=phi)
            self._emulator.enqueue_trajectory([pose])
            self._planned_pose = pose
            return [
                '<RESP:ACK#QUEUE=1>',
                f'<RESP:MOVE_DONE#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}>'
            ]
        return ['<RESP:NACK#INVALID_POINT>']

    def _handle_cmd(self, cmd: str) -> list[str]:
        '''
            Processes <CMD:...> protocol command.

            :param cmd: Raw CMD string.
            :return: List of response strings.
            :exceptions: None.
        '''
        body: str = cmd[5:].rstrip('>')
        parts: list[str] = body.split('#')
        op: str = parts[0].upper()

        match op:
            case 'ENABLE':
                self._emulator.set_motors_enabled(True)
                return ['<RESP:ACK#MOTORS_ENABLED>']
            case 'DISABLE':
                self._emulator.set_motors_enabled(False)
                return ['<RESP:ACK#MOTORS_DISABLED>']
            case 'HOME':
                home_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
                self._emulator.set_target_pose(home_pose, direct=True)
                self._planned_pose = home_pose
                return ['<RESP:HOMED_SUCCESS#RIGHT>']
            case 'HOLD' | 'PAUSE':
                self._emulator.set_hold(True)
                return ['<RESP:ACK#HOLD>']
            case 'RESUME':
                self._emulator.set_hold(False)
                return ['<RESP:ACK#RESUME>']
            case 'ESTOP':
                self._emulator.set_estop(True)
                return ['<RESP:ACK#ESTOP>']
            case 'PUMP':
                state = parts[1] if len(parts) > 1 else '0'
                tag = 'PUMP_ON' if state == '1' else 'PUMP_OFF'
                return [f'<RESP:ACK#{tag}>']
            case 'VALVE':
                state = parts[1] if len(parts) > 1 else '0'
                tag = 'VALVE_ON' if state == '1' else 'VALVE_OFF'
                return [f'<RESP:ACK#{tag}>']
            case 'WAIT':
                ms_val = parts[1] if len(parts) > 1 else '0'
                return [f'<RESP:ACK#WAIT_DONE#{ms_val}>']
            case 'OVERRIDE':
                pct = parts[1] if len(parts) > 1 else '100'
                return [f'<RESP:ACK#OVERRIDE#{pct}>']
            case 'GET_POS' | 'GETPOS':
                curr = self._emulator.get_current_pose()
                return [f'<RESP:POS#{curr.x:.2f}#{curr.y:.2f}#{curr.z:.2f}#{curr.phi:.2f}>']
            case 'STATUS':
                curr = self._emulator.get_current_pose()
                return [f'<RESP:STATUS#STATE=IDLE#X={curr.x:.2f}#Y={curr.y:.2f}#Z={curr.z:.2f}#PHI={curr.phi:.2f}>']
            case 'SET_ELBOW':
                raw_mode: str = parts[1].upper() if len(parts) > 1 else 'RIGHT'
                is_left: bool = (raw_mode == 'LEFT')
                self._emulator.set_elbow_mode(is_left)
                mode_str: str = 'LEFT' if is_left else 'RIGHT'
                return [f'<RESP:ACK#ELBOW={mode_str}>']
            case 'GET_ELBOW':
                mode_str = 'LEFT' if self._emulator.get_telemetry().elbow_left else 'RIGHT'
                return [f'<RESP:ELBOW#{mode_str}>']
            case 'JOG':
                return self._handle_jog(parts)
            case _:
                return [f'<RESP:ACK#{op}>']

    def _handle_jog(self, parts: list[str]) -> list[str]:
        '''
            Processes JOG sub-command.

            :param parts: Parameter list.
            :return: List of response strings.
            :exceptions: None.
        '''
        if len(parts) < 3:
            return ['<RESP:NACK#INVALID_JOG>']

        axis: str = parts[1].upper()
        try:
            step: float = float(parts[2])
        except ValueError:
            step = 0.0

        sim_state = self._emulator.get_simulation_state()
        base: ScaraPose = (
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

        target: ScaraPose = ScaraPose(x=new_x, y=new_y, z=new_z, phi=new_phi)
        enqueued: int = self._emulator.enqueue_trajectory([target])
        if enqueued > 0:
            self._planned_pose = target
            return [
                f'<RESP:ACK#JOG_QUEUED#QUEUE={enqueued}>',
                f'<RESP:MOVE_DONE#{new_x:.2f}#{new_y:.2f}#{new_z:.2f}#{new_phi:.2f}>'
            ]
        return ['<RESP:NACK#OUT_OF_BOUNDS>']
