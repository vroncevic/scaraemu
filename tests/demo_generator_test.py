# -*- coding: UTF-8 -*-

'''
Module
    test_demo_generator.py
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
    Unit tests for TrajectoryDemoGenerator.
'''

from __future__ import annotations

import unittest
from scaraemu.core.service.demo_generator import TrajectoryDemoGenerator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryDemoGenerator(unittest.TestCase):
    '''Unit test cases for TrajectoryDemoGenerator.'''

    def test_generate_circle(self) -> None:
        '''Tests circular trajectory generation.'''
        poses = TrajectoryDemoGenerator.generate_circle(160.0, 0.0, 45.0, 20.0, 20)
        self.assertEqual(len(poses), 21)
        self.assertAlmostEqual(poses[0].x, 205.0)

    def test_generate_square(self) -> None:
        '''Tests square trajectory generation.'''
        poses = TrajectoryDemoGenerator.generate_square(160.0, 0.0, 60.0, 20.0)
        self.assertEqual(len(poses), 5)

    def test_generate_star(self) -> None:
        '''Tests 5-pointed star trajectory generation.'''
        poses = TrajectoryDemoGenerator.generate_star(160.0, 0.0, 45.0, 20.0, 20.0)
        self.assertEqual(len(poses), 11)

    def test_generate_helix(self) -> None:
        '''Tests 3D helical trajectory generation.'''
        poses = TrajectoryDemoGenerator.generate_helix(160.0, 0.0, 30.0, 10.0, 50.0, 2, 20)
        self.assertEqual(len(poses), 21)
        self.assertAlmostEqual(poses[0].z, 10.0)
        self.assertAlmostEqual(poses[-1].z, 50.0)

    def test_dynamic_generate(self) -> None:
        '''Tests dispatch via dynamic generate method.'''
        for demo in TrajectoryDemoGenerator.AVAILABLE_DEMOS:
            poses = TrajectoryDemoGenerator.generate(demo, 160.0, 0.0, 20.0)
            self.assertTrue(len(poses) > 0)

        empty = TrajectoryDemoGenerator.generate('unknown_pattern')
        self.assertEqual(len(empty), 0)


if __name__ == '__main__':
    unittest.main()
