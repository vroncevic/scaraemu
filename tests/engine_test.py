# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for root SCARAEmu engine.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaraemu.engine import SCARAEmu
from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.factory import SCARAEmuBundleFactory
from scaraemu.setup.options import SCARAEmuBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAEmuTestCase(TestCase):
    '''
        Unit tests for SCARAEmu application engine.

        It defines:

            :methods:
                | setUp - Prepares real bundle and engine instance.
                | test_initialization - Tests initialization status.
                | test_get_version - Tests engine version string retrieval.
                | test_process_success - Tests successful process execution.
                | test_process_failure - Tests failed command execution.
                | test_process_when_not_initialized - Tests process handling when engine is uninitialized.
                | test_init_invalid_bundle - Tests handling of invalid bundle parameter.
    '''

    _bundle: SCARAEmuBundle
    _engine: SCARAEmu

    def setUp(self) -> None:
        '''
            Prepares real bundle and engine instance.

            :exceptions: None.
        '''
        self._bundle = SCARAEmuBundleFactory.create(SCARAEmuBundleOptions())
        self._engine = SCARAEmu(self._bundle)

    def test_initialization(self) -> None:
        '''
            Tests initialization status.

            :exceptions: None.
        '''
        self.assertTrue(self._engine.is_initialized())

    def test_get_version(self) -> None:
        '''
            Tests engine version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self._engine.get_version(), '1.0.2')

    def test_process_success(self) -> None:
        '''
            Tests successful process execution.

            :exceptions: None.
        '''
        mock_cli = MagicMock()
        mock_cli.run.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}
        self._engine._cli = mock_cli
        self.assertTrue(self._engine.process())

    def test_process_failure(self) -> None:
        '''
            Tests failed command execution.

            :exceptions: None.
        '''
        mock_cli = MagicMock()
        mock_cli.run.return_value = {'returncode': 1, 'stdout': '', 'stderr': 'command error'}
        self._engine._cli = mock_cli
        self.assertFalse(self._engine.process())

    def test_process_when_not_initialized(self) -> None:
        '''
            Tests process handling when engine is uninitialized.

            :exceptions: None.
        '''
        self._engine._is_initialized = False
        self.assertFalse(self._engine.process())

    def test_init_invalid_bundle(self) -> None:
        '''
            Tests handling of invalid bundle parameter.

            :exceptions: None.
        '''
        uninitialized_engine = SCARAEmu(None)  # type: ignore[arg-type]
        self.assertFalse(uninitialized_engine.is_initialized())

    @patch('scaraemu.engine.SCARAEmuBundleValidator.validate', side_effect=Exception('unexpected init error'))
    def test_init_unexpected_exception(self, _mock_validator: MagicMock) -> None:
        '''
            Tests engine initialization when unexpected exception is raised.

            :param _mock_validator: Mocked validator instance.
            :exceptions: None.
        '''
        engine = SCARAEmu(self._bundle)
        self.assertFalse(engine.is_initialized())

    def test_process_ats_error(self) -> None:
        '''
            Tests process handling when command execution raises ATSValueError.

            :exceptions: None.
        '''
        mock_cli = MagicMock()
        mock_cli.run.side_effect = ATSValueError('ATS error occurred')
        self._engine._cli = mock_cli
        self.assertFalse(self._engine.process())

    def test_process_unexpected_exception(self) -> None:
        '''
            Tests process handling when command execution raises unexpected Exception.

            :exceptions: None.
        '''
        mock_cli = MagicMock()
        mock_cli.run.side_effect = Exception('Unexpected execution failure')
        self._engine._cli = mock_cli
        self.assertFalse(self._engine.process())


if __name__ == '__main__':
    unittest_main()
