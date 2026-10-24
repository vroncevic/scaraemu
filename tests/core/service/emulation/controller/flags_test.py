# -*- coding: UTF-8 -*-

'''
Module
    flags_test.py
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
    Unit test cases for EmulationFlags state container.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.service.emulation.controller.flags import EmulationFlags

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationFlagsTestCase(TestCase):
    '''
        Test case verifying behavior of EmulationFlags.

        It defines:

            :methods:
                | test_default_values - Verifies default flag values.
                | test_custom_values - Verifies flag mutation.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default flag values.

            :exceptions: None.
        '''
        flags = EmulationFlags()
        self.assertTrue(flags.motors_enabled)
        self.assertFalse(flags.estop_active)
        self.assertFalse(flags.hold_active)
        self.assertFalse(flags.elbow_left)

    def test_custom_values(self) -> None:
        '''
            Verifies flag mutation.

            :exceptions: None.
        '''
        flags = EmulationFlags(
            motors_enabled=False,
            estop_active=True,
            hold_active=True,
            elbow_left=True,
        )
        self.assertFalse(flags.motors_enabled)
        self.assertTrue(flags.estop_active)
        self.assertTrue(flags.hold_active)
        self.assertTrue(flags.elbow_left)


if __name__ == '__main__':
    unittest_main()
