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
    Unit tests for ITrajectoryPresetDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyTrajectoryPresetDelegate:
    '''
        Dummy implementation satisfying ITrajectoryPresetDelegate.
    '''

    def handle_demo_select(self, preset_name: str) -> None:
        '''
            Tests handle demo select.

            :param preset_name: Input preset_name.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidTrajectoryPresetDelegate:
    '''
        Dummy class missing required protocol methods.
    '''

    def invalid_action(self) -> None:
        '''
            Tests invalid action.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestTrajectoryPresetDelegate(TestCase):
    '''
        Test cases verifying ITrajectoryPresetDelegate protocol conformance.

        It defines:

            :methods:
                | test_protocol_implementation - Verifies dummy delegate satisfies ITrajectoryPresetDelegate protocol.
                | test_protocol_rejection - Verifies incomplete class fails ITrajectoryPresetDelegate conformance.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies dummy delegate satisfies ITrajectoryPresetDelegate protocol.

            :exceptions: None.
        '''
        delegate = _DummyTrajectoryPresetDelegate()
        self.assertIsInstance(delegate, ITrajectoryPresetDelegate)

    def test_protocol_rejection(self) -> None:
        '''
            Verifies incomplete class fails ITrajectoryPresetDelegate conformance.

            :exceptions: None.
        '''
        delegate = _InvalidTrajectoryPresetDelegate()
        self.assertNotIsInstance(delegate, ITrajectoryPresetDelegate)


if __name__ == '__main__':
    unittest_main()
