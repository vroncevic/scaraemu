# -*- coding: UTF-8 -*-

'''
Module
    options.py
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
    SCARAEmu bundle options TypedDict definition.
'''

from __future__ import annotations

from typing import TypedDict

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAEmuBundleOptions(TypedDict, total=False):
    '''
        SCARAEmu bundle options specification.

        It defines:

            :attributes:
                | info_file - The path to the ats configuration file.
                | robot_config - Path to custom robot kinematics configuration file.
                | l1 - Primary SCARA link length in mm.
                | l2 - Secondary SCARA link length in mm.
                | z_min - Minimum vertical height limit in mm.
                | z_max - Maximum vertical height limit in mm.
                | min_speed - Minimum feedrate speed limit in mm/s.
                | max_speed - Maximum feedrate speed limit in mm/s.
                | serial_port - Default USB serial port device.
                | baud_rate - Serial port communication speed.
                | file_path - Optional initial plan file path.
    '''

    info_file: str
    robot_config: str
    l1: float
    l2: float
    z_min: float
    z_max: float
    min_speed: float
    max_speed: float
    serial_port: str
    baud_rate: int
    file_path: str
