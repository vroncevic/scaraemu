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
    Parameter bundle dataclass encapsulating dependencies for ClientSessionWorker.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.infrastructure.server.dispatcher.idispatcher import IServerFrameDispatcher
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.session.ioutbound_queue import IOutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class SessionDependencies:
    '''
        Parameter bundle dataclass encapsulating dependencies for ClientSessionWorker.

        It defines:

            :attributes:
                | dispatcher - Frame and command processing dispatcher.
                | log_listener - Server event log listener.
                | outbound_queue - Outbound frame queue for asynchronous event streaming.
    '''

    dispatcher: IServerFrameDispatcher
    log_listener: IServerLogListener
    outbound_queue: IOutboundFrameQueue
