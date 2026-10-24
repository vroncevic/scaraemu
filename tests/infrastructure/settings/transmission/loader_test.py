# -*- coding: UTF-8 -*-

'''
Module
    loader_test.py
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
    Unit tests for TransmissionLoader.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from ats_utilities.context.factory import ContextBundleFactory
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters

from scaraemu.infrastructure.settings.transmission.loader import TransmissionLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransmissionLoader(TestCase):
    '''
        Unit tests for TransmissionLoader.

        It defines:

            :methods:
                | setUp - Initializes loader and paths to test config files.
                | test_load_transmission_with_valid_files - Verifies loading transmission parameters from valid JSON.
                | test_load_transmission_with_missing_files_returns_default - Verifies fallback to default transmission parameters.
                | test_load_transmission_exception_fallback - Verifies fallback on exception.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes loader and paths to test config files.

            :exceptions: None.
        '''
        self._context = ContextBundleFactory.create_bundle()
        self._loader = TransmissionLoader(self._context)
        root_dir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
        self._config_path = join(root_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry.json')
        self._scheme_path = join(
            root_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry_scheme.json'
        )

    def test_load_transmission_with_valid_files(self) -> None:
        '''
            Verifies loading transmission parameters from valid JSON.

            :exceptions: None.
        '''
        trans: TransmissionParameters = self._loader.load_transmission(
            config_path=self._config_path,
            scheme_path=self._scheme_path,
        )

        self.assertIsInstance(trans, TransmissionParameters)
        self.assertEqual(trans.steps_per_rev, 200.0)
        self.assertEqual(trans.microstepping, 16.0)
        self.assertEqual(trans.gear_ratio_j1, 4.0)
        self.assertEqual(trans.gear_ratio_j2, 4.0)
        self.assertEqual(trans.gear_ratio_j4, 1.0)
        self.assertEqual(trans.leadscrew_pitch_z, 8.0)

    def test_load_transmission_with_missing_files_returns_default(self) -> None:
        '''
            Verifies fallback to default transmission parameters.

            :exceptions: None.
        '''
        trans: TransmissionParameters = self._loader.load_transmission(
            config_path='/nonexistent/config.json',
            scheme_path='/nonexistent/scheme.json',
        )

        self.assertIsInstance(trans, TransmissionParameters)
        self.assertEqual(trans.steps_per_rev, 200.0)
        self.assertEqual(trans.microstepping, 16.0)

    @patch('scaraemu.infrastructure.settings.transmission.loader.Loader.load_configuration', side_effect=Exception('loader failure'))
    def test_load_transmission_exception_fallback(self, _mock_load: MagicMock) -> None:
        '''
            Verifies fallback to default transmission parameters on exception.

            :param _mock_load: Mocked loader.
            :exceptions: None.
        '''
        trans: TransmissionParameters = self._loader.load_transmission(
            config_path=self._config_path,
            scheme_path=self._scheme_path,
        )
        self.assertIsInstance(trans, TransmissionParameters)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(self._loader.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
