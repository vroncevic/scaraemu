# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for ISafetyDelegate structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate


class _DummySafetyDelegate:
    '''
        Dummy class conforming to ISafetyDelegate structurally.

        It defines:

            :methods:
                | handle_toggle_hold - Toggles feed-hold pause state.
                | handle_estop - Triggers emergency stop.
                | get_version - Returns version string.
    '''

    def handle_toggle_hold(self) -> None:
        '''
            Toggles feed-hold pause state.

            :exceptions: None.
        '''

    def handle_estop(self) -> None:
        '''
            Triggers emergency stop.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidSafetyDelegate:
    '''
        Dummy class missing protocol methods.

        It defines:

            :methods:
                | reset - Resets safety state.
                | get_version - Returns version string.
    '''

    def reset(self) -> None:
        '''
            Resets safety state.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestISafetyDelegate(TestCase):
    '''
        Test cases verifying ISafetyDelegate structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming instance satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming instance fails check.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming instance satisfies protocol.

            :exceptions: None.
        '''
        delegate = _DummySafetyDelegate()
        self.assertIsInstance(delegate, ISafetyDelegate)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming instance fails check.

            :exceptions: None.
        '''
        invalid = _InvalidSafetyDelegate()
        self.assertNotIsInstance(invalid, ISafetyDelegate)


if __name__ == '__main__':
    unittest_main()
