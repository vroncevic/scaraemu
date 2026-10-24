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
    Unit test cases for CoordinatorDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator as IComConnectionCoordinator

from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.connection.coordinator.dependencies import CoordinatorDependencies
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.streaming.streamer.istreamer import IQueueStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CoordinatorDependenciesTestCase(TestCase):
    '''
        Test cases verifying CoordinatorDependencies behavior.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores and exposes attributes.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle correctly stores and exposes attributes.
        '''
        connection = MagicMock(spec=IComConnectionCoordinator)
        listener = MagicMock(spec=IBridgeSynchronizer)
        streamer = MagicMock(spec=IQueueStreamer)
        command_dispatcher = MagicMock(spec=ICommandDispatcher)

        bundle = CoordinatorDependencies(
            connection=connection,
            listener=listener,
            streamer=streamer,
            command_dispatcher=command_dispatcher,
        )

        self.assertIs(bundle.connection, connection)
        self.assertIs(bundle.listener, listener)
        self.assertIs(bundle.streamer, streamer)
        self.assertIs(bundle.command_dispatcher, command_dispatcher)


if __name__ == '__main__':
    unittest_main()
