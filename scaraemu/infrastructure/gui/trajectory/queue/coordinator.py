# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Action coordinator handling motion queue clearing across domain and bridge.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueActionCoordinator:
    '''
        Coordinates motion queue clearing across digital twin and hardware bridge.

        It defines:

            :attributes:
                | _command_port - Hardware command communication port.
                | _emulation_queue - FIFO motion emulation queue.
                | _emulation_service - Core emulation service for visual trail clearing.
            :methods:
                | __init__ - Initializes queue action coordinator with collaborators.
                | handle_clear_queue - Flushes motion queues across emulator and bridge.
                | handle_clear_trail - Clears historical motion trail coordinates.
                | get_version - Returns coordinator component version.
    '''

    _command_port: ICommandDispatcher
    _emulation_queue: IEmulationQueue
    _emulation_service: IEmulationService

    def __init__(
        self,
        *,
        command_port: ICommandDispatcher,
        emulation_queue: IEmulationQueue,
        emulation_service: IEmulationService,
    ) -> None:
        '''
            Initializes queue action coordinator with collaborators.

            :param command_port: Hardware command communication port.
            :param emulation_queue: FIFO motion emulation queue.
            :param emulation_service: Core emulation service port.
            :exceptions: None.
        '''
        self._command_port: Final[ICommandDispatcher] = command_port
        self._emulation_queue: Final[IEmulationQueue] = emulation_queue
        self._emulation_service: Final[IEmulationService] = emulation_service

    def handle_clear_queue(self) -> None:
        '''
            Flushes motion queues across emulator and bridge.

            :exceptions: None.
        '''
        self._emulation_queue.clear_queue()
        self._command_port.clear_queue()

    def handle_clear_trail(self) -> None:
        '''
            Clears historical motion trail coordinates.

            :exceptions: None.
        '''
        self._emulation_service.clear_trail()

    def get_version(self) -> str:
        '''
            Returns coordinator component version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
