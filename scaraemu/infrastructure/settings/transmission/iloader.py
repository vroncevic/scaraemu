# -*- coding: UTF-8 -*-

'''
Module
    iloader.py
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
    Interface protocol for robot transmission configuration loader.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITransmissionLoader(Protocol):
    '''
        Interface protocol for transmission configuration loader.

        It defines:

            :methods:
                | load_transmission - Loads validated transmission parameters from configuration.
                | get_version - Returns loader interface version string.
    '''

    def load_transmission(
        self,
        *,
        config_path: str,
        scheme_path: str,
    ) -> TransmissionParameters:
        '''
            Loads validated transmission parameters from configuration files.

            :param config_path: Path to robot geometry JSON configuration file.
            :param scheme_path: Path to JSON validation scheme file.
            :return: TransmissionParameters value object.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns loader interface version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
