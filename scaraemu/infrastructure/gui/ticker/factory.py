# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring simulation ticker components.
'''

from __future__ import annotations

from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
from scaraemu.infrastructure.gui.ticker.observer.observer import SimulationViewObserver
from scaraemu.infrastructure.gui.ticker.scheduler.scheduler import TkinterIntervalScheduler
from scaraemu.infrastructure.gui.ticker.ticker import SimulationTicker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SimulationTickerFactory:
    '''
        Factory providing configured SimulationTicker instances.

        It defines:

            :methods:
                | create - Wires and returns a new SimulationTicker instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: SimulationTickerDependencies,
    ) -> SimulationTicker:
        '''
            Wires scheduler, view observer, and engine into a SimulationTicker.

            :param dependencies: External collaborators parameter bundle.
            :return: Fully wired SimulationTicker instance.
            :exceptions: None.
        '''
        scheduler: TkinterIntervalScheduler = TkinterIntervalScheduler(
            root=dependencies.root,
        )
        observer: SimulationViewObserver = SimulationViewObserver(
            canvas_xy=dependencies.canvas_xy,
            canvas_z=dependencies.canvas_z,
            telemetry_view=dependencies.telemetry_view,
            queue_view=dependencies.queue_view,
        )
        return SimulationTicker(
            scheduler=scheduler,
            emulation_service=dependencies.emulation_service,
            view_observer=observer,
            interval_ms=dependencies.interval_ms,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
