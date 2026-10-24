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
    Unit tests for IDeadZoneBypassAdapter protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockDeadZoneBypassAdapter:
    '''
        Mock implementation verifying IDeadZoneBypassAdapter structural protocol.
    '''

    def plan_bypass(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> list[ScaraPose]:
        '''
            Computes a collision-free bypass trajectory sequence around the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: Ordered list of intermediate Cartesian poses to destination.
            :exceptions: None.
        '''
        return [end_pose]

    def is_segment_crossing_dead_zone(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Determines whether the direct line between poses traverses the dead zone.

            :param start_pose: Starting Cartesian pose.
            :param end_pose: Destination Cartesian pose.
            :return: True if segment crosses dead zone, False otherwise.
            :exceptions: None.
        '''
        return False

    def get_version(self) -> str:
        '''
            Returns adapter component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return '1.0.2'


class TestDeadZoneBypassAdapterProtocol(TestCase):
    '''
        Test cases verifying IDeadZoneBypassAdapter protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies mock satisfies protocol.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies mock satisfies protocol.

            :exceptions: None.
        '''
        adapter = _MockDeadZoneBypassAdapter()
        self.assertIsInstance(adapter, IDeadZoneBypassAdapter)


if __name__ == '__main__':
    unittest_main()
