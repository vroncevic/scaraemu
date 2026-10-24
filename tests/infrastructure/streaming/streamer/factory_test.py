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
    Unit test cases for QueueStreamerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.flow.pacing.iwindow import IFlowWindow
from scaracom.transport.itransport import ITransport

from scaraemu.infrastructure.streaming.pumper.ipumper import IQueuePumper
from scaraemu.infrastructure.streaming.streamer.dependencies import StreamerDependencies
from scaraemu.infrastructure.streaming.streamer.factory import QueueStreamerFactory
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer
from scaraemu.infrastructure.streaming.streamer.streamer import QueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueStreamerFactoryTestCase(TestCase):
    '''
        Test cases verifying QueueStreamerFactory behavior.

        It defines:

            :methods:
                | test_create - Tests factory create instantiating QueueStreamer.
                | test_get_version - Tests factory version inquiry.
    '''

    def test_create(self) -> None:
        '''
            Tests factory create instantiating QueueStreamer.
        '''
        deps = StreamerDependencies(
            transport=MagicMock(spec=ITransport),
            flow_window=MagicMock(spec=IFlowWindow),
            pumper=MagicMock(spec=IQueuePumper),
        )
        streamer = QueueStreamerFactory.create(dependencies=deps)
        self.assertIsInstance(streamer, QueueStreamer)
        self.assertIsInstance(streamer, IQueueStreamer)
        self.assertEqual(streamer.get_version(), '1.0.2')

    def test_get_version(self) -> None:
        '''
            Tests factory version inquiry.
        '''
        self.assertEqual(QueueStreamerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
