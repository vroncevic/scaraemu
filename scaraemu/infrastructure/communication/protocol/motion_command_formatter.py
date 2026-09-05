# -*- coding: UTF-8 -*-

'''
Module
    motion_command_formatter.py
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
    Motion and runtime command packet encoder for SCARA microcontroller.
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
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandFormatter:
    '''
        Serial packet encoder formatting motion and runtime control commands.

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
                | format_hold - Formats feed-hold pause command.
                | format_resume - Formats motion resume command.
                | format_set_elbow - Formats set elbow configuration command.
                | format_get_elbow - Formats get elbow configuration command.
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

    @classmethod
    def format_hold(cls) -> str:
        '''
            Formats feed-hold pause command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_hold

    @classmethod
    def format_resume(cls) -> str:
        '''
            Formats motion resume command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_resume

    @classmethod
    def format_set_elbow(cls, elbow_left: bool) -> str:
        '''
            Formats set elbow configuration command.

            :param elbow_left: True for Lefty, False for Righty.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        name: str = 'LEFT' if elbow_left else 'RIGHT'
        return cls.TEMPLATES.cmd_set_elbow.format(elbow=name)

    @classmethod
    def format_get_elbow(cls) -> str:
        '''
            Formats get elbow configuration command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_get_elbow
