# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit test cases verifying SystemHandlerDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSystemHandlerDependencies(TestCase):
    '''
        Unit test cases verifying SystemHandlerDependencies encapsulation.

        It defines:

            :methods:
                | test_bundle_creation - Verifies bundle correctly stores injected dependencies.
                | test_bundle_immutability - Verifies frozen bundle rejects direct attribute mutation.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle correctly stores injected dependencies.

            :exceptions: None.
        '''
        mock_controller = MagicMock()
        mock_queue = MagicMock()
        mock_builder = MagicMock()
        home = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)

        bundle = SystemHandlerDependencies(
            emulation_controller=mock_controller,
            emulation_queue=mock_queue,
            response_builder=mock_builder,
            home_pose=home,
        )

        self.assertIs(bundle.emulation_controller, mock_controller)
        self.assertIs(bundle.emulation_queue, mock_queue)
        self.assertIs(bundle.response_builder, mock_builder)
        self.assertEqual(bundle.home_pose, home)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen bundle rejects direct attribute mutation.

            :exceptions: None.
        '''
        bundle = SystemHandlerDependencies(
            emulation_controller=MagicMock(),
            emulation_queue=MagicMock(),
            response_builder=MagicMock(),
            home_pose=ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0),
        )

        with self.assertRaises(AttributeError):
            bundle.home_pose = ScaraPose(x=0.0, y=0.0, z=0.0, phi=0.0)  # type: ignore[misc]


if __name__ == '__main__':
    unittest_main()
