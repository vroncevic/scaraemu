# -*- coding: UTF-8 -*-

'''
Module
    preference_not_found_error_test.py
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
    Unit tests for PreferenceNotFoundError exception.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.preferences.exceptions.preference_not_found_error import PreferenceNotFoundError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferenceNotFoundErrorTestCase(TestCase):
    '''
        Unit tests for PreferenceNotFoundError.

        It defines:

            :methods:
                | test_exception_inheritance_and_message - Tests that exception inherits from LookupError and retains message.
    '''

    def test_exception_inheritance_and_message(self) -> None:
        '''
            Tests that exception inherits from LookupError and retains message.

            :exceptions: None.
        '''
        err: PreferenceNotFoundError = PreferenceNotFoundError('Preference file not found')
        self.assertIsInstance(err, LookupError)
        self.assertEqual(str(err), 'Preference file not found')


if __name__ == '__main__':
    unittest_main()
