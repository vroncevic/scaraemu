# -*- coding: UTF-8 -*-

'''
Module
    command_formatter.py
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
    Serial packet encoder and command formatter for SCARA microcontroller.
'''

from __future__ import annotations

from typing import ClassVar

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.protocol.command_templates import (
    CommandTemplates
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFormatter:
    '''
        Serial packet encoder formatting commands for microcontroller firmware.

        It defines:

            :attributes:
                | TEMPLATES - Protocol command template configurations.
            :methods:
                | format_move_pose - Formats Cartesian target point packet.
                | format_enable_motors - Formats motor power enable command.
                | format_disable_motors - Formats motor power disable command.
                | format_estop - Formats emergency stop command.
                | format_home - Formats homing routine command.
                | format_get_telemetry - Formats telemetry query command.
                | format_get_position - Formats position query command.
                | format_get_status - Formats status query command.
    '''

    TEMPLATES: ClassVar[CommandTemplates] = CommandTemplates()

    @classmethod
    def format_move_pose(cls, pose: ScaraPose, speed: float = 30.0) -> str:
        '''
            Formats Cartesian target point packet.

            :param pose: Target ScaraPose.
            :param speed: Feedrate speed in mm/s.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.point_move.format(
            x=pose.x,
            y=pose.y,
            z=pose.z,
            phi=pose.phi,
            speed=speed
        )

    @classmethod
    def format_enable_motors(cls) -> str:
        '''
            Formats motor power enable command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_enable

    @classmethod
    def format_disable_motors(cls) -> str:
        '''
            Formats motor power disable command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_disable

    @classmethod
    def format_estop(cls) -> str:
        '''
            Formats emergency stop command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_estop

    @classmethod
    def format_home(cls) -> str:
        '''
            Formats homing routine command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_home

    @classmethod
    def format_get_telemetry(cls) -> str:
        '''
            Formats telemetry query command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_get_telem

    @classmethod
    def format_get_position(cls) -> str:
        '''
            Formats position query command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_getpos

    @classmethod
    def format_get_status(cls) -> str:
        '''
            Formats status query command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_status
