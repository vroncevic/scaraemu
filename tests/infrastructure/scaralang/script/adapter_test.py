# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for ScriptLoaderAdapter.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase, main as unittest_main
from unittest.mock import Mock

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan

from scaraemu.infrastructure.scaralang.script.adapter import ScriptLoaderAdapter
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScriptLoaderAdapter(TestCase):
    '''
        Unit tests for ScriptLoaderAdapter.

        It defines:

            :methods:
                | setUp - Initializes mock compiler and adapter.
                | test_implements_iscript_loader_adapter_protocol - Verifies structural protocol conformance at runtime.
                | test_load_from_text_compiles_waypoints - Verifies load_from_text delegates to compiler and maps waypoints.
                | test_load_from_file_json_plan - Verifies load_from_file handles JSON plan format.
                | test_load_from_file_scara_script - Verifies load_from_file reads .scara script and compiles it.
                | test_load_from_nonexistent_file_returns_empty_list - Verifies load_from_file returns empty list when file does not exist.
                | test_get_version - Verifies get_version returns valid version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes mock compiler and adapter.

            :exceptions: None.
        '''
        self._mock_compiler: Mock = Mock(spec=IScriptPlanCompiler)
        self._adapter: ScriptLoaderAdapter = ScriptLoaderAdapter(
            compiler=self._mock_compiler,
        )

    def test_implements_iscript_loader_adapter_protocol(self) -> None:
        '''
            Verifies structural protocol conformance at runtime.

            :exceptions: None.
        '''
        self.assertIsInstance(self._adapter, IScriptLoaderAdapter)

    def test_load_from_text_compiles_waypoints(self) -> None:
        '''
            Verifies load_from_text delegates to compiler and maps waypoints.

            :exceptions: None.
        '''
        mock_plan = Mock(spec=ITrajectoryPlan)
        mock_plan.waypoints = [
            Waypoint(
                x=10.0,
                y=20.0,
                z=5.0,
                phi=30.0,
                speed=50.0,
                name='',
                command='',
            ),
            Waypoint(
                x=40.0,
                y=50.0,
                z=-10.0,
                phi=60.0,
                speed=50.0,
                name='',
                command='',
            ),
        ]
        self._mock_compiler.compile_script.return_value = mock_plan

        poses = self._adapter.load_from_text('MOVE TO X 10 Y 20')

        self.assertEqual(len(poses), 2)
        self.assertEqual(poses[0].x, 10.0)
        self.assertEqual(poses[0].y, 20.0)
        self.assertEqual(poses[0].z, 5.0)
        self.assertEqual(poses[0].phi, 30.0)
        self.assertEqual(poses[1].x, 40.0)
        self.assertEqual(poses[1].y, 50.0)
        self.assertEqual(poses[1].z, -10.0)
        self.assertEqual(poses[1].phi, 60.0)

    def test_load_from_file_json_plan(self) -> None:
        '''
            Verifies load_from_file handles JSON plan format.

            :exceptions: None.
        '''
        json_content = '{"waypoints": [{"x": 100.0, "y": 50.0, "z": 0.0, "phi": 0.0}]}'
        with NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
            tmp.write(json_content)
            tmp_path = tmp.name

        try:
            poses = self._adapter.load_from_file(tmp_path)
            self.assertEqual(len(poses), 1)
            self.assertEqual(poses[0].x, 100.0)
            self.assertEqual(poses[0].y, 50.0)
        finally:
            Path(tmp_path).unlink()

    def test_load_from_file_scara_script(self) -> None:
        '''
            Verifies load_from_file reads .scara script and compiles it.

            :exceptions: None.
        '''
        mock_plan = Mock(spec=ITrajectoryPlan)
        mock_plan.waypoints = [
            Waypoint(
                x=15.0,
                y=25.0,
                z=0.0,
                phi=0.0,
                speed=50.0,
                name='',
                command='',
            ),
        ]
        self._mock_compiler.compile_script.return_value = mock_plan

        with NamedTemporaryFile('w', suffix='.scara', delete=False) as tmp:
            tmp.write('MOVE TO X 15 Y 25')
            tmp_path = tmp.name

        try:
            poses = self._adapter.load_from_file(tmp_path)
            self.assertEqual(len(poses), 1)
            self.assertEqual(poses[0].x, 15.0)
            self.assertEqual(poses[0].y, 25.0)
        finally:
            Path(tmp_path).unlink()

    def test_load_from_nonexistent_file_returns_empty_list(self) -> None:
        '''
            Verifies load_from_file returns empty list when file does not exist.

            :exceptions: None.
        '''
        poses = self._adapter.load_from_file('/nonexistent/path/script.scara')
        self.assertEqual(poses, [])

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self._adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
