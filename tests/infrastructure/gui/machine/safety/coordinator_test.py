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
    Unit tests for SafetyCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.message import MessageId

from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.connection.command.idispatcher import ICommandDispatcher
from scaraemu.infrastructure.gui.machine.safety.coordinator import SafetyCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSafetyCoordinator(TestCase):
    '''
        Unit tests for SafetyCoordinator.

        It defines:

            :methods:
                | setUp - Initializes mock dependencies and coordinator.
                | test_handle_estop - Verifies emergency stop asserting and dispatching.
                | test_handle_toggle_hold_activate - Verifies activating feed-hold pause.
                | test_handle_toggle_hold_resume - Verifies resuming from feed-hold pause.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock dependencies and coordinator.

            :exceptions: None.
        '''
        self._controller = MagicMock(spec=IEmulationController)
        self._queue = MagicMock(spec=IEmulationQueue)
        self._command_port = MagicMock(spec=ICommandDispatcher)

        self._flags = EmulationFlags(
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )
        self._controller.get_flags.return_value = self._flags

        self._coordinator = SafetyCoordinator(
            emulation_controller=self._controller,
            emulation_queue=self._queue,
            command_port=self._command_port,
        )

    def test_handle_estop(self) -> None:
        '''
            Verifies emergency stop asserting and dispatching.

            :exceptions: None.
        '''
        self._coordinator.handle_estop()
        self._controller.set_estop.assert_called_once_with(True)
        self._queue.clear_queue.assert_called_once()
        self._command_port.clear_queue.assert_called_once()
        self._command_port.send_command.assert_called_once_with(MessageId.CMD_ESTOP)

    def test_handle_toggle_hold_activate(self) -> None:
        '''
            Verifies activating feed-hold pause.

            :exceptions: None.
        '''
        self._coordinator.handle_toggle_hold()
        self._controller.set_hold.assert_called_once_with(True)
        self._command_port.send_command.assert_called_once_with(MessageId.CMD_HOLD)

    def test_handle_toggle_hold_resume(self) -> None:
        '''
            Verifies resuming from feed-hold pause.

            :exceptions: None.
        '''
        held_flags = EmulationFlags(
            motors_enabled=True,
            estop_active=False,
            hold_active=True,
            elbow_left=False,
        )
        self._controller.get_flags.return_value = held_flags

        self._coordinator.handle_toggle_hold()
        self._controller.set_hold.assert_called_once_with(False)
        self._command_port.send_command.assert_called_once_with(MessageId.CMD_RESUME)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self._coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
