# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Provides dataclass encapsulating GUI view and logger bridge ports.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.gui.toolbar.connection.istatus_view import IConnectionStatusView
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.manager.ilistener import IServerStateListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class BridgeProvides:
    '''
        Provides dataclass encapsulating GUI view and logger bridge ports.

        It defines:

            :attributes:
                | log_listener - Console logging sink listener.
                | status_view - Toolbar connection and motion state status view.
                | server_state_listener - Toolbar virtual server toggle indicator listener.
                | server_log_listener - Virtual server diagnostics logging sink listener.
                | bridge_synchronizer - Hardware bridge status and telemetry synchronizer adapter.
    '''

    log_listener: ILogListener
    status_view: IConnectionStatusView
    server_state_listener: IServerStateListener
    server_log_listener: IServerLogListener
    bridge_synchronizer: IBridgeSynchronizer
