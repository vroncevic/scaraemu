# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for ActionCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaracom.transport.preference.preference import SerialPreference

from scaraemu.infrastructure.gui.toolbar.action.coordinator import ActionCoordinator
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate
from scaraemu.infrastructure.preferences.server.preference import ServerPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockConnectionPort:
    '''
        Mock implementation of IConnectionCoordinator.

        It defines:

            :attributes:
                | toggled_ports - List of handled connection toggles.
            :methods:
                | __init__ - Initializes mock container.
                | handle_connect_toggle - Records connection toggles.
                | get_version - Returns mock version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock connection tracker.

            :exceptions: None.
        '''
        self.toggled_ports: list[tuple[str, int]] = []

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Records connection parameters.

            :param port: Selected port.
            :param baudrate: Selected baud rate.
            :exceptions: None.
        '''
        self.toggled_ports.append((port, baudrate))

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockServerManager:
    '''
        Mock implementation of IVirtualServerManager.

        It defines:

            :attributes:
                | toggled_ports - List of toggled TCP ports.
                | running - Running status flag.
            :methods:
                | __init__ - Initializes mock container.
                | is_running - Returns running state.
                | toggle - Records toggle calls.
                | stop - Sets running to False.
                | get_version - Returns mock version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock server manager.

            :exceptions: None.
        '''
        self.toggled_ports: list[int] = []
        self.running: bool = False

    def is_running(self) -> bool:
        '''
            Checks running state.

            :return: True if running, False otherwise.
            :exceptions: None.
        '''
        return self.running

    def toggle(self, port: int) -> bool:
        '''
            Toggles server state.

            :param port: TCP port.
            :return: Updated running state.
            :exceptions: None.
        '''
        self.toggled_ports.append(port)
        self.running = not self.running
        return self.running

    def stop(self) -> None:
        '''
            Stops server.

            :exceptions: None.
        '''
        self.running = False

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockSerialPreferencesRepository:
    '''
        Mock implementation of ISerialPreferenceRepository.

        It defines:

            :attributes:
                | saved_preferences - Recorded saved preferences.
            :methods:
                | __init__ - Initializes mock container.
                | has_preference - Checks if preferences exist.
                | load_preference - Returns dummy preference.
                | save_preference - Records saved preference parameters.
                | get_version - Returns mock version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock repository.

            :exceptions: None.
        '''
        self.saved_preferences: list[tuple[str, int]] = []

    def has_preference(self) -> bool:
        '''
            Returns True if preferences were saved.

            :return: True if preference exists.
            :exceptions: None.
        '''
        return len(self.saved_preferences) > 0

    def load_preference(self) -> SerialPreference:
        '''
            Returns dummy preference.

            :return: SerialPreference instance.
            :exceptions: None.
        '''
        return SerialPreference(port='/dev/ttyUSB0', baud=115200)

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Saves preference parameters.

            :param preference: Selected preference.
            :return: True.
            :exceptions: None.
        '''
        self.saved_preferences.append((preference.port, preference.baud))
        return True

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockServerPreferencesRepository:
    '''
        Mock implementation of IServerPreferenceRepository.

        It defines:

            :attributes:
                | pref - Optional stored preference.
            :methods:
                | __init__ - Initializes mock container.
                | has_preference - Checks if preferences exist.
                | load_preference - Returns preference.
                | save_preference - Records saved preference parameters.
                | get_version - Returns mock version string.
    '''

    def __init__(
        self,
        pref: ServerPreference | None = None,
        should_fail_load: bool = False,
    ) -> None:
        '''
            Initializes mock repository.

            :param pref: Optional preference.
            :param should_fail_load: Flag causing load_preference to raise error.
            :exceptions: None.
        '''
        self.pref: ServerPreference | None = pref
        self.should_fail_load: bool = should_fail_load

    def has_preference(self) -> bool:
        '''
            Returns True if preference is configured.

            :return: True if preference exists.
            :exceptions: None.
        '''
        return self.pref is not None

    def load_preference(self) -> ServerPreference:
        '''
            Returns preference.

            :return: ServerPreference instance.
            :exceptions:
                | LookupError: If no preference is set.
                | RuntimeError: If should_fail_load is True.
        '''
        if self.should_fail_load:
            raise RuntimeError('Corrupted server preference')
        if self.pref is None:
            raise LookupError('No server preferences')
        return self.pref

    def save_preference(self, host: str, port: int = 8888) -> bool:
        '''
            Saves preference parameters.

            :param host: Selected host.
            :param port: Selected port.
            :return: True.
            :exceptions: None.
        '''
        self.pref = ServerPreference(host, port)
        return True

    def get_version(self) -> str:
        '''
            Returns mock version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class ActionCoordinatorTestCase(TestCase):
    '''
        Unit tests for ActionCoordinator operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies ActionCoordinator satisfies IActionDelegate.
                | test_handle_connect_toggle - Verifies connect toggling delegates to connection port and saves preferences.
                | test_handle_server_toggle - Verifies server toggling delegates to server manager with default port.
                | test_handle_server_toggle_with_custom_preference - Verifies server toggling uses configured preference.
                | test_handle_server_toggle_with_preference_load_exception - Verifies server toggling falls back to default port on error.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies ActionCoordinator satisfies IActionDelegate.

            :exceptions: None.
        '''
        connection_port = _MockConnectionPort()
        server_manager = _MockServerManager()
        serial_repo = _MockSerialPreferencesRepository()
        server_repo = _MockServerPreferencesRepository()
        coordinator = ActionCoordinator(
            connection_port=connection_port,
            server_manager=server_manager,
            serial_preferences=serial_repo,
            server_preferences=server_repo,
        )

        self.assertIsInstance(coordinator, IActionDelegate)
        self.assertEqual(coordinator.get_version(), '1.0.2')
        self.assertEqual(ActionCoordinator.DEFAULT_SERVER_PORT, 8888)

    def test_handle_connect_toggle(self) -> None:
        '''
            Verifies connect toggling delegates to connection port and saves preferences.

            :exceptions: None.
        '''
        connection_port = _MockConnectionPort()
        server_manager = _MockServerManager()
        serial_repo = _MockSerialPreferencesRepository()
        server_repo = _MockServerPreferencesRepository()
        coordinator = ActionCoordinator(
            connection_port=connection_port,
            server_manager=server_manager,
            serial_preferences=serial_repo,
            server_preferences=server_repo,
        )

        coordinator.handle_connect_toggle('/dev/ttyUSB0', 115200)
        self.assertEqual(connection_port.toggled_ports, [('/dev/ttyUSB0', 115200)])
        self.assertEqual(serial_repo.saved_preferences, [('/dev/ttyUSB0', 115200)])

    def test_handle_server_toggle(self) -> None:
        '''
            Verifies server toggling delegates to server manager with default port when no pref exists.

            :exceptions: None.
        '''
        connection_port = _MockConnectionPort()
        server_manager = _MockServerManager()
        serial_repo = _MockSerialPreferencesRepository()
        server_repo = _MockServerPreferencesRepository()
        coordinator = ActionCoordinator(
            connection_port=connection_port,
            server_manager=server_manager,
            serial_preferences=serial_repo,
            server_preferences=server_repo,
        )

        coordinator.handle_server_toggle()
        self.assertEqual(server_manager.toggled_ports, [8888])

    def test_handle_server_toggle_with_custom_preference(self) -> None:
        '''
            Verifies server toggling uses configured preference port.

            :exceptions: None.
        '''
        connection_port = _MockConnectionPort()
        server_manager = _MockServerManager()
        serial_repo = _MockSerialPreferencesRepository()
        server_repo = _MockServerPreferencesRepository(
            pref=ServerPreference(host='127.0.0.1', port=9000)
        )
        coordinator = ActionCoordinator(
            connection_port=connection_port,
            server_manager=server_manager,
            serial_preferences=serial_repo,
            server_preferences=server_repo,
        )

        coordinator.handle_server_toggle()
        self.assertEqual(server_manager.toggled_ports, [9000])

    def test_handle_server_toggle_with_preference_load_exception(self) -> None:
        '''
            Verifies server toggling falls back to default port on preference load error.

            :exceptions: None.
        '''
        connection_port = _MockConnectionPort()
        server_manager = _MockServerManager()
        serial_repo = _MockSerialPreferencesRepository()
        server_repo = _MockServerPreferencesRepository(
            pref=ServerPreference(host='127.0.0.1', port=9000),
            should_fail_load=True,
        )
        coordinator = ActionCoordinator(
            connection_port=connection_port,
            server_manager=server_manager,
            serial_preferences=serial_repo,
            server_preferences=server_repo,
        )

        coordinator.handle_server_toggle()
        self.assertEqual(server_manager.toggled_ports, [8888])


if __name__ == '__main__':
    unittest_main()
