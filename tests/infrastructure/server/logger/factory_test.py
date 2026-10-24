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
    Unit tests for ServerLogListenerHolderFactory implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.logger.factory import ServerLogListenerHolderFactory
from scaraemu.infrastructure.server.logger.holder import ServerLogListenerHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerLogListenerHolderFactory(TestCase):
    '''
        Unit tests for ServerLogListenerHolderFactory.

        It defines:

            :methods:
                | test_create - Tests instantiating ServerLogListenerHolder.
                | test_get_version - Tests component version retrieval.
    '''

    def test_create(self) -> None:
        '''
            Tests instantiating ServerLogListenerHolder.

            :exceptions: None.
        '''
        holder = ServerLogListenerHolderFactory.create()
        self.assertIsInstance(holder, ServerLogListenerHolder)

    def test_get_version(self) -> None:
        '''
            Tests component version retrieval.

            :exceptions: None.
        '''
        version = ServerLogListenerHolderFactory.get_version()
        self.assertIsInstance(version, str)


if __name__ == '__main__':
    unittest_main()
