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
    Unit test cases verifying MotionHandlerDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.server.handler.motion.dependencies import MotionHandlerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionHandlerDependencies(TestCase):
    '''
        Unit test cases verifying MotionHandlerDependencies encapsulation.

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
        mock_service = MagicMock()
        mock_queue = MagicMock()
        mock_holder = MagicMock()
        mock_kin = MagicMock()
        mock_val = MagicMock()
        mock_builder = MagicMock()
        mock_dec = MagicMock()
        mock_log = MagicMock()

        bundle = MotionHandlerDependencies(
            emulation_service=mock_service,
            emulation_queue=mock_queue,
            pose_holder=mock_holder,
            kinematics=mock_kin,
            validator=mock_val,
            response_builder=mock_builder,
            decoder=mock_dec,
            log_listener=mock_log,
        )

        self.assertIs(bundle.emulation_service, mock_service)
        self.assertIs(bundle.emulation_queue, mock_queue)
        self.assertIs(bundle.pose_holder, mock_holder)
        self.assertIs(bundle.kinematics, mock_kin)
        self.assertIs(bundle.validator, mock_val)
        self.assertIs(bundle.response_builder, mock_builder)
        self.assertIs(bundle.decoder, mock_dec)
        self.assertIs(bundle.log_listener, mock_log)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen bundle rejects direct attribute mutation.

            :exceptions: None.
        '''
        bundle = MotionHandlerDependencies(
            emulation_service=MagicMock(),
            emulation_queue=MagicMock(),
            pose_holder=MagicMock(),
            kinematics=MagicMock(),
            validator=MagicMock(),
            response_builder=MagicMock(),
            decoder=MagicMock(),
            log_listener=MagicMock(),
        )

        with self.assertRaises(AttributeError):
            bundle.kinematics = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    unittest_main()
