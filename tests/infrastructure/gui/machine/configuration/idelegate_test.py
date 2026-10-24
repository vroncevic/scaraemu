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
    Unit tests for IConfigurationDelegate structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.machine.configuration.idelegate import IConfigurationDelegate


class _DummyConfigurationDelegate:
    '''
        Dummy class conforming to IConfigurationDelegate structurally.

        It defines:

            :methods:
                | handle_toggle_elbow - Toggles elbow orientation.
                | handle_toggle_motors - Toggles motor drivers.
                | get_version - Returns version string.
    '''

    def handle_toggle_elbow(self) -> None:
        '''
            Toggles elbow orientation.

            :exceptions: None.
        '''

    def handle_toggle_motors(self) -> None:
        '''
            Toggles motor drivers.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidConfigurationDelegate:
    '''
        Dummy class missing protocol methods.

        It defines:

            :methods:
                | reset - Resets delegate state.
                | get_version - Returns version string.
    '''

    def reset(self) -> None:
        '''
            Resets delegate state.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestIConfigurationDelegate(TestCase):
    '''
        Test cases verifying IConfigurationDelegate structural protocol subtyping.

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
        delegate = _DummyConfigurationDelegate()
        self.assertIsInstance(delegate, IConfigurationDelegate)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming instance fails check.

            :exceptions: None.
        '''
        invalid = _InvalidConfigurationDelegate()
        self.assertNotIsInstance(invalid, IConfigurationDelegate)


if __name__ == '__main__':
    unittest_main()
