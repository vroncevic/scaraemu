# -*- coding: UTF-8 -*-

'''
Module
    iscara_script_loader.py
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
    Interface protocol for parsing and loading .scara DSL scripts into emulator poses.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraScriptLoader(Protocol):
    '''
        Protocol defining operations for converting .scara scripts or plans into ScaraPose trajectories.

        It defines:

            :methods:
                | load_from_file - Reads and parses script or plan from filesystem.
                | parse_script - Parses raw script text content into sequence of poses.
    '''

    def load_from_file(self, *, filepath: str) -> list[ScaraPose]:
        '''
            Reads and parses a script or plan file from the filesystem.

            :param filepath: Path to .scara or .json trajectory plan file.
            :return: List of ScaraPose waypoints.
            :exceptions: OSError, ValueError.
        '''

    def parse_script(self, *, source: str) -> list[ScaraPose]:
        '''
            Parses raw script text content into sequence of ScaraPose waypoints.

            :param source: SCARA DSL source text.
            :return: List of ScaraPose waypoints.
            :exceptions: ValueError.
        '''
