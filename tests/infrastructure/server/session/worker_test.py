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
    Unit tests for ClientSessionWorker.
'''

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket as Socket, timeout as SocketTimeout
from threading import Event, Thread
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.server.session.outbound_queue import OutboundFrameQueue
from scaraemu.infrastructure.server.session.worker import ClientSessionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _EchoDispatcher:
    '''
        Dummy dispatcher for testing.

        It defines:

            :attributes:
                | outbound_queue - Optional outbound frame queue.
            :methods:
                | __init__ - Initializes dispatcher.
                | dispatch_binary - Tests dispatch binary.
                | reset - Tests reset.
                | get_version - Tests get version.
    '''

    outbound_queue: OutboundFrameQueue | None

    def __init__(self, outbound_queue: OutboundFrameQueue | None = None) -> None:
        '''
            Initializes mock dispatcher.

            :param outbound_queue: Optional outbound queue.
            :exceptions: None.
        '''
        self.outbound_queue = outbound_queue

    def dispatch_binary(self, data: bytes) -> tuple[bytes, ...]:
        '''
            Tests dispatch binary.

            :param data: Input data.
            :return: Response tuple.
            :exceptions: None.
        '''
        _ = data
        if self.outbound_queue is not None:
            self.outbound_queue.push(b'<ASYNC_EVENT>\n')
        return (b'<BIN_ACK>\n',)

    def reset(self) -> None:
        '''
            Tests reset.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockServerLogListener:
    '''
        Mock server log listener for testing.
    '''

    def on_server_log(self, message: str) -> None:
        '''
            Tests on server log.

            :param message: Input message.
            :exceptions: None.
        '''
        _ = message

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestClientSessionWorker(TestCase):
    '''
        Test cases verifying ClientSessionWorker client communication.

        It defines:

            :methods:
                | test_handle_client_binary - Verifies handling binary frames.
                | test_handle_client_timeout_and_exceptions - Verifies timeout/errors.
                | test_get_version - Verifies version string.
    '''

    def test_handle_client_binary(self) -> None:
        '''
            Verifies handling binary frames over connected socket pair.

            :exceptions: None.
        '''
        listener_sock = Socket(AF_INET, SOCK_STREAM)
        listener_sock.bind(('127.0.0.1', 0))
        listener_sock.listen(1)
        port: int = listener_sock.getsockname()[1]

        client_sock = Socket(AF_INET, SOCK_STREAM)
        client_sock.connect(('127.0.0.1', port))

        server_side_sock, _ = listener_sock.accept()
        listener_sock.close()

        dispatcher = _EchoDispatcher()
        outbound_queue = OutboundFrameQueue()
        worker = ClientSessionWorker(
            dispatcher=dispatcher,
            log_listener=_MockServerLogListener(),
            outbound_queue=outbound_queue,
        )

        stop_event = Event()
        worker_thread = Thread(
            target=worker.handle_client,
            kwargs={
                'client_sock': server_side_sock,
                'stop_event': stop_event,
            },
            daemon=True,
        )
        try:
            worker_thread.start()
            client_sock.sendall(b'\xaa\x55ping')
            resp = client_sock.recv(1024)
            self.assertEqual(resp, b'<BIN_ACK>\n')

            outbound_queue.push(b'<ASYNC_EVENT>\n')
            async_resp = client_sock.recv(1024)
            self.assertEqual(async_resp, b'<ASYNC_EVENT>\n')
        finally:
            stop_event.set()
            client_sock.close()
            worker_thread.join(timeout=1.0)
            try:
                server_side_sock.close()
            except OSError:
                pass

    def test_handle_client_timeout_and_exceptions(self) -> None:
        '''
            Verifies handling client socket timeout and OS exceptions.

            :exceptions: None.
        '''
        mock_sock = MagicMock()
        mock_sock.recv.side_effect = [SocketTimeout(), b'test_data', b'']
        mock_sock.close.side_effect = OSError('close failure')
        stop_event = Event()

        outbound_queue = OutboundFrameQueue()
        worker = ClientSessionWorker(
            dispatcher=_EchoDispatcher(outbound_queue=outbound_queue),
            log_listener=_MockServerLogListener(),
            outbound_queue=outbound_queue,
        )
        worker.handle_client(client_sock=mock_sock, stop_event=stop_event)
        mock_sock.sendall.assert_any_call(b'<ASYNC_EVENT>\n')

        mock_sock_err = MagicMock()
        mock_sock_err.recv.side_effect = OSError('connection reset')
        worker.handle_client(client_sock=mock_sock_err, stop_event=stop_event)

    def test_get_version(self) -> None:
        '''
            Verifies version string.

            :exceptions: None.
        '''
        worker = ClientSessionWorker(
            dispatcher=_EchoDispatcher(),
            log_listener=_MockServerLogListener(),
            outbound_queue=OutboundFrameQueue(),
        )
        self.assertEqual(worker.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
