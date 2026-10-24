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
    Factory constructing ClientSessionWorker instances.
'''

from __future__ import annotations

from scaraemu.infrastructure.server.session.dependencies import SessionDependencies
from scaraemu.infrastructure.server.session.worker import ClientSessionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ClientSessionWorkerFactory:
    '''
        Factory constructing ClientSessionWorker instances.

        It defines:

            :methods:
                | create - Instantiates ClientSessionWorker with session dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: SessionDependencies,
    ) -> ClientSessionWorker:
        '''
            Instantiates ClientSessionWorker with session dependencies.

            :param dependencies: Encapsulated SessionDependencies parameter bundle.
            :return: Configured ClientSessionWorker instance.
            :exceptions: None.
        '''
        return ClientSessionWorker(
            dispatcher=dependencies.dispatcher,
            log_listener=dependencies.log_listener,
            outbound_queue=dependencies.outbound_queue,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
