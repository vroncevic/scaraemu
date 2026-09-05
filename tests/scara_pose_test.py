# -*- coding: UTF-8 -*-

'''
Module
    test_scara_pose.py
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
    Unit tests for ScaraPose domain model.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraPose(unittest.TestCase):
    '''Unit test cases for ScaraPose model.'''

    def test_pose_instantiation(self) -> None:
        '''Tests dataclass field assignments and immutability.'''
        pose = ScaraPose(x=100.0, y=50.0, z=20.0, phi=0.5)
        self.assertEqual(pose.x, 100.0)
        self.assertEqual(pose.y, 50.0)
        self.assertEqual(pose.z, 20.0)
        self.assertEqual(pose.phi, 0.5)


if __name__ == '__main__':
    unittest.main()
