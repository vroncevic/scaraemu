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
    Unit tests for ClientSessionWorkerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.session.dependencies import SessionDependencies
from scaraemu.infrastructure.server.session.factory import ClientSessionWorkerFactory
from scaraemu.infrastructure.server.session.outbound_queue import OutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyDispatcher:
    '''
        Dummy dispatcher for testing.
    '''

    def dispatch_binary(self, data: bytes) -> tuple[bytes, ...]:
        '''
            Tests dispatch binary.

            :param data: Input data.
            :return: Response tuple.
            :exceptions: None.
        '''
        return ()

    def reset(self) -> None:
        '''
            Tests reset.

            :exceptions: None.
        '''
        pass

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _DummyServerLogListener:
    '''
        Dummy server log listener for testing.
    '''

    def on_server_log(self, message: str) -> None:
        '''
            Tests on server log.

            :param message: Input message.
            :exceptions: None.
        '''
        pass

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestClientSessionWorkerFactory(TestCase):
    '''
        Test cases verifying ClientSessionWorkerFactory creation.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates ClientSessionWorker.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory instantiates ClientSessionWorker.

            :exceptions: None.
        '''
        dependencies = SessionDependencies(
            dispatcher=_DummyDispatcher(),
            log_listener=_DummyServerLogListener(),
            outbound_queue=OutboundFrameQueue(),
        )
        worker = ClientSessionWorkerFactory.create(dependencies)
        self.assertIsNotNone(worker)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(ClientSessionWorkerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
