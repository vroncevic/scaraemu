# -*- coding: UTF-8 -*-

'''
Module
    services_test.py
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
    Unit tests for GuiServicesBundle dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.services import GuiServicesBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiServicesBundleTestCase(TestCase):
    '''
        Unit tests verifying GuiServicesBundle data container behavior.

        It defines:

            :methods:
                | setUp - Initializes mock services and bundle instance.
                | test_bundle_field_preservation - Verifies all services are stored and accessible.
                | test_bundle_immutability - Verifies frozen dataclass raises error upon attribute mutation.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock services and bundle instance.
        '''
        self.mock_transport = MagicMock()
        self.mock_kinematics = MagicMock()
        self.mock_emulation_service = MagicMock()
        self.mock_emulation_controller = MagicMock()
        self.mock_emulation_queue = MagicMock()
        self.mock_server = MagicMock()
        self.mock_preferences = MagicMock()
        self.mock_scaralang = MagicMock()
        self.mock_port_scanner = MagicMock()

        self.bundle = GuiServicesBundle(
            transport=self.mock_transport,
            kinematics=self.mock_kinematics,
            emulation_service=self.mock_emulation_service,
            emulation_controller=self.mock_emulation_controller,
            emulation_queue=self.mock_emulation_queue,
            server=self.mock_server,
            preferences=self.mock_preferences,
            scaralang=self.mock_scaralang,
            port_scanner=self.mock_port_scanner,
        )

    def test_bundle_field_preservation(self) -> None:
        '''
            Verifies all services are stored and accessible.
        '''
        self.assertIs(self.bundle.transport, self.mock_transport)
        self.assertIs(self.bundle.kinematics, self.mock_kinematics)
        self.assertIs(self.bundle.emulation_service, self.mock_emulation_service)
        self.assertIs(self.bundle.emulation_controller, self.mock_emulation_controller)
        self.assertIs(self.bundle.emulation_queue, self.mock_emulation_queue)
        self.assertIs(self.bundle.server, self.mock_server)
        self.assertIs(self.bundle.preferences, self.mock_preferences)
        self.assertIs(self.bundle.scaralang, self.mock_scaralang)
        self.assertIs(self.bundle.port_scanner, self.mock_port_scanner)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen dataclass raises error upon attribute mutation.
        '''
        with self.assertRaises(FrozenInstanceError):
            self.bundle.transport = MagicMock()


if __name__ == '__main__':
    unittest_main()
