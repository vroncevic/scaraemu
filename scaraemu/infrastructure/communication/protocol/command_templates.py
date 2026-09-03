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
__version__ = '1.0.1'
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
                | cmd_hold - Template for feed-hold pause command.
                | cmd_resume - Template for motion resume command.
    '''

    point_move: str = '<pt#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}#{speed:.1f}#end>'
    cmd_enable: str = '<CMD:ENABLE>'
    cmd_disable: str = '<CMD:DISABLE>'
    cmd_estop: str = '<CMD:ESTOP>'
    cmd_home: str = '<CMD:HOME>'
    cmd_get_telem: str = '<CMD:GET_TELEM>'
    cmd_getpos: str = '<CMD:GETPOS>'
    cmd_status: str = '<CMD:STATUS>'
    cmd_hold: str = '<CMD:HOLD>'
    cmd_resume: str = '<CMD:RESUME>'
    cmd_get_config: str = '<CMD:GET_CONFIG>'
    cmd_save_config: str = '<CMD:SAVE_CONFIG>'
    cmd_set_config: str = (
        '<CMD:SET_CONFIG#L1={l1:.2f}#L2={l2:.2f}#Z_MIN={z_min:.2f}'
        '#Z_MAX={z_max:.2f}#MIN_SPD={min_speed:.2f}#MAX_SPD={max_speed:.2f}>'
    )
    cmd_set_dynamics: str = '<CMD:SET_DYNAMICS#ACCEL={accel:.2f}#MAX_ACCEL={max_accel:.2f}#DEF_SPD={def_speed:.2f}>'
    cmd_set_homing: str = '<CMD:SET_HOMING#OFF_J1={off_j1:.4f}#OFF_J2={off_j2:.4f}#RATE={rate:d}>'
    cmd_set_limits: str = '<CMD:SET_LIMITS#J1_MIN={j1_min:.4f}#J1_MAX={j1_max:.4f}#J2_MIN={j2_min:.4f}#J2_MAX={j2_max:.4f}>'
    cmd_set_steps: str = '<CMD:SET_STEPS#GR_J1={gr_j1:.2f}#GR_J2={gr_j2:.2f}#GR_J4={gr_j4:.2f}#LEAD_Z={lead_z:.2f}>'
    cmd_set_elbow: str = '<CMD:SET_ELBOW#{elbow}>'
    cmd_get_elbow: str = '<CMD:GET_ELBOW>'

