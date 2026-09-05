# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Concrete facade implementation of IService.
'''

from __future__ import annotations

from scaraemu.core.service.ikinematics_service import IKinematicsService
from scaraemu.core.service.iemulator_service import IEmulatorService
from scaraemu.core.service.iservice import IService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Service(IService):
    '''
        Service facade orchestrating kinematics and emulation services.

        It defines:

            :attributes:
                | _kinematics - Injected IKinematicsService.
                | _emulator - Injected IEmulatorService.
            :methods:
                | __init__ - Initializes the service facade.
                | is_initialized - Checks initialization status of sub-services.
                | get_kinematics - Returns IKinematicsService.
                | get_emulator - Returns IEmulatorService.
    '''

    _kinematics: IKinematicsService
    _emulator: IEmulatorService

    def __init__(
        self,
        kinematics: IKinematicsService,
        emulator: IEmulatorService
    ) -> None:
        '''
            Initializes the service facade.

            :param kinematics: Kinematics solver service instance.
            :param emulator: Emulator simulation service instance.
            :exceptions: None.
        '''
        self._kinematics = kinematics
        self._emulator = emulator

    def is_initialized(self) -> bool:
        '''
            Checks if all sub-services are initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return bool(self._kinematics and self._emulator)

    def get_kinematics(self) -> IKinematicsService:
        '''
            Returns active IKinematicsService.

            :return: IKinematicsService instance.
            :exceptions: None.
        '''
        return self._kinematics

    def get_emulator(self) -> IEmulatorService:
        '''
            Returns active IEmulatorService.

            :return: IEmulatorService instance.
            :exceptions: None.
        '''
        return self._emulator
