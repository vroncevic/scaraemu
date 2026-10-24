# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for SimulationTickerDependencies parameter bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSimulationTickerDependencies(TestCase):
    '''
        Unit tests for SimulationTickerDependencies.

        It defines:

            :methods:
                | test_initialization_and_version - Verifies bundle values and get_version().
                | test_immutability - Verifies that attempting to mutate bundle raises FrozenInstanceError.
    '''

    def test_initialization_and_version(self) -> None:
        '''
            Verifies bundle values and get_version().

            :exceptions: None.
        '''
        mock_root = MagicMock()
        mock_engine = MagicMock(spec=IEmulationService)
        mock_canvas_xy = MagicMock(spec=ICanvasXY)
        mock_canvas_z = MagicMock(spec=ICanvasZ)
        mock_telemetry = MagicMock(spec=ITelemetryView)
        mock_queue = MagicMock(spec=IQueueDepthView)

        deps = SimulationTickerDependencies(
            root=mock_root,
            emulation_service=mock_engine,
            canvas_xy=mock_canvas_xy,
            canvas_z=mock_canvas_z,
            telemetry_view=mock_telemetry,
            queue_view=mock_queue,
            interval_ms=50,
        )

        self.assertEqual(deps.interval_ms, 50)
        self.assertEqual(deps.get_version(), '1.0.2')

    def test_immutability(self) -> None:
        '''
            Verifies that attempting to mutate bundle raises FrozenInstanceError.

            :exceptions: None.
        '''
        deps = SimulationTickerDependencies(
            root=MagicMock(),
            emulation_service=MagicMock(spec=IEmulationService),
            canvas_xy=MagicMock(spec=ICanvasXY),
            canvas_z=MagicMock(spec=ICanvasZ),
            telemetry_view=MagicMock(spec=ITelemetryView),
            queue_view=MagicMock(spec=IQueueDepthView),
        )

        with self.assertRaises(FrozenInstanceError):
            deps.interval_ms = 100  # type: ignore[misc]


if __name__ == '__main__':
    unittest_main()
