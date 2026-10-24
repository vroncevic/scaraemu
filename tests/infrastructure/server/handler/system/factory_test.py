# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SystemHandlerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.server.handler.system.dependencies import SystemHandlerDependencies
from scaraemu.infrastructure.server.handler.system.factory import SystemHandlerFactory
from scaraemu.infrastructure.server.handler.system.handler import SystemHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSystemHandlerFactory(TestCase):
    '''
        Unit tests for SystemHandlerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creates SystemHandler.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates SystemHandler.

            :exceptions: None.
        '''
        deps = SystemHandlerDependencies(
            emulation_controller=MagicMock(),
            emulation_queue=MagicMock(),
            response_builder=MagicMock(),
            home_pose=ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0),
        )
        handler = SystemHandlerFactory.create(dependencies=deps)
        self.assertIsInstance(handler, SystemHandler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertIsInstance(SystemHandlerFactory.get_version(), str)
        self.assertEqual(SystemHandlerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
