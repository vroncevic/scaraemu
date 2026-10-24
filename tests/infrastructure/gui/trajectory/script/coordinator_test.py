# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for ScriptLoaderCoordinator.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate
from scaraemu.infrastructure.gui.trajectory.script.coordinator import ScriptLoaderCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockScriptLoaderAdapter:
    '''
        Mock script loader returning preset poses based on filepath.
    '''

    def __init__(self) -> None:
        self.return_empty: bool = False

    def load_from_text(self, source: str) -> list[ScaraPose]:
        '''
            Loads from text.
        '''
        _ = source
        return []

    def load_from_file(self, filepath: str) -> list[ScaraPose]:
        '''
            Tests load from file.

            :param filepath: Input filepath.
            :exceptions: None.
        '''
        _ = filepath
        if self.return_empty:
            return []
        return [
            ScaraPose(x=10.0, y=20.0, z=5.0, phi=0.0),
            ScaraPose(x=30.0, y=40.0, z=10.0, phi=1.0),
        ]

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockEmulationQueue:
    '''
        Mock emulation queue recording enqueued poses.
    '''

    def __init__(self) -> None:
        self.poses: list[ScaraPose] = []

    def enqueue_waypoint(self, waypoint: ScaraPose) -> bool:
        '''
            Enqueues waypoint.
        '''
        self.poses.append(waypoint)
        return True

    def clear_queue(self) -> None:
        '''
            Clears queue.
        '''
        self.poses.clear()

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockHardwareMotionPort:
    '''
        Mock motion port capturing hardware trajectory enqueueing.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.trajectories: list[list[ScaraPose]] = []

    def enqueue_hardware_trajectory(self, waypoints: list[ScaraPose]) -> None:
        '''
            Tests enqueue hardware trajectory.

            :param waypoints: Input waypoints.
            :exceptions: None.
        '''
        self.trajectories.append(waypoints)

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockLogListener:
    '''
        Mock log listener capturing logged messages and levels.
    '''

    def __init__(self) -> None:
        '''
            Tests init.

            :exceptions: None.
        '''
        self.logs: list[tuple[str, str]] = []

    def append_log(self, message: str, level: str) -> None:
        '''
            Tests append log.

            :param message: Input message.
            :param level: Input level.
            :exceptions: None.
        '''
        self.logs.append((message, level))

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestScriptLoaderCoordinator(TestCase):
    '''
        Unit tests verifying ScriptLoaderCoordinator behavior.

        It defines:

            :methods:
                | setUp - Tests setUp.
                | test_structural_protocol_conformance - Verifies ScriptLoaderCoordinator satisfies IScriptLoaderDelegate.
                | test_handle_load_script_success - Verifies loaded poses are appended to queue, sent to motion port, and logged.
                | test_handle_load_script_empty - Verifies empty loaded poses logs warning and does not enqueue.
                | test_get_version - Verifies get_version returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Tests setUp.

            :exceptions: None.
        '''
        self.loader = _MockScriptLoaderAdapter()
        self.queue = _MockEmulationQueue()
        self.motion_port = _MockHardwareMotionPort()
        self.logger = _MockLogListener()
        self.coordinator = ScriptLoaderCoordinator(
            script_loader=self.loader,
            emulation_queue=self.queue,
            motion_port=self.motion_port,
            log_listener=self.logger,
        )

    def test_structural_protocol_conformance(self) -> None:
        '''
            Verifies ScriptLoaderCoordinator satisfies IScriptLoaderDelegate.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IScriptLoaderDelegate)

    def test_handle_load_script_success(self) -> None:
        '''
            Verifies loaded poses are appended to queue, sent to motion port, and logged.

            :exceptions: None.
        '''
        self.coordinator.handle_load_script('/path/to/script.scara')
        self.assertEqual(len(self.queue.poses), 2)
        self.assertEqual(len(self.motion_port.trajectories), 1)
        self.assertEqual(len(self.logger.logs), 1)
        self.assertIn('Loaded 2 waypoints', self.logger.logs[0][0])
        self.assertEqual(self.logger.logs[0][1], 'info')

    def test_handle_load_script_empty(self) -> None:
        '''
            Verifies empty loaded poses logs warning and does not enqueue.

            :exceptions: None.
        '''
        self.loader.return_empty = True
        self.coordinator.handle_load_script('/path/to/empty.scara')
        self.assertEqual(len(self.queue.poses), 0)
        self.assertEqual(len(self.motion_port.trajectories), 0)
        self.assertEqual(len(self.logger.logs), 1)
        self.assertIn('No waypoints loaded', self.logger.logs[0][0])
        self.assertEqual(self.logger.logs[0][1], 'warn')

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
