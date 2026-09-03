# -*- coding: UTF-8 -*-

'''
Module
    test_scara_step_coords.py
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
    Unit tests for ScaraStepCoords domain model.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_step_coords import ScaraStepCoords

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraStepCoords(unittest.TestCase):
    '''Unit test cases for ScaraStepCoords model.'''

    def test_step_coords_instantiation(self) -> None:
        '''Tests dataclass step values.'''
        steps = ScaraStepCoords(j1_steps=1600, j2_steps=-800, z_steps=400, j4_steps=200)
        self.assertEqual(steps.j1_steps, 1600)
        self.assertEqual(steps.j2_steps, -800)
        self.assertEqual(steps.z_steps, 400)
        self.assertEqual(steps.j4_steps, 200)


if __name__ == '__main__':
    unittest.main()
