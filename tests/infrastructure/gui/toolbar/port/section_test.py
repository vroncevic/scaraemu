# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for PortSelectorSection toolbar subcomponent.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from tkinter.ttk import Combobox
from unittest import TestCase, main as unittest_main

from scaracom.transport.preference.preference import SerialPreference

from scaraemu.infrastructure.gui.toolbar.port.iprovider import IConnectionParameterProvider
from scaraemu.infrastructure.gui.toolbar.port.section import PortSelectorSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockPortScanner:
    '''
        Unit tests for _MockPortScanner.
    '''
    def scan_ports(self) -> list[str]:
        '''
            Tests scan ports.

            :exceptions: None.
        '''
        return ['/dev/ttyUSB0', '/dev/ttyACM0']

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockPreferencesRepository:
    '''
        Unit tests for _MockPreferencesRepository.
    '''
    def has_preference(self) -> bool:
        '''
            Tests has preference.

            :exceptions: None.
        '''
        return True

    def load_preference(self) -> SerialPreference:
        '''
            Tests load preference.

            :exceptions: None.
        '''
        return SerialPreference(port='/dev/ttyUSB0', baud=115200)

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Tests save preference.

            :param preference: Input preference.
            :exceptions: None.
        '''
        _ = preference
        return True

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestPortSelectorSection(TestCase):
    '''
        Unit tests for PortSelectorSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_section_initialization_and_protocol - Tests section initialization and protocol conformance.
                | test_refresh_ports_and_set_enabled - Tests refreshing ports and toggling enabled state.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_section_initialization_and_protocol(self) -> None:
        '''
            Tests section initialization and protocol conformance.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        section = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_MockPreferencesRepository(),
        )
        section.pack()

        self.assertIsInstance(section, IConnectionParameterProvider)
        port, baud = section.get_connection_parameters()
        self.assertIsInstance(port, str)
        self.assertIsInstance(baud, int)
        self.assertEqual(section.get_version(), '1.0.2')

    def test_refresh_ports_and_set_enabled(self) -> None:
        '''
            Tests refreshing ports and toggling enabled state.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        section = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_MockPreferencesRepository(),
        )
        section.set_enabled(False)
        section.set_enabled(True)

    def test_get_connection_target_invalid_baud(self) -> None:
        '''
            Tests get_connection_parameters fallback when baud cannot be parsed as int.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        section = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_MockPreferencesRepository(),
        )
        combos: list[Combobox] = [
            w for w in section.winfo_children() if isinstance(w, Combobox)
        ]
        combos[1].set('invalid_baud')
        _, baud = section.get_connection_parameters()
        self.assertEqual(baud, 115200)

    def test_refresh_ports_preference_fallbacks(self) -> None:
        '''
            Tests refresh_ports fallback branches when preferences are missing or invalid.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        # Case 1: no preference
        class _NoPrefRepo(_MockPreferencesRepository):
            def has_preference(self) -> bool:
                return False

        section1 = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_NoPrefRepo(),
        )
        section1.refresh_ports()

        # Case 2: preference port not in combo
        class _UnknownPortRepo(_MockPreferencesRepository):
            def load_preference(self) -> SerialPreference:
                return SerialPreference(port='/dev/unknown_device', baud=9600)

        section2 = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_UnknownPortRepo(),
        )
        section2.refresh_ports()

        # Case 3: exception loading preference
        class _FailingRepo(_MockPreferencesRepository):
            def load_preference(self) -> SerialPreference:
                raise RuntimeError('preference read failure')

        section3 = PortSelectorSection(
            self._root,
            port_scanner=_MockPortScanner(),
            preference_repository=_FailingRepo(),
        )
        section3.refresh_ports()


if __name__ == '__main__':
    unittest_main()
