# -*- coding: UTF-8 -*-

'''
Module
    scara_script_loader_test.py
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
    Unit tests for ScaraScriptLoader service.
'''

from __future__ import annotations

from json import dump
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.service.scara_script_loader import ScaraScriptLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraScriptLoader(TestCase):
    '''
        Test cases for ScaraScriptLoader parsing and loading.

        It defines:

            :methods:
                | setUp - Initializes loader instance.
                | test_parse_linear_and_joint_motion - Verifies MOVE_L and MOVE_J extraction.
                | test_parse_jump_and_elevation - Verifies JUMP, APPROACH and RETRACT.
                | test_parse_circular_arc - Verifies ARC_CW interpolation.
                | test_load_from_file_json - Verifies loading plan JSON file.
                | test_load_bundled_examples - Verifies loading bundled examples from filesystem.
    '''

    def setUp(self) -> None:
        '''
            Sets up loader instance.
        '''
        self.loader = ScaraScriptLoader()

    def test_parse_linear_and_joint_motion(self) -> None:
        '''
            Verifies MOVE_L and MOVE_J extraction.
        '''
        script = (
            'HOME\n'
            'MOVE_J X=150.0 Y=50.0 Z=20.0 PHI=15.0\n'
            'MOVE_L X=160.0 Y=80.0 Z=10.0\n'
        )
        poses = self.loader.parse_script(source=script)
        self.assertEqual(len(poses), 3)
        self.assertEqual(poses[0], ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0))
        self.assertEqual(poses[1], ScaraPose(x=150.0, y=50.0, z=20.0, phi=15.0))
        self.assertEqual(poses[2], ScaraPose(x=160.0, y=80.0, z=10.0, phi=15.0))

    def test_parse_jump_and_elevation(self) -> None:
        '''
            Verifies JUMP, APPROACH and RETRACT.
        '''
        script = (
            'HOME\n'
            'APPROACH DIST=10.0\n'
            'RETRACT DIST=15.0\n'
            'JUMP X=140.0 Y=-50.0 Z=10.0 ARCH=20.0\n'
        )
        poses = self.loader.parse_script(source=script)
        self.assertGreaterEqual(len(poses), 5)
        # Approach descent
        self.assertEqual(poses[1].z, 10.0)
        # Retract ascent
        self.assertEqual(poses[2].z, 25.0)

    def test_parse_circular_arc(self) -> None:
        '''
            Verifies ARC_CW interpolation.
        '''
        script = (
            'MOVE_L X=150.0 Y=0.0 Z=20.0\n'
            'ARC_CW X=150.0 Y=40.0 I=0.0 J=20.0\n'
        )
        poses = self.loader.parse_script(source=script)
        self.assertGreater(len(poses), 2)
        end_pt = poses[-1]
        self.assertAlmostEqual(end_pt.x, 150.0, delta=0.5)
        self.assertAlmostEqual(end_pt.y, 40.0, delta=0.5)

    def test_load_from_file_json(self) -> None:
        '''
            Verifies loading plan JSON file.
        '''
        plan_data = {
            'version': '1.0.2',
            'waypoints': [
                {'x': 140.0, 'y': 30.0, 'z': 15.0, 'phi': 0.0},
                {'x': 150.0, 'y': 40.0, 'z': 15.0, 'phi': 10.0},
            ],
        }
        tmp_path = None
        with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            dump(plan_data, f)
            tmp_path = Path(f.name)

        try:
            poses = self.loader.load_from_file(filepath=str(tmp_path))
            self.assertEqual(len(poses), 2)
            self.assertEqual(poses[0].x, 140.0)
            self.assertEqual(poses[1].y, 40.0)
        finally:
            if tmp_path is not None and tmp_path.exists():
                tmp_path.unlink()

    def test_load_bundled_examples(self) -> None:
        '''
            Verifies loading bundled examples from filesystem.
        '''
        sample = Path('/data/dev/python/3_tools/scarajectory/github/scarajectory/examples/12_industrial_pick_place.scara')
        if sample.is_file():
            poses = self.loader.load_from_file(filepath=str(sample))
            self.assertGreater(len(poses), 5)


if __name__ == '__main__':
    unittest_main()
