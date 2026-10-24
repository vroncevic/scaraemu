# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SimulationTickerFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
from scaraemu.infrastructure.gui.ticker.factory import SimulationTickerFactory
from scaraemu.infrastructure.gui.ticker.iticker import ISimulationTicker
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSimulationTickerFactory(TestCase):
    '''
        Unit tests for SimulationTickerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates a valid ISimulationTicker.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory instantiates a valid ISimulationTicker.

            :exceptions: None.
        '''
        deps = SimulationTickerDependencies(
            root=MagicMock(),
            emulation_service=MagicMock(spec=IEmulationService),
            canvas_xy=MagicMock(spec=ICanvasXY),
            canvas_z=MagicMock(spec=ICanvasZ),
            telemetry_view=MagicMock(spec=ITelemetryView),
            queue_view=MagicMock(spec=IQueueDepthView),
            interval_ms=30,
        )

        ticker = SimulationTickerFactory.create(dependencies=deps)
        self.assertIsInstance(ticker, ISimulationTicker)
        self.assertEqual(ticker.get_version(), '1.0.2')

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(SimulationTickerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
