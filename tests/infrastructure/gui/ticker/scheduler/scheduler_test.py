# -*- coding: UTF-8 -*-

'''
Module
    scheduler_test.py
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
    Unit tests for TkinterIntervalScheduler component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.ticker.scheduler.ischeduler import ITickerScheduler
from scaraemu.infrastructure.gui.ticker.scheduler.scheduler import TkinterIntervalScheduler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockListener:
    '''
        Mock listener for testing scheduler loop callbacks.

        It defines:

            :methods:
                | on_tick - Records tick event count.
                | get_version - Returns version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock listener tick counter.

            :exceptions: None.
        '''
        self.tick_count: int = 0

    def on_tick(self) -> None:
        '''
            Records tick event count.

            :exceptions: None.
        '''
        self.tick_count += 1

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestTkinterIntervalScheduler(TestCase):
    '''
        Unit tests for TkinterIntervalScheduler.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conformance to ITickerScheduler protocol.
                | test_start_and_run_tick - Verifies loop starts and dispatches tick.
                | test_stop - Verifies loop terminates on stop.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conformance to ITickerScheduler protocol.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        scheduler = TkinterIntervalScheduler(root=mock_root)
        self.assertIsInstance(scheduler, ITickerScheduler)

    def test_start_and_run_tick(self) -> None:
        '''
            Verifies loop starts and dispatches tick.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        scheduler = TkinterIntervalScheduler(root=mock_root)
        listener = _MockListener()

        scheduler.start(interval_ms=50, listener=listener)
        self.assertEqual(listener.tick_count, 1)
        mock_root.after.assert_called_once_with(50, scheduler.run_tick)

    def test_stop(self) -> None:
        '''
            Verifies loop terminates on stop.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        scheduler = TkinterIntervalScheduler(root=mock_root)
        listener = _MockListener()

        scheduler.start(interval_ms=50, listener=listener)
        mock_root.reset_mock()

        scheduler.stop()
        scheduler.run_tick()
        mock_root.after.assert_not_called()

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        scheduler = TkinterIntervalScheduler(root=mock_root)
        self.assertEqual(scheduler.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
