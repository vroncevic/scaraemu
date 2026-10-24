# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for IWorkspaceReachAdapter structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockWorkspaceReachAdapter:
    '''
        Mock implementation verifying IWorkspaceReachAdapter structural protocol.
    '''

    def get_safe_r_min(self) -> float:
        '''
            Returns minimum safe annular reach radius in mm.
        '''
        return 77.6

    def get_safe_r_max(self) -> float:
        '''
            Returns maximum safe reach radius considering singularity margin in mm.
        '''
        return 267.0

    def calculate_home_pose(self) -> ScaraPose:
        '''
            Returns mock home pose.
        '''
        return ScaraPose(x=175.5, y=0.0, z=20.0, phi=0.0)

    def get_version(self) -> str:
        '''
            Returns component version string.
        '''
        return '1.0.2'


class TestIWorkspaceReachAdapter(TestCase):
    '''
        Validates structural protocol compliance for IWorkspaceReachAdapter.
    '''

    def test_mock_implements_protocol(self) -> None:
        '''
            Verifies mock satisfies structural protocol.
        '''
        mock_adapter = _MockWorkspaceReachAdapter()
        self.assertIsInstance(mock_adapter, IWorkspaceReachAdapter)

    def test_invalid_object_fails(self) -> None:
        '''
            Verifies incomplete class fails check.
        '''
        class _IncompleteAdapter:
            def get_safe_r_min(self) -> float:
                return 77.6

        self.assertNotIsInstance(_IncompleteAdapter(), IWorkspaceReachAdapter)


if __name__ == '__main__':
    unittest_main()
