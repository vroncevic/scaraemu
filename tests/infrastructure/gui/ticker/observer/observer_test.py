# -*- coding: UTF-8 -*-

'''
Module
    observer_test.py
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
    Unit tests for SimulationViewObserver component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.ticker.observer.iobserver import ISimulationViewObserver
from scaraemu.infrastructure.gui.ticker.observer.observer import SimulationViewObserver
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSimulationViewObserver(TestCase):
    '''
        Unit tests for SimulationViewObserver.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conformance to ISimulationViewObserver.
                | test_update_views - Verifies view observer dispatches to all viewports.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conformance to ISimulationViewObserver.

            :exceptions: None.
        '''
        observer = SimulationViewObserver(
            canvas_xy=MagicMock(spec=ICanvasXY),
            canvas_z=MagicMock(spec=ICanvasZ),
            telemetry_view=MagicMock(spec=ITelemetryView),
            queue_view=MagicMock(spec=IQueueDepthView),
        )
        self.assertIsInstance(observer, ISimulationViewObserver)

    def test_update_views(self) -> None:
        '''
            Verifies view observer dispatches to all viewports.

            :exceptions: None.
        '''
        mock_xy = MagicMock(spec=ICanvasXY)
        mock_z = MagicMock(spec=ICanvasZ)
        mock_telem_view = MagicMock(spec=ITelemetryView)
        mock_queue = MagicMock(spec=IQueueDepthView)

        observer = SimulationViewObserver(
            canvas_xy=mock_xy,
            canvas_z=mock_z,
            telemetry_view=mock_telem_view,
            queue_view=mock_queue,
        )

        mock_telem = MagicMock(spec=Telemetry)
        mock_state = MagicMock(spec=SimulationState)
        mock_state.queue_depth = 5

        observer.update_views(telemetry=mock_telem, simulation_state=mock_state)

        mock_xy.redraw.assert_called_once_with(
            pose=mock_telem.pose,
            joints=mock_telem.joints,
            trail_points=mock_state.trail_points,
            current_target=mock_state.current_target,
            planned_path=mock_state.planned_path,
        )
        mock_z.redraw.assert_called_once_with(
            pose=mock_telem.pose,
            current_target=mock_state.current_target,
        )
        mock_telem_view.update_telemetry.assert_called_once_with(mock_telem)
        mock_queue.update_queue_depth.assert_called_once_with(5)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        observer = SimulationViewObserver(
            canvas_xy=MagicMock(spec=ICanvasXY),
            canvas_z=MagicMock(spec=ICanvasZ),
            telemetry_view=MagicMock(spec=ITelemetryView),
            queue_view=MagicMock(spec=IQueueDepthView),
        )
        self.assertEqual(observer.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
