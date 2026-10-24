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
    Unit test cases for ConnectionFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.transport.itransport import ITransport

from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.connection.dependencies import ConnectionDependencies
from scaraemu.infrastructure.connection.factory import ConnectionFactory
from scaraemu.infrastructure.connection.provides import ConnectionProvides
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionFactoryTestCase(TestCase):
    '''
        Unit test cases verifying ConnectionFactory behavior.

        It defines:

            :methods:
                | test_create - Tests factory create instantiating ConnectionProvides.
                | test_get_version - Tests factory version inquiry.
    '''

    def test_create(self) -> None:
        '''
            Tests factory create instantiating ConnectionProvides.
        '''
        mock_transport = MagicMock(spec=ITransport)
        mock_bridge_synchronizer = MagicMock(spec=IBridgeSynchronizer)
        mock_log = MagicMock(spec=ILogListener)
        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        mock_decoder = MagicMock(spec=IBinaryResponseDecoderAdapter)
        mock_kinematics = MagicMock(spec=IManipulatorKinematics)
        mock_streamer = MagicMock(spec=IQueueStreamer)

        deps = ConnectionDependencies(
            transport=mock_transport,
            bridge_synchronizer=mock_bridge_synchronizer,
            log_listener=mock_log,
            codec=mock_codec,
            response_decoder=mock_decoder,
            kinematics=mock_kinematics,
            streamer=mock_streamer,
        )

        provides = ConnectionFactory.create(dependencies=deps)

        self.assertIsInstance(provides, ConnectionProvides)
        self.assertIsNotNone(provides.coordinator)
        self.assertIsNotNone(provides.command_dispatcher)

    def test_get_version(self) -> None:
        '''
            Tests factory version inquiry.
        '''
        self.assertEqual(ConnectionFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
