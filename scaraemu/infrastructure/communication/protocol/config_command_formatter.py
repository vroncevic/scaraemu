# -*- coding: UTF-8 -*-

'''
Module
    config_command_formatter.py
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
    Configuration and calibration command packet encoder for SCARA microcontroller.
'''

from __future__ import annotations

from typing import ClassVar

from scaraemu.infrastructure.communication.protocol.command_templates import (
    CommandTemplates
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigCommandFormatter:
    '''
        Serial packet encoder formatting configuration and calibration commands.

        It defines:

            :attributes:
                | TEMPLATES - Protocol command template configurations.
            :methods:
                | format_get_config - Formats configuration query command.
                | format_save_config - Formats configuration Flash save command.
                | format_reset_config - Formats configuration factory reset command.
                | format_set_config - Formats basic geometry and speed limits command.
                | format_set_dynamics - Formats motion dynamics configuration command.
                | format_set_homing - Formats homing offsets and step pulse rate command.
                | format_set_limits - Formats joint angle limits command.
                | format_set_steps - Formats mechanical transmission gear ratios command.
    '''

    TEMPLATES: ClassVar[CommandTemplates] = CommandTemplates()

    @classmethod
    def format_get_config(cls) -> str:
        '''
            Formats configuration query command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_get_config

    @classmethod
    def format_save_config(cls) -> str:
        '''
            Formats configuration Flash save command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_save_config

    @classmethod
    def format_reset_config(cls) -> str:
        '''
            Formats configuration factory reset command.

            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_reset_config

    @classmethod
    def format_set_config(
        cls, l1: float, l2: float, z_min: float, z_max: float, min_speed: float, max_speed: float
    ) -> str:
        '''
            Formats basic geometry and speed limits command.

            :param l1: Inner arm length in mm.
            :param l2: Outer arm length in mm.
            :param z_min: Minimum Z in mm.
            :param z_max: Maximum Z in mm.
            :param min_speed: Minimum speed in mm/s.
            :param max_speed: Maximum speed in mm/s.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_set_config.format(
            l1=l1, l2=l2, z_min=z_min, z_max=z_max, min_speed=min_speed, max_speed=max_speed
        )

    @classmethod
    def format_set_dynamics(cls, accel: float, max_accel: float, def_speed: float) -> str:
        '''
            Formats motion dynamics configuration command.

            :param accel: Default acceleration in mm/s^2.
            :param max_accel: Maximum acceleration in mm/s^2.
            :param def_speed: Default speed in mm/s.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_set_dynamics.format(
            accel=accel, max_accel=max_accel, def_speed=def_speed
        )

    @classmethod
    def format_set_homing(cls, off_j1: float, off_j2: float, rate: int) -> str:
        '''
            Formats homing offsets and step pulse rate command.

            :param off_j1: J1 home offset in radians.
            :param off_j2: J2 home offset in radians.
            :param rate: Step pulse rate during homing in Hz.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_set_homing.format(
            off_j1=off_j1, off_j2=off_j2, rate=rate
        )

    @classmethod
    def format_set_limits(cls, j1_min: float, j1_max: float, j2_min: float, j2_max: float) -> str:
        '''
            Formats joint angle limits command.

            :param j1_min: J1 minimum angle in radians.
            :param j1_max: J1 maximum angle in radians.
            :param j2_min: J2 minimum angle in radians.
            :param j2_max: J2 maximum angle in radians.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_set_limits.format(
            j1_min=j1_min, j1_max=j1_max, j2_min=j2_min, j2_max=j2_max
        )

    @classmethod
    def format_set_steps(cls, gr_j1: float, gr_j2: float, gr_j4: float, lead_z: float) -> str:
        '''
            Formats mechanical transmission gear ratio and leadscrew pitch command.

            :param gr_j1: Joint 1 gear ratio.
            :param gr_j2: Joint 2 gear ratio.
            :param gr_j4: Joint 4 gear ratio.
            :param lead_z: Z leadscrew pitch in mm/rev.
            :return: Encoded protocol string.
            :exceptions: None.
        '''
        return cls.TEMPLATES.cmd_set_steps.format(
            gr_j1=gr_j1, gr_j2=gr_j2, gr_j4=gr_j4, lead_z=lead_z
        )
