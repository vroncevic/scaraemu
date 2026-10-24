# -*- coding: UTF-8 -*-

'''
Module
    listener_test.py
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
    Unit tests for ConnectionTransportListener.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.bridge.listener.itransport_listener import ITransportListener

from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler
from scaraemu.infrastructure.connection.listener.dependencies import ListenerDependencies
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


class TestConnectionTransportListener(TestCase):
    '''
        Unit test cases for ConnectionTransportListener.

        It defines:

            :methods:
                | test_structural_protocol_conformity - Tests structural conformity to ITransportListener.
                | test_on_bytes_received - Tests forwarding bytes to handler.
                | test_on_log_emitted_regular - Tests regular log emission.
                | test_on_log_emitted_connection_lost - Tests connection lost state synchronization.
                | test_get_version - Tests component version inquiry.
    '''

    def test_structural_protocol_conformity(self) -> None:
        '''
            Tests structural conformity to ITransportListener.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        bundle = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListener(dependencies=bundle)
        self.assertIsInstance(listener, ITransportListener)
        self.assertEqual(listener.get_version(), '1.0.2')

    def test_on_bytes_received(self) -> None:
        '''
            Tests forwarding bytes to handler.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        bundle = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListener(dependencies=bundle)

        test_data = b'TEST_BYTES\x00\x01'
        listener.on_bytes_received(test_data)
        handler.on_bytes.assert_called_once_with(test_data)

    def test_on_log_emitted_regular(self) -> None:
        '''
            Tests regular log emission.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        bundle = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListener(dependencies=bundle)

        listener.on_log_emitted('Connected successfully', is_tx=False)
        handler.on_log.assert_called_once_with('Connected successfully')
        synchronizer.on_state_change.assert_not_called()

    def test_on_log_emitted_connection_lost(self) -> None:
        '''
            Tests connection lost state synchronization.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        bundle = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListener(dependencies=bundle)

        lost_msg = '[HOST]: Connection lost (device disconnected / unplugged)'
        listener.on_log_emitted(lost_msg, is_tx=False)
        handler.on_log.assert_called_once_with(lost_msg)
        synchronizer.on_state_change.assert_called_once_with(False)

    def test_get_version(self) -> None:
        '''
            Tests component version inquiry.
        '''
        handler = MagicMock(spec=IResponseHandler)
        synchronizer = MagicMock(spec=IBridgeSynchronizer)
        bundle = ListenerDependencies(
            handler=handler,
            synchronizer=synchronizer,
        )
        listener = ConnectionTransportListener(dependencies=bundle)
        self.assertEqual(listener.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
