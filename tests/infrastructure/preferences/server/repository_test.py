# -*- coding: UTF-8 -*-

'''
Module
    repository_test.py
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
    Unit tests for ServerPreferenceRepository.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock
from unittest.mock import patch

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.infrastructure.preferences.exceptions.preference_not_found_error import PreferenceNotFoundError
from scaraemu.infrastructure.preferences.server.irepository import IServerPreferenceRepository
from scaraemu.infrastructure.preferences.server.preference import ServerPreference
from scaraemu.infrastructure.preferences.server.repository import ServerPreferenceRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerPreferenceRepository(TestCase):
    '''
        Unit tests for ServerPreferenceRepository.

        It defines:

            :methods:
                | setUp - Sets up temporary directory and ATS context bundle.
                | tearDown - Cleans up temporary directory.
                | test_protocol_conformance - Tests that repository implements IServerPreferenceRepository.
                | test_has_preference_when_file_absent - Tests has_preference returns False when configuration file does not exist.
                | test_load_preference_raises_when_file_absent - Tests load_preference raises PreferenceNotFoundError when file is missing.
                | test_save_and_load_preference_roundtrip - Tests saving and loading valid server preferences.
                | test_save_preference_invalid - Tests that saving empty host or invalid port is rejected.
                | test_load_preference_corrupt_file_raises - Tests that corrupted configuration files raise PreferenceNotFoundError.
                | test_get_version - Tests component version query.
                | test_str_representation - Tests string representation of repository.
    '''

    def setUp(self) -> None:
        '''
            Sets up temporary directory and ATS context bundle.

            :exceptions: None.
        '''
        self._temp_dir = TemporaryDirectory()
        self._config_path = Path(self._temp_dir.name) / 'server_config.json'
        self._context: ContextBundle = ContextBundleFactory.create_bundle()
        self._repo = ServerPreferenceRepository(self._config_path, self._context)

    def tearDown(self) -> None:
        '''
            Cleans up temporary directory.

            :exceptions: None.
        '''
        self._temp_dir.cleanup()

    def test_protocol_conformance(self) -> None:
        '''
            Tests that repository implements IServerPreferenceRepository.

            :exceptions: None.
        '''
        self.assertIsInstance(self._repo, IServerPreferenceRepository)

    def test_has_preference_when_file_absent(self) -> None:
        '''
            Tests has_preference returns False when configuration file does not exist.

            :exceptions: None.
        '''
        self.assertFalse(self._repo.has_preference())

    def test_load_preference_raises_when_file_absent(self) -> None:
        '''
            Tests load_preference raises PreferenceNotFoundError when file is missing.

            :exceptions: None.
        '''
        with self.assertRaises(PreferenceNotFoundError):
            self._repo.load_preference()

    def test_save_and_load_preference_roundtrip(self) -> None:
        '''
            Tests saving and loading valid server preferences.

            :exceptions: None.
        '''
        save_success = self._repo.save_preference('127.0.0.1', 8888)
        self.assertTrue(save_success)
        self.assertTrue(self._repo.has_preference())

        pref: ServerPreference = self._repo.load_preference()
        self.assertEqual(pref.host, '127.0.0.1')
        self.assertEqual(pref.port, 8888)

    def test_save_preference_invalid(self) -> None:
        '''
            Tests that saving empty host or invalid port is rejected.

            :exceptions: None.
        '''
        self.assertFalse(self._repo.save_preference('', 8888))
        self.assertFalse(self._repo.save_preference('127.0.0.1', 0))
        self.assertFalse(self._repo.save_preference('127.0.0.1', -1))

    def test_load_preference_corrupt_file_raises(self) -> None:
        '''
            Tests that corrupted configuration files raise PreferenceNotFoundError.

            :exceptions: None.
        '''
        self._config_path.write_text('INVALID_JSON', encoding='utf-8')
        self.assertFalse(self._repo.has_preference())
        with self.assertRaises(PreferenceNotFoundError):
            self._repo.load_preference()

    @patch('scaraemu.infrastructure.preferences.server.repository.Loader.load_configuration', side_effect=Exception('loader failure'))
    def test_has_preference_exception(self, _mock_load: MagicMock) -> None:
        '''
            Tests has_preference returns False when loader raises unexpected exception.

            :param _mock_load: Mocked load_configuration method.
            :exceptions: None.
        '''
        self._repo.save_preference('127.0.0.1', 8888)
        self.assertFalse(self._repo.has_preference())

    @patch('scaraemu.infrastructure.preferences.server.repository.Loader.load_configuration', side_effect=RuntimeError('IO read failure'))
    def test_load_preference_unexpected_exception(self, _mock_load: MagicMock) -> None:
        '''
            Tests load_preference wraps unexpected Exception in PreferenceNotFoundError.

            :param _mock_load: Mocked load_configuration method.
            :exceptions: None.
        '''
        self._repo.save_preference('127.0.0.1', 8888)
        with self.assertRaises(PreferenceNotFoundError):
            self._repo.load_preference()

    @patch('scaraemu.infrastructure.preferences.server.repository.Storer.store_configuration', side_effect=Exception('storer failure'))
    def test_save_preference_exception(self, _mock_store: MagicMock) -> None:
        '''
            Tests save_preference returns False when storer raises unexpected exception.

            :param _mock_store: Mocked store_configuration method.
            :exceptions: None.
        '''
        self.assertFalse(self._repo.save_preference('127.0.0.1', 8888))

    def test_get_version(self) -> None:
        '''
            Tests component version query.

            :exceptions: None.
        '''
        self.assertEqual(self._repo.get_version(), '1.0.2')

    def test_str_representation(self) -> None:
        '''
            Tests string representation of repository.

            :exceptions: None.
        '''
        self.assertIn('ServerPreferenceRepository', str(self._repo))


if __name__ == '__main__':
    unittest_main()
