# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit test cases for EmulationController.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.controller.controller import EmulationController
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationControllerTestCase(TestCase):
    '''
        Test case verifying EmulationController command processing and interlocks.

        It defines:

            :methods:
                | setUp - Prepares test environment with flags and mock queue.
                | test_structural_compliance - Verifies satisfaction of IEmulationController.
                | test_set_motors_enabled - Verifies motors enable/disable and queue clearing.
                | test_set_estop - Verifies estop activation and queue clearing.
                | test_set_hold - Verifies feed-hold pause state changes.
                | test_set_elbow_mode - Verifies elbow kinematic orientation mode setting.
                | test_get_flags - Verifies get_flags returns current flags instance.
    '''

    def setUp(self) -> None:
        self.flags = EmulationFlags()
        self.queue = MagicMock(spec=IEmulationQueue)
        self.controller = EmulationController(flags=self.flags, queue=self.queue)

    def test_structural_compliance(self) -> None:
        '''
            Verifies satisfaction of IEmulationController protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.controller, IEmulationController)

    def test_set_motors_enabled(self) -> None:
        '''
            Verifies motors enable/disable and queue clearing.

            :exceptions: None.
        '''
        self.controller.set_motors_enabled(False)
        self.assertFalse(self.flags.motors_enabled)
        self.queue.clear_queue.assert_called_once()

        self.queue.clear_queue.reset_mock()
        self.controller.set_motors_enabled(True)
        self.assertTrue(self.flags.motors_enabled)
        self.queue.clear_queue.assert_not_called()

    def test_set_estop(self) -> None:
        '''
            Verifies estop activation and queue clearing.

            :exceptions: None.
        '''
        self.controller.set_estop(True)
        self.assertTrue(self.flags.estop_active)
        self.queue.clear_queue.assert_called_once()

        self.queue.clear_queue.reset_mock()
        self.controller.set_estop(False)
        self.assertFalse(self.flags.estop_active)
        self.queue.clear_queue.assert_not_called()

    def test_set_hold(self) -> None:
        '''
            Verifies feed-hold pause state changes.

            :exceptions: None.
        '''
        self.controller.set_hold(True)
        self.assertTrue(self.flags.hold_active)
        self.controller.set_hold(False)
        self.assertFalse(self.flags.hold_active)

    def test_set_elbow_mode(self) -> None:
        '''
            Verifies elbow kinematic orientation mode setting.

            :exceptions: None.
        '''
        self.controller.set_elbow_mode(True)
        self.assertTrue(self.flags.elbow_left)
        self.controller.set_elbow_mode(False)
        self.assertFalse(self.flags.elbow_left)

    def test_get_flags(self) -> None:
        '''
            Verifies get_flags returns current flags instance.

            :exceptions: None.
        '''
        self.assertIs(self.controller.get_flags(), self.flags)


if __name__ == '__main__':
    unittest_main()
