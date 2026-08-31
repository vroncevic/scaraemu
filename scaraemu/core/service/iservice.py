# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines interface IService for SCARA domain service facade.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.service.ikinematics_service import IKinematicsService
from scaraemu.core.service.iemulator_service import IEmulatorService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IService(Protocol):
    '''
        Interface for orchestrating SCARA kinematics and emulation services.

        It defines:

            :methods:
                | is_initialized - Checks if all sub-services are initialized.
                | get_kinematics - Returns active IKinematicsService.
                | get_emulator - Returns active IEmulatorService.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if all sub-services are initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''

    def get_kinematics(self) -> IKinematicsService:
        '''
            Returns active IKinematicsService.

            :return: IKinematicsService instance.
            :exceptions: None.
        '''

    def get_emulator(self) -> IEmulatorService:
        '''
            Returns active IEmulatorService.

            :return: IEmulatorService instance.
            :exceptions: None.
        '''
