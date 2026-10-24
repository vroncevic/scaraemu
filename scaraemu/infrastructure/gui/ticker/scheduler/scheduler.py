# -*- coding: UTF-8 -*-

'''
Module
    scheduler.py
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
    Concrete interval scheduler driving periodic loops via Tkinter root after().
'''

from __future__ import annotations

from tkinter import Tk
from typing import Final

from scaraemu.infrastructure.gui.ticker.scheduler.ilistener import ITickerListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TkinterIntervalScheduler:
    '''
        Drives recurring periodic tick notifications using Tkinter after() timer.

        It defines:

            :attributes:
                | _root - Injected Tkinter root window reference.
                | _interval_ms - Configured tick interval in milliseconds.
                | _running - Active ticking state flag.
                | _has_listener - Flag indicating if a listener is registered.
                | _listener - Active listener sink notified on each tick.
            :methods:
                | __init__ - Initializes scheduler with Tkinter root window.
                | start - Starts periodic timer loop with specified interval and listener.
                | stop - Stops recurring timer loop.
                | run_tick - Executes a single tick and reschedules next iteration.
                | get_version - Returns scheduler component version string.
    '''

    _root: Tk
    _interval_ms: int
    _running: bool
    _has_listener: bool
    _listener: ITickerListener

    def __init__(self, root: Tk) -> None:
        '''
            Initializes scheduler with Tkinter root window.

            :param root: Injected Tkinter root window reference.
            :exceptions: None.
        '''
        self._root: Final[Tk] = root
        self._interval_ms = 25
        self._running = False
        self._has_listener = False

    def start(self, interval_ms: int, listener: ITickerListener) -> None:
        '''
            Starts periodic timer loop with specified interval and listener.

            :param interval_ms: Interval between ticks in milliseconds.
            :param listener: Listener notified on each timer interval.
            :exceptions: None.
        '''
        self._interval_ms = interval_ms
        self._listener = listener
        self._has_listener = True
        self._running = True
        self.run_tick()

    def stop(self) -> None:
        '''
            Stops recurring timer loop.

            :exceptions: None.
        '''
        self._running = False

    def run_tick(self) -> None:
        '''
            Executes a single tick and reschedules next iteration if still running.

            :exceptions: None.
        '''
        if self._running and self._has_listener:
            self._listener.on_tick()
            self._root.after(self._interval_ms, self.run_tick)

    def get_version(self) -> str:
        '''
            Returns scheduler component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
