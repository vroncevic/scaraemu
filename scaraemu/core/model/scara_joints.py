# -*- coding: UTF-8 -*-

'''
Module
    scara_joints.py
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
    Defines SCARA articulated joint angles and linear positions.
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
class ScaraJoints:
    '''
        SCARA joint positions and reachability status.

        It defines:

            :attributes:
                | theta1 - Shoulder joint angle in radians.
                | theta2 - Elbow joint angle in radians.
                | z - Vertical carriage displacement in mm.
                | theta4 - Wrist tool orientation in radians.
                | reachable - Reachability boundary compliance flag.
    '''

    theta1: float
    theta2: float
    z: float
    theta4: float
    reachable: bool = True
