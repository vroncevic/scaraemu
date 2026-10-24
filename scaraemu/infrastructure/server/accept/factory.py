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
    Factory constructing ServerAcceptWorker instances.
'''

from __future__ import annotations

from scaraemu.infrastructure.server.accept.worker import ServerAcceptWorker
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.session.iworker import IClientSessionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServerAcceptWorkerFactory:
    '''
        Factory constructing ServerAcceptWorker instances.

        It defines:

            :methods:
                | create - Instantiates ServerAcceptWorker with session worker and log listener.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        session_worker: IClientSessionWorker,
        log_listener: IServerLogListener,
    ) -> ServerAcceptWorker:
        '''
            Instantiates ServerAcceptWorker with session worker and log listener.

            :param session_worker: Injected IClientSessionWorker instance.
            :param log_listener: Injected IServerLogListener instance.
            :return: Configured ServerAcceptWorker instance.
            :exceptions: None.
        '''
        return ServerAcceptWorker(session_worker=session_worker, log_listener=log_listener)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
