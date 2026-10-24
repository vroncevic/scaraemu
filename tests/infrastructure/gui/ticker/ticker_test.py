# -*- coding: UTF-8 -*-

'''
Module
    ticker_test.py
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
    Unit tests for SimulationTicker component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.ticker.iticker import ISimulationTicker
from scaraemu.infrastructure.gui.ticker.observer.iobserver import ISimulationViewObserver
from scaraemu.infrastructure.gui.ticker.scheduler.ilistener import ITickerListener
from scaraemu.infrastructure.gui.ticker.scheduler.ischeduler import ITickerScheduler
from scaraemu.infrastructure.gui.ticker.ticker import SimulationTicker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSimulationTicker(TestCase):
    '''
        Unit tests for SimulationTicker.

        It defines:

            :methods:
                | setUp - Prepares test dependencies.
                | test_structural_conformance - Verifies conformance to ISimulationTicker protocol.
                | test_listener_conformance - Verifies conformance to ITickerListener protocol.
                | test_start_and_stop - Verifies start and stop delegate to scheduler.
                | test_on_tick_execution - Verifies simulation stepping and observer update.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Prepares test dependencies.

            :exceptions: None.
        '''
        self._scheduler = MagicMock(spec=ITickerScheduler)
        self._engine = MagicMock(spec=IEmulationService)
        self._observer = MagicMock(spec=ISimulationViewObserver)
        self._ticker = SimulationTicker(
            scheduler=self._scheduler,
            emulation_service=self._engine,
            view_observer=self._observer,
            interval_ms=25,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies conformance to ISimulationTicker protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._ticker, ISimulationTicker)

    def test_listener_conformance(self) -> None:
        '''
            Verifies conformance to ITickerListener protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._ticker, ITickerListener)

    def test_start_and_stop(self) -> None:
        '''
            Verifies start and stop delegate to scheduler.

            :exceptions: None.
        '''
        self._ticker.start()
        self._scheduler.start.assert_called_once_with(25, self._ticker)

        self._ticker.stop()
        self._scheduler.stop.assert_called_once()

    def test_on_tick_execution(self) -> None:
        '''
            Verifies simulation stepping and observer update.

            :exceptions: None.
        '''
        mock_telem = MagicMock(spec=Telemetry)
        mock_sim_state = MagicMock(spec=SimulationState)

        self._engine.get_telemetry.return_value = mock_telem
        self._engine.get_simulation_state.return_value = mock_sim_state

        self._ticker.on_tick()

        self._engine.step.assert_called_once_with(0.025)
        self._observer.update_views.assert_called_once_with(mock_telem, mock_sim_state)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self._ticker.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
