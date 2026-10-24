# -*- coding: UTF-8 -*-

'''
Module
    iadapter.py
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
    Structural protocol defining adapter port for script loading and compilation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScriptLoaderAdapter(Protocol):
    '''
        Structural protocol defining adapter port for script loading and compilation.

        It defines:

            :methods:
                | load_from_text - Compiles DSL text into Cartesian poses.
                | load_from_file - Reads file and parses into Cartesian poses.
                | get_version - Returns adapter version string.
    '''

    def load_from_text(self, source: str) -> list[ScaraPose]:
        '''
            Compiles DSL source script text into a sequence of Cartesian poses.

            :param source: Raw script text content.
            :return: List of Cartesian poses for trajectory execution.
            :exceptions: None.
        '''

    def load_from_file(self, filepath: str) -> list[ScaraPose]:
        '''
            Reads DSL script file and compiles into Cartesian poses.

            :param filepath: Path to SCARA script file on disk.
            :return: List of Cartesian poses for trajectory execution.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
