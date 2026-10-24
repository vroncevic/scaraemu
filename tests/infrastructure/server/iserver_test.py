# -*- coding: UTF-8 -*-

'''
Module
    iserver_test.py
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
    Unit tests for IVirtualManipulatorServer protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.server.iserver import IVirtualManipulatorServer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyVirtualManipulatorServer:
    '''
        Dummy class conforming to IVirtualManipulatorServer structurally.
    '''

    def start(self, *, host: str = '127.0.0.1', port: int = 8888) -> bool:
        '''
            Starts listening for external host connections.

            :param host: Host string.
            :param port: Port integer.
            :return: True if started.
            :exceptions: None.
        '''
        _ = (host, port)
        return True

    def stop(self) -> None:
        '''
            Terminates background server and closes client sockets.

            :exceptions: None.
        '''

    def is_running(self) -> bool:
        '''
            Checks whether server is currently active.

            :return: True if active.
            :exceptions: None.
        '''
        return True

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidVirtualManipulatorServer:
    '''
        Dummy class missing required protocol methods.
    '''


class TestIVirtualManipulatorServer(TestCase):
    '''
        Test cases verifying IVirtualManipulatorServer structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy class satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming class fails.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies IVirtualManipulatorServer structurally.

            :exceptions: None.
        '''
        server = _DummyVirtualManipulatorServer()
        self.assertIsInstance(server, IVirtualManipulatorServer)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IVirtualManipulatorServer.

            :exceptions: None.
        '''
        invalid = _InvalidVirtualManipulatorServer()
        self.assertNotIsInstance(invalid, IVirtualManipulatorServer)


if __name__ == '__main__':
    unittest_main()
