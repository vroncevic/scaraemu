# -*- coding: UTF-8 -*-

'''
Module
    preference_test.py
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
    Unit tests for ServerPreference value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.preferences.server.preference import ServerPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerPreference(TestCase):
    '''
        Unit tests for ServerPreference.

        It defines:

            :methods:
                | test_preference_creation_and_attributes - Tests creating preference and accessing attributes.
                | test_preference_equality - Tests equality and immutability between identical preferences.
    '''

    def test_preference_creation_and_attributes(self) -> None:
        '''
            Tests creating preference and accessing attributes.

            :exceptions: None.
        '''
        pref: ServerPreference = ServerPreference(
            host='127.0.0.1',
            port=8888
        )
        self.assertEqual(pref.host, '127.0.0.1')
        self.assertEqual(pref.port, 8888)

    def test_preference_equality(self) -> None:
        '''
            Tests equality and immutability between identical preferences.

            :exceptions: None.
        '''
        pref1: ServerPreference = ServerPreference('127.0.0.1', 8888)
        pref2: ServerPreference = ServerPreference('127.0.0.1', 8888)
        pref3: ServerPreference = ServerPreference('0.0.0.0', 8889)

        self.assertEqual(pref1, pref2)
        self.assertNotEqual(pref1, pref3)


if __name__ == '__main__':
    unittest_main()
