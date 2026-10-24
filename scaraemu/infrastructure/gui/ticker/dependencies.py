# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Immutable dependencies bundle for simulation ticker subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Tk

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class SimulationTickerDependencies:
    '''
        Immutable parameter bundle encapsulating external ticker collaborators.

        It defines:

            :attributes:
                | root - Tkinter root window reference for event loop timer.
                | emulation_service - Digital twin simulation engine.
                | canvas_xy - Planar XY top-down view port.
                | canvas_z - Elevation Z side view port.
                | telemetry_view - Telemetry monitor view port.
                | queue_view - Trajectory queue depth view port.
                | interval_ms - Periodic timer interval in milliseconds.
            :methods:
                | get_version - Returns dependencies bundle version string.
    '''

    root: Tk
    emulation_service: IEmulationService
    canvas_xy: ICanvasXY
    canvas_z: ICanvasZ
    telemetry_view: ITelemetryView
    queue_view: IQueueDepthView
    interval_ms: int = 25

    def get_version(self) -> str:
        '''
            Returns dependencies bundle version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
