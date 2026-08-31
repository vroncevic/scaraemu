# -*- coding: UTF-8 -*-

'''
Module
    command_templates.py
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
    String formatting templates for firmware commands.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CommandTemplates:
    '''
        String formatting templates for firmware commands.

        It defines:

            :attributes:
                | point_move - Template for Cartesian point movement.
                | cmd_enable - Template for enabling motors.
                | cmd_disable - Template for disabling motors.
                | cmd_estop - Template for emergency stop.
                | cmd_home - Template for homing routine.
                | cmd_get_telem - Template for retrieving telemetry.
                | cmd_getpos - Template for retrieving current position.
                | cmd_status - Template for retrieving device status.
    '''

    point_move: str = '<pt#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}#{speed:.1f}#end>'
    cmd_enable: str = '<CMD:ENABLE>'
    cmd_disable: str = '<CMD:DISABLE>'
    cmd_estop: str = '<CMD:ESTOP>'
    cmd_home: str = '<CMD:HOME>'
    cmd_get_telem: str = '<CMD:GET_TELEM>'
    cmd_getpos: str = '<CMD:GETPOS>'
    cmd_status: str = '<CMD:STATUS>'
