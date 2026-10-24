# -*- coding: UTF-8 -*-

'''
Module
    ticker.py
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
    Periodic simulation and visualizer update ticker loop for GUI.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.ticker.observer.iobserver import ISimulationViewObserver
from scaraemu.infrastructure.gui.ticker.scheduler.ischeduler import ITickerScheduler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SimulationTicker:
    '''
        Drives the periodic simulation step and visualizer widget redraw loop.

        It defines:

            :attributes:
                | _scheduler - Periodic loop timing scheduler.
                | _emulation_service - Digital twin simulation engine.
                | _view_observer - Composite visualizer and telemetry views observer.
                | _interval_ms - Periodic timer tick interval in milliseconds.
            :methods:
                | __init__ - Initializes ticker with scheduler, simulation engine, and view observer.
                | start - Starts periodic ticking loop using injected scheduler.
                | stop - Stops periodic ticking loop.
                | on_tick - Executes a single simulation step and notifies view observer.
                | get_version - Returns ticker component version string.
    '''

    _scheduler: ITickerScheduler
    _emulation_service: IEmulationService
    _view_observer: ISimulationViewObserver
    _interval_ms: int

    def __init__(
        self,
        *,
        scheduler: ITickerScheduler,
        emulation_service: IEmulationService,
        view_observer: ISimulationViewObserver,
        interval_ms: int = 25,
    ) -> None:
        '''
            Initializes ticker with scheduler, simulation engine, and view observer.

            :param scheduler: Periodic loop timing scheduler interface.
            :param emulation_service: Digital twin simulation engine interface.
            :param view_observer: Composite visualizer and telemetry views observer.
            :param interval_ms: Periodic timer tick interval in milliseconds.
            :exceptions: None.
        '''
        self._scheduler: Final[ITickerScheduler] = scheduler
        self._emulation_service: Final[IEmulationService] = emulation_service
        self._view_observer: Final[ISimulationViewObserver] = view_observer
        self._interval_ms: Final[int] = interval_ms

    def start(self) -> None:
        '''
            Starts periodic ticking loop using injected scheduler.

            :exceptions: None.
        '''
        self._scheduler.start(self._interval_ms, self)

    def stop(self) -> None:
        '''
            Stops periodic ticking loop.

            :exceptions: None.
        '''
        self._scheduler.stop()

    def on_tick(self) -> None:
        '''
            Executes a single simulation step and notifies view observer.

            :exceptions: None.
        '''
        self._emulation_service.step(self._interval_ms / 1000.0)
        telem: Telemetry = self._emulation_service.get_telemetry()
        sim_state: SimulationState = self._emulation_service.get_simulation_state()
        self._view_observer.update_views(telem, sim_state)

    def get_version(self) -> str:
        '''
            Returns ticker component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
