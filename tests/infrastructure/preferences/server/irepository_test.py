# -*- coding: UTF-8 -*-

'''
Module
    irepository_test.py
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
    Unit tests for IServerPreferenceRepository protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.preferences.server.irepository import IServerPreferenceRepository
from scaraemu.infrastructure.preferences.server.preference import ServerPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyServerPreferencesRepository:
    '''
        Dummy implementation satisfying IServerPreferenceRepository structurally.

        It defines:

            :methods:
                | has_preference - Checks preference presence.
                | load_preference - Loads preference.
                | save_preference - Saves preference.
                | get_version - Returns version string.
    '''

    def has_preference(self) -> bool:
        '''
            Checks preference presence.

            :exceptions: None.
        '''
        return True

    def load_preference(self) -> ServerPreference:
        '''
            Loads preference.

            :exceptions: None.
        '''
        return ServerPreference(host='127.0.0.1', port=8888)

    def save_preference(self, host: str, port: int = 8888) -> bool:
        '''
            Saves preference.

            :param host: Input host.
            :param port: Input port.
            :exceptions: None.
        '''
        return bool(host and port > 0)

    def get_version(self) -> str:
        '''
            Returns version string.

            :exceptions: None.
        '''
        return '1.0.2'


class TestIServerPreferenceRepository(TestCase):
    '''
        Unit tests for IServerPreferenceRepository protocol.

        It defines:

            :methods:
                | test_structural_subtyping_conformance - Tests structural typing conformance.
    '''

    def test_structural_subtyping_conformance(self) -> None:
        '''
            Tests that structural typing matches IServerPreferenceRepository.

            :exceptions: None.
        '''
        dummy = DummyServerPreferencesRepository()
        self.assertIsInstance(dummy, IServerPreferenceRepository)
        self.assertTrue(dummy.has_preference())
        self.assertEqual(dummy.load_preference().host, '127.0.0.1')
        self.assertTrue(dummy.save_preference('127.0.0.1', 8888))
        self.assertEqual(dummy.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
