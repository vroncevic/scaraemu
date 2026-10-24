# -*- coding: UTF-8 -*-

'''
Module
    imanager_test.py
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
    Unit tests for IVirtualServerManager structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.manager.imanager import IVirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyVirtualServerManager:
    '''
        Dummy class conforming to IVirtualServerManager structurally.
    '''

    def is_running(self) -> bool:
        '''
            Checks whether the virtual server is actively running.

            :exceptions: None.
        '''
        return True

    def toggle(self, port: int) -> bool:
        '''
            Starts or stops the background TCP server on given port.

            :param port: Input port.
            :exceptions: None.
        '''
        return True

    def stop(self) -> None:
        '''
            Stops the virtual server if active.

            :exceptions: None.
        '''
        pass

    def get_version(self) -> str:
        '''
            Returns interface version string.

            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidVirtualServerManager:
    '''
        Dummy class missing required protocol methods.
    '''
    pass


class TestIVirtualServerManager(TestCase):
    '''
        Test cases verifying IVirtualServerManager structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy class satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming class fails.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IVirtualServerManager structurally.

            :exceptions: None.
        '''
        manager = _DummyVirtualServerManager()
        self.assertIsInstance(manager, IVirtualServerManager)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IVirtualServerManager.

            :exceptions: None.
        '''
        invalid = _InvalidVirtualServerManager()
        self.assertNotIsInstance(invalid, IVirtualServerManager)


if __name__ == '__main__':
    unittest_main()
