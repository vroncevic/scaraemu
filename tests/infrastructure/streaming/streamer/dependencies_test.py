# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit test cases for StreamerDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.flow.pacing.iwindow import IFlowWindow
from scaracom.transport.itransport import ITransport

from scaraemu.infrastructure.streaming.pumper.ipumper import IQueuePumper
from scaraemu.infrastructure.streaming.streamer.dependencies import StreamerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerDependenciesTestCase(TestCase):
    '''
        Test cases verifying StreamerDependencies behavior.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores and exposes attributes.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle correctly stores and exposes attributes.
        '''
        transport = MagicMock(spec=ITransport)
        flow_window = MagicMock(spec=IFlowWindow)
        pumper = MagicMock(spec=IQueuePumper)

        bundle = StreamerDependencies(
            transport=transport,
            flow_window=flow_window,
            pumper=pumper,
        )

        self.assertIs(bundle.transport, transport)
        self.assertIs(bundle.flow_window, flow_window)
        self.assertIs(bundle.pumper, pumper)


if __name__ == '__main__':
    unittest_main()
