# -*- coding: UTF-8 -*-

'''
Module
    test_kinematics_config_dto.py
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
    Unit tests for KinematicsConfigDTO model.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.kinematics_config_dto import KinematicsConfigDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsConfigDTO(unittest.TestCase):
    '''Unit test cases for KinematicsConfigDTO model.'''

    def test_default_config(self) -> None:
        '''Tests transmission defaults.'''
        cfg = KinematicsConfigDTO()
        self.assertEqual(cfg.steps_per_rev, 200.0)
        self.assertEqual(cfg.microstepping, 16.0)
        self.assertEqual(cfg.gear_ratio_j1, 4.0)
        self.assertEqual(cfg.gear_ratio_j2, 4.0)
        self.assertEqual(cfg.gear_ratio_j4, 1.0)
        self.assertEqual(cfg.leadscrew_pitch_z, 8.0)


if __name__ == '__main__':
    unittest.main()
