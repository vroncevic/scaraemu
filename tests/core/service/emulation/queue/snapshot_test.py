# -*- coding: UTF-8 -*-

'''
Module
    snapshot_test.py
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
    Unit test cases for EmulationQueueSnapshot.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.queue.snapshot import EmulationQueueSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationQueueSnapshotTestCase(TestCase):
    '''
        Unit test cases verifying EmulationQueueSnapshot properties.

        It defines:

            :methods:
                | test_snapshot_creation - Tests creating snapshot dataclass.
    '''

    def test_snapshot_creation(self) -> None:
        '''
            Tests creating snapshot dataclass and verifies fields.

            :exceptions: None.
        '''
        target = ScaraPose(x=100.0, y=50.0, z=10.0, phi=0.0)
        path = ((100.0, 50.0), (120.0, 60.0))
        snapshot = EmulationQueueSnapshot(
            queue_depth=3,
            has_target=True,
            current_target=target,
            planned_path=path,
        )
        self.assertEqual(snapshot.queue_depth, 3)
        self.assertTrue(snapshot.has_target)
        self.assertEqual(snapshot.current_target, target)
        self.assertEqual(snapshot.planned_path, path)


if __name__ == '__main__':
    unittest_main()
