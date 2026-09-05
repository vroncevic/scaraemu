# -*- coding: UTF-8 -*-

'''
Module
    test_simulation_state_dto.py
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
    Unit tests for SimulationStateDTO model.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.model.simulation_state_dto import SimulationStateDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSimulationStateDTO(unittest.TestCase):
    '''Unit test cases for SimulationStateDTO model.'''

    def test_simulation_state_dto(self) -> None:
        '''Tests animation and queue state fields.'''
        tgt = ScaraPose(x=120.0, y=30.0, z=5.0)
        dto = SimulationStateDTO(
            is_animating=True,
            queue_depth=12,
            trail_points=((100.0, 0.0), (110.0, 15.0)),
            current_target=tgt
        )
        self.assertTrue(dto.is_animating)
        self.assertEqual(dto.queue_depth, 12)
        self.assertEqual(len(dto.trail_points), 2)
        self.assertEqual(dto.current_target, tgt)


if __name__ == '__main__':
    unittest.main()
