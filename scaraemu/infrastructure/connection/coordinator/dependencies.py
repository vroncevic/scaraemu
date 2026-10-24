# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Dependencies dataclass for ConnectionCoordinator instantiation.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator

from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CoordinatorDependencies:
    '''
        Encapsulates required dependencies for ConnectionCoordinator instantiation.

        :param connection: Injected hardware communication connection coordinator.
        :param listener: Hardware bridge status and telemetry synchronizer.
        :param streamer: Trajectory queue streamer managing flow control.
        :param command_dispatcher: Injected hardware command dispatcher.
    '''

    connection: IConnectionCoordinator
    listener: IBridgeSynchronizer
    streamer: IQueueStreamer
    command_dispatcher: ICommandDispatcher
