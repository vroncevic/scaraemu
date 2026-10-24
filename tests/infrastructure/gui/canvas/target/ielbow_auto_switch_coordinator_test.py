# -*- coding: UTF-8 -*-

'''
Module
    ielbow_auto_switch_coordinator_test.py
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
    Unit tests for IElbowAutoSwitchCoordinator protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.target.elbow_auto_switch_coordinator import ElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.ielbow_auto_switch_coordinator import IElbowAutoSwitchCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ValidElbowAutoSwitchCoordinator:
    '''
        Dummy class conforming to IElbowAutoSwitchCoordinator structurally.
    '''

    def try_auto_switch(self, target_pose: ScaraPose) -> bool:
        '''
            Tests try auto switch.

            :param target_pose: Input target_pose.
            :exceptions: None.
        '''
        _ = target_pose
        return True

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidElbowAutoSwitchCoordinator:
    '''
        Dummy non-conforming class.
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


class TestIElbowAutoSwitchCoordinator(TestCase):
    '''
        Test cases verifying IElbowAutoSwitchCoordinator structural protocol.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming instance satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming instance fails protocol check.
                | test_concrete_class_satisfies_protocol - Verifies ElbowAutoSwitchCoordinator satisfies protocol attributes.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming instance satisfies protocol.

            :exceptions: None.
        '''
        instance = _ValidElbowAutoSwitchCoordinator()
        self.assertIsInstance(instance, IElbowAutoSwitchCoordinator)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming instance fails protocol check.

            :exceptions: None.
        '''
        invalid = _InvalidElbowAutoSwitchCoordinator()
        self.assertNotIsInstance(invalid, IElbowAutoSwitchCoordinator)

    def test_concrete_class_satisfies_protocol(self) -> None:
        '''
            Verifies ElbowAutoSwitchCoordinator satisfies protocol attributes.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(ElbowAutoSwitchCoordinator, 'try_auto_switch'))
        self.assertTrue(hasattr(ElbowAutoSwitchCoordinator, 'get_version'))


if __name__ == '__main__':
    unittest_main()
