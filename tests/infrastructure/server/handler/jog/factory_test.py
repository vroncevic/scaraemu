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
    Unit tests for JogHandlerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.server.handler.jog.dependencies import JogHandlerDependencies
from scaraemu.infrastructure.server.handler.jog.factory import JogHandlerFactory
from scaraemu.infrastructure.server.handler.jog.handler import JogHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogHandlerFactory(TestCase):
    '''
        Unit tests for JogHandlerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creates JogHandler.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates JogHandler.

            :exceptions: None.
        '''
        deps = JogHandlerDependencies(
            emulation_service=MagicMock(),
            emulation_queue=MagicMock(),
            pose_holder=MagicMock(),
            kinematics=MagicMock(),
            response_builder=MagicMock(),
            decoder=MagicMock(),
        )
        handler = JogHandlerFactory.create(dependencies=deps)
        self.assertIsInstance(handler, JogHandler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertIsInstance(JogHandlerFactory.get_version(), str)
        self.assertEqual(JogHandlerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
