# -*- coding: UTF-8 -*-

'''
Module
    icoordinator_test.py
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
    Unit tests for IConnectionCoordinator structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.connection.coordinator.icoordinator import IConnectionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingConnectionCoordinator:
    '''
        Dummy class conforming to IConnectionCoordinator structurally.
    '''

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Tests handle connect toggle.

            :param port: Target port.
            :param baudrate: Baud rate.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _NonConformingClass:
    '''
        Dummy class not conforming to IConnectionCoordinator.
    '''

    def dummy_method(self) -> None:
        '''Dummy method.'''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestIConnectionCoordinator(TestCase):
    '''
        Test cases verifying IConnectionCoordinator structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy class satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy protocol.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IConnectionCoordinator structurally.
        '''
        coordinator = _ConformingConnectionCoordinator()
        self.assertIsInstance(coordinator, IConnectionCoordinator)
        self.assertEqual(coordinator.get_version(), '1.0.2')

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IConnectionCoordinator.
        '''
        invalid = _NonConformingClass()
        self.assertNotIsInstance(invalid, IConnectionCoordinator)


if __name__ == '__main__':
    unittest_main()
