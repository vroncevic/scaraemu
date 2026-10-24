# -*- coding: UTF-8 -*-

'''
Module
    ischeduler_test.py
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
    Unit tests for ITickerScheduler protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.ticker.scheduler.ilistener import ITickerListener
from scaraemu.infrastructure.gui.ticker.scheduler.ischeduler import ITickerScheduler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingScheduler:
    '''
        Mock conforming to ITickerScheduler protocol.

        It defines:

            :methods:
                | start - Starts scheduling.
                | stop - Stops scheduling.
                | run_tick - Executes a tick.
                | get_version - Returns version string.
    '''

    def start(self, interval_ms: int, listener: ITickerListener) -> None:
        '''
            Starts scheduling.

            :param interval_ms: Tick interval in ms.
            :param listener: Injected ticker listener.
            :exceptions: None.
        '''
        _ = (interval_ms, listener)

    def stop(self) -> None:
        '''
            Stops scheduling.

            :exceptions: None.
        '''

    def run_tick(self) -> None:
        '''
            Executes a tick.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _NonConformingScheduler:
    '''
        Mock non-conforming to ITickerScheduler protocol.

        It defines:

            :methods:
                | pause - Pauses scheduling.
                | get_version - Returns version string.
    '''

    def pause(self) -> None:
        '''
            Pauses scheduling.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestITickerScheduler(TestCase):
    '''
        Unit tests for ITickerScheduler structural protocol verification.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conforming class satisfies protocol.
                | test_non_conforming_rejection - Verifies non-conforming class fails protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conforming class satisfies protocol.

            :exceptions: None.
        '''
        scheduler = _ConformingScheduler()
        self.assertIsInstance(scheduler, ITickerScheduler)

    def test_non_conforming_rejection(self) -> None:
        '''
            Verifies non-conforming class fails protocol.

            :exceptions: None.
        '''
        non_conforming = _NonConformingScheduler()
        self.assertNotIsInstance(non_conforming, ITickerScheduler)


if __name__ == '__main__':
    unittest_main()
