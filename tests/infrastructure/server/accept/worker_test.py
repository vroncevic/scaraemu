# -*- coding: UTF-8 -*-

'''
Module
    worker_test.py
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
    Unit tests for ServerAcceptWorker implementation.
'''

from __future__ import annotations

from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket as Socket
from socket import timeout as SocketTimeout
from threading import Event
from threading import Thread
from time import sleep
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

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
    '''
        Mock session worker for test assertions.
    '''

    def __init__(self) -> None:
        self.handled = False

    def handle_client(
        self,
        *,
        client_sock: Socket,
        stop_event: Event,
    ) -> None:
        '''Handles client connection.'''
        _ = stop_event
        self.handled = True
        try:
            client_sock.close()
        except OSError:
            pass

    def get_version(self) -> str:
        '''Returns mock version string.'''
        return '1.0.2'


class _MockServerLogListener:
    '''
        Mock server log listener for testing.
    '''

    def on_server_log(self, message: str) -> None:
        '''Handles server log message.'''
        _ = message

    def get_version(self) -> str:
        '''Returns mock version string.'''
        return '1.0.2'


class TestServerAcceptWorker(TestCase):
    '''
        Test cases verifying ServerAcceptWorker connection lifecycle.

        It defines:

            :methods:
                | test_accept_flow - Verifies socket accept loop.
                | test_accept_timeout - Verifies timeout handling.
                | test_get_version - Verifies component version string.
    '''

    def test_accept_flow(self) -> None:
        '''
            Verifies socket accept loop.

            :exceptions: None.
        '''
        server_sock = Socket(AF_INET, SOCK_STREAM)
        server_sock.bind(('127.0.0.1', 0))
        server_sock.listen(1)
        server_sock.settimeout(0.2)
        port: int = server_sock.getsockname()[1]

        session_worker = _MockSessionWorker()
        stop_event = Event()
        worker = ServerAcceptWorker(
            session_worker=session_worker,
            log_listener=_MockServerLogListener(),
        )

        accept_thread = Thread(
            target=worker.run,
            kwargs={'server_socket': server_sock, 'stop_event': stop_event},
            daemon=True,
        )
        accept_thread.start()

        client_sock = Socket(AF_INET, SOCK_STREAM)
        client_sock.connect(('127.0.0.1', port))

        for _ in range(20):
            if session_worker.handled:
                break
            sleep(0.05)

        stop_event.set()
        client_sock.close()
        server_sock.close()
        accept_thread.join(timeout=1.0)
        self.assertTrue(session_worker.handled)

    def test_accept_timeout(self) -> None:
        '''
            Verifies accept loop continues on SocketTimeout until stop event.

            :exceptions: None.
        '''
        mock_sock = MagicMock()
        stop_event = Event()

        def _timeout_once() -> tuple[MagicMock, tuple[str, int]]:
            stop_event.set()
            raise SocketTimeout()

        mock_sock.accept.side_effect = _timeout_once
        worker = ServerAcceptWorker(
            session_worker=_MockSessionWorker(),
            log_listener=_MockServerLogListener(),
        )
        worker.run(server_socket=mock_sock, stop_event=stop_event)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        worker = ServerAcceptWorker(
            session_worker=_MockSessionWorker(),
            log_listener=_MockServerLogListener(),
        )
        self.assertEqual(worker.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
