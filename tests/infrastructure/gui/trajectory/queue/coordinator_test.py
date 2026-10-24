# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for QueueActionCoordinator and IQueueActionDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate
from scaraemu.infrastructure.gui.trajectory.queue.coordinator import QueueActionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueActionCoordinatorTestCase(TestCase):
    '''
        Unit tests for QueueActionCoordinator operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies QueueActionCoordinator satisfies IQueueActionDelegate.
                | test_handle_clear_queue - Verifies clearing queue on both digital twin and hardware bridge.
                | test_handle_clear_trail - Verifies clearing trail on core emulation service.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies QueueActionCoordinator satisfies IQueueActionDelegate.

            :exceptions: None.
        '''
        command_port = MagicMock(spec=ICommandDispatcher)
        queue = MagicMock(spec=IEmulationQueue)
        service = MagicMock(spec=IEmulationService)

        coordinator = QueueActionCoordinator(
            command_port=command_port,
            emulation_queue=queue,
            emulation_service=service,
        )

        self.assertIsInstance(coordinator, IQueueActionDelegate)
        self.assertEqual(coordinator.get_version(), '1.0.2')

    def test_handle_clear_queue(self) -> None:
        '''
            Verifies clearing queue on both digital twin and hardware bridge.

            :exceptions: None.
        '''
        command_port = MagicMock(spec=ICommandDispatcher)
        queue = MagicMock(spec=IEmulationQueue)
        service = MagicMock(spec=IEmulationService)

        coordinator = QueueActionCoordinator(
            command_port=command_port,
            emulation_queue=queue,
            emulation_service=service,
        )

        coordinator.handle_clear_queue()

        queue.clear_queue.assert_called_once()
        command_port.clear_queue.assert_called_once()

    def test_handle_clear_trail(self) -> None:
        '''
            Verifies clearing trail on core emulation service.

            :exceptions: None.
        '''
        command_port = MagicMock(spec=ICommandDispatcher)
        queue = MagicMock(spec=IEmulationQueue)
        service = MagicMock(spec=IEmulationService)

        coordinator = QueueActionCoordinator(
            command_port=command_port,
            emulation_queue=queue,
            emulation_service=service,
        )

        coordinator.handle_clear_trail()

        service.clear_trail.assert_called_once()


if __name__ == '__main__':
    unittest_main()
