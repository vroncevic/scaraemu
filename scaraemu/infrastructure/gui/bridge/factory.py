# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory creating and configuring GUI presentation and logging bridge adapters.
'''

from __future__ import annotations

from scaraemu.infrastructure.gui.bridge.log.adapter import LogAdapter
from scaraemu.infrastructure.gui.bridge.provides import BridgeProvides
from scaraemu.infrastructure.gui.bridge.server.log_adapter import ServerLogAdapter
from scaraemu.infrastructure.gui.bridge.server.state_adapter import ServerAdapter
from scaraemu.infrastructure.gui.bridge.status.adapter import StatusAdapter
from scaraemu.infrastructure.gui.bridge.sync.synchronizer import BridgeSynchronizer
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.server.logger.iholder import IServerLogListenerHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BridgeFactory:
    '''
        Factory creating and configuring GUI presentation and logging bridge adapters.

        It defines:

            :methods:
                | create - Instantiates GUI bridge adapters and connects server log listener.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        layout_builder: ILayoutBuilder,
        server_log_holder: IServerLogListenerHolder,
    ) -> BridgeProvides:
        '''
            Instantiates GUI bridge adapters and connects server log listener.

            :param layout_builder: Root GUI layout builder.
            :param server_log_holder: Virtual server log listener registry.
            :return: Wired GUI bridge bundle.
            :exceptions: None.
        '''
        log_listener: LogAdapter = LogAdapter(layout_builder=layout_builder)
        status_view: StatusAdapter = StatusAdapter(
            layout_builder=layout_builder
        )
        server_state_listener: ServerAdapter = ServerAdapter(
            layout_builder=layout_builder
        )
        server_log_listener: ServerLogAdapter = ServerLogAdapter(
            log_listener=log_listener
        )
        server_log_holder.set_listener(server_log_listener)
        bridge_synchronizer: BridgeSynchronizer = BridgeSynchronizer(
            status_view=status_view
        )

        return BridgeProvides(
            log_listener=log_listener,
            status_view=status_view,
            server_state_listener=server_state_listener,
            server_log_listener=server_log_listener,
            bridge_synchronizer=bridge_synchronizer,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
