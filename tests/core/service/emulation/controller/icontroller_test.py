# -*- coding: UTF-8 -*-

'''
Module
    icontroller_test.py
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
    Unit test cases for IEmulationController structural protocol definition.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationController:
    '''
        Mock class satisfying IEmulationController structural protocol.

        It defines:

            :methods:
                | set_motors_enabled - Enables or disables motors.
                | set_estop - Sets emergency stop state.
                | set_hold - Sets hold motion state.
                | set_elbow_mode - Sets kinematic elbow orientation.
                | get_flags - Returns current emulation state flags.
    '''

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables motors.

            :param enabled: Motor state.
            :exceptions: None.
        '''
        _ = enabled

    def set_estop(self, active: bool) -> None:
        '''
            Sets emergency stop state.

            :param active: Stop state.
            :exceptions: None.
        '''
        _ = active

    def set_hold(self, active: bool) -> None:
        '''
            Sets hold motion state.

            :param active: Hold state.
            :exceptions: None.
        '''
        _ = active

    def set_elbow_mode(self, is_left: bool) -> None:
        '''
            Sets kinematic elbow orientation.

            :param is_left: True if elbow left.
            :exceptions: None.
        '''
        _ = is_left

    def get_flags(self) -> EmulationFlags:
        '''
            Returns current emulation state flags.

            :return: EmulationFlags instance.
            :exceptions: None.
        '''
        return EmulationFlags(
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=True,
        )


class _IncompleteEmulationController:
    '''
        Mock class missing methods of IEmulationController.

        It defines:

            :methods:
                | set_motors_enabled - Enables or disables motors.
                | get_version - Returns version string.
    '''

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables motors.

            :param enabled: Motor state.
            :exceptions: None.
        '''
        _ = enabled

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


class IEmulationControllerTestCase(TestCase):
    '''
        Test case verifying runtime checkability of IEmulationController.

        It defines:

            :methods:
                | test_structural_conformance - Verifies complete protocol conformance.
                | test_incomplete_conformance - Verifies rejection of incomplete class.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies complete protocol conformance.

            :exceptions: None.
        '''
        mock = _MockEmulationController()
        self.assertIsInstance(mock, IEmulationController)

    def test_incomplete_conformance(self) -> None:
        '''
            Verifies rejection of incomplete class.

            :exceptions: None.
        '''
        incomplete = _IncompleteEmulationController()
        self.assertNotIsInstance(incomplete, IEmulationController)


if __name__ == '__main__':
    unittest_main()
