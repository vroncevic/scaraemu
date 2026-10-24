# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ServerAcceptWorkerFactory implementation.
'''

from __future__ import annotations

from socket import socket as Socket
from threading import Event
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.accept.factory import ServerAcceptWorkerFactory
from scaraemu.infrastructure.server.accept.worker import ServerAcceptWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockSessionWorker:
    '''Mock session worker.'''

    def handle_client(self, *, client_sock: Socket, stop_event: Event) -> None:
        '''Handles client.'''
        _ = (client_sock, stop_event)

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class _MockServerLogListener:
    '''Mock server log listener.'''

    def on_server_log(self, message: str) -> None:
        '''Handles server log.'''
        _ = message

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.2'


class TestServerAcceptWorkerFactory(TestCase):
    '''
        Unit tests for ServerAcceptWorkerFactory.

        It defines:

            :methods:
                | test_create - Tests instantiating ServerAcceptWorker.
                | test_get_version - Tests component version retrieval.
    '''

    def test_create(self) -> None:
        '''
            Tests instantiating ServerAcceptWorker.

            :exceptions: None.
        '''
        worker = ServerAcceptWorkerFactory.create(
            session_worker=_MockSessionWorker(),
            log_listener=_MockServerLogListener(),
        )
        self.assertIsInstance(worker, ServerAcceptWorker)

    def test_get_version(self) -> None:
        '''
            Tests component version retrieval.

            :exceptions: None.
        '''
        version = ServerAcceptWorkerFactory.get_version()
        self.assertIsInstance(version, str)


if __name__ == '__main__':
    unittest_main()
