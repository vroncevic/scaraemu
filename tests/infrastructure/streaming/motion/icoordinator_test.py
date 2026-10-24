# -*- coding: UTF-8 -*-

'''
Module
    icoordinator_test.py
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
    Unit tests for IMotionCoordinator structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingMotionCoordinator:
    '''
        Dummy class conforming to IMotionCoordinator structurally.
    '''

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Tests send move.

            :param pose: Target pose.
            :exceptions: None.
        '''

    def enqueue_hardware_trajectory(self, poses: Sequence[ScaraPose]) -> None:
        '''
            Tests enqueue trajectory.

            :param poses: Sequence of poses.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _NonConformingMotionCoordinator:
    '''
        Dummy class missing methods.
    '''

    def send_hardware_move(self, pose: ScaraPose) -> None:
        '''
            Tests send move.
        '''

    def dummy_method(self) -> None:
        '''Dummy method.'''


class IMotionCoordinatorTestCase(TestCase):
    '''
        Unit tests for IMotionCoordinator.

        It defines:

            :methods:
                | test_structural_conformance - Verifies duck typing conformance.
                | test_non_conformance - Verifies non-conforming object is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies duck typing conformance.

            :exceptions: None.
        '''
        coordinator = _ConformingMotionCoordinator()
        self.assertIsInstance(coordinator, IMotionCoordinator)

    def test_non_conformance(self) -> None:
        '''
            Verifies non-conforming object is rejected.

            :exceptions: None.
        '''
        coordinator = _NonConformingMotionCoordinator()
        self.assertNotIsInstance(coordinator, IMotionCoordinator)


if __name__ == '__main__':
    unittest_main()
