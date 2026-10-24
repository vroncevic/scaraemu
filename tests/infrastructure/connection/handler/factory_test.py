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
    Unit tests for ResponseHandlerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.connection.handler.dependencies import HandlerDependencies
from scaraemu.infrastructure.connection.handler.factory import ResponseHandlerFactory
from scaraemu.infrastructure.connection.handler.handler import ResponseHandler
from scaraemu.infrastructure.connection.handler.ihandler import IResponseHandler
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


class TestResponseHandlerFactory(TestCase):
    '''
        Unit tests verifying ResponseHandlerFactory instantiation semantics.
    '''

    def test_create(self) -> None:
        '''
            Tests creating ResponseHandler instance via factory.
        '''
        deps = HandlerDependencies(
            listener=MagicMock(spec=IBridgeSynchronizer),
            log_listener=MagicMock(spec=ILogListener),
            streamer=MagicMock(spec=IQueueStreamer),
            codec=MagicMock(spec=IBinaryFrameCodecAdapter),
            kinematics=MagicMock(spec=IManipulatorKinematics),
            response_decoder=MagicMock(spec=IBinaryResponseDecoderAdapter),
        )

        handler = ResponseHandlerFactory.create(dependencies=deps)
        self.assertIsInstance(handler, ResponseHandler)
        self.assertIsInstance(handler, IResponseHandler)

    def test_get_version(self) -> None:
        '''
            Tests factory version accessor.
        '''
        self.assertEqual(ResponseHandlerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
