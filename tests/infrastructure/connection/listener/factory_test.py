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
    Unit test cases for ConnectionTransportListenerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.bridge.listener.itransport_listener import ITransportListener

from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler
from scaraemu.infrastructure.connection.listener.dependencies import ListenerDependencies
from scaraemu.infrastructure.connection.listener.factory import ConnectionTransportListenerFactory
from scaraemu.infrastructure.connection.listener.listener import ConnectionTransportListener
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionTransportListenerFactoryTestCase(TestCase):
    '''
        Test cases verifying ConnectionTransportListenerFactory behavior.

        It defines:

            :methods:
                | test_create - Tests factory create instantiating ConnectionTransportListener.
                | test_get_version - Tests factory version inquiry.
    '''

    def test_create(self) -> None:
        '''
            Tests factory create instantiating ConnectionTransportListener.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        deps = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListenerFactory.create(dependencies=deps)
        self.assertIsInstance(listener, ConnectionTransportListener)
        self.assertIsInstance(listener, ITransportListener)
        self.assertEqual(listener.get_version(), '1.0.2')

    def test_get_version(self) -> None:
        '''
            Tests factory version inquiry.
        '''
        self.assertEqual(ConnectionTransportListenerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
