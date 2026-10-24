# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Coordinates DSL script and compiled plan loading actions.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter
from scaraemu.infrastructure.streaming.motion.icoordinator import IMotionCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptLoaderCoordinator:
    '''
        Coordinates DSL script and compiled plan loading actions.

        It defines:

            :attributes:
                | _script_loader - DSL script and plan loading adapter.
                | _emulation_queue - FIFO motion emulation queue.
                | _motion_port - Hardware bridge motion streaming port.
                | _log_listener - Logging sink for host diagnostics.
            :methods:
                | __init__ - Initializes script loader coordinator with collaborators.
                | handle_load_script - Loads .scara or JSON plan and enqueues trajectory.
                | get_version - Returns coordinator component version string.
    '''

    _script_loader: IScriptLoaderAdapter
    _emulation_queue: IEmulationQueue
    _motion_port: IMotionCoordinator
    _log_listener: ILogListener

    def __init__(
        self,
        *,
        script_loader: IScriptLoaderAdapter,
        emulation_queue: IEmulationQueue,
        motion_port: IMotionCoordinator,
        log_listener: ILogListener,
    ) -> None:
        '''
            Initializes script loader coordinator with loader, queue, and logger.

            :param script_loader: Script and plan trajectory loader adapter.
            :param emulation_queue: FIFO motion emulation queue.
            :param motion_port: Hardware bridge motion streaming port.
            :param log_listener: Logging listener for host diagnostics.
            :exceptions: None.
        '''
        self._script_loader: Final[IScriptLoaderAdapter] = script_loader
        self._emulation_queue: Final[IEmulationQueue] = emulation_queue
        self._motion_port: Final[IMotionCoordinator] = motion_port
        self._log_listener: Final[ILogListener] = log_listener

    def handle_load_script(self, script_path: str) -> None:
        '''
            Loads and parses .scara script or plan JSON file and enqueues trajectory.

            :param script_path: Path to script or plan file.
            :exceptions: None.
        '''
        poses: list[ScaraPose] = self._script_loader.load_from_file(
            filepath=script_path
        )

        if poses:
            for pose in poses:
                self._emulation_queue.enqueue_waypoint(pose)
            self._motion_port.enqueue_hardware_trajectory(poses)
            self._log_listener.append_log(
                f'[HOST]: Loaded {len(poses)} waypoints from {script_path}',
                'info',
            )
        else:
            self._log_listener.append_log(
                f'[HOST]: No waypoints loaded from {script_path}',
                'warn',
            )

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
