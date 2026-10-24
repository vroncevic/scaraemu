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
    Unit tests for IMotionValidatorAdapter protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.safety.factory import MotionValidatorAdapterFactory
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockMotionValidatorAdapter:
    '''
        Mock implementation verifying IMotionValidatorAdapter structural protocol.
    '''

    def is_pose_valid(self, pose: ScaraPose) -> bool:
        '''
            Checks whether Cartesian pose avoids the dead zone and falls within reachable envelope.
        '''
        return True

    def is_segment_valid(
        self,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
    ) -> bool:
        '''
            Determines whether linear segment between poses avoids traversing the dead zone.
        '''
        return True

    def get_version(self) -> str:
        '''
            Returns adapter component version string representation.
        '''
        return '1.0.2'


class _NonConformingMotionValidator:
    '''
        Non-conforming class lacking required motion validator methods.
    '''

    def dummy(self) -> None:
        '''
            Non-conforming dummy method.
        '''


class TestMotionValidatorAdapterProtocol(TestCase):
    '''
        Test cases verifying IMotionValidatorAdapter protocol conformance.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies mock satisfies IMotionValidatorAdapter structurally.
        '''
        mock_adapter = _MockMotionValidatorAdapter()
        self.assertIsInstance(mock_adapter, IMotionValidatorAdapter)

    def test_concrete_adapter_conformance(self) -> None:
        '''
            Verifies concrete MotionValidatorAdapter satisfies IMotionValidatorAdapter structurally.
        '''
        adapter: IMotionValidatorAdapter = MotionValidatorAdapterFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        self.assertIsInstance(adapter, IMotionValidatorAdapter)

    def test_non_conforming_fails(self) -> None:
        '''
            Verifies invalid object fails IMotionValidatorAdapter protocol check.
        '''
        invalid = _NonConformingMotionValidator()
        self.assertNotIsInstance(invalid, IMotionValidatorAdapter)


if __name__ == '__main__':
    unittest_main()
