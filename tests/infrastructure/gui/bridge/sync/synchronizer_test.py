# -*- coding: UTF-8 -*-

'''
Module
    synchronizer_test.py
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
    Unit tests for BridgeSynchronizer and IBridgeSynchronizer protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer
from scaraemu.infrastructure.gui.bridge.sync.synchronizer import BridgeSynchronizer

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockStatusView:
    '''
        Mock status view for testing bridge synchronizer.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock state.

            :exceptions: None.
        '''
        self.connected: bool = False

    def set_connected_state(self, connected: bool) -> None:
        '''
            Sets connected state.

            :param connected: Connection active flag.
            :exceptions: None.
        '''
        self.connected = connected

    def get_version(self) -> str:
        '''
            Returns mock version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return '1.0.2'


class BridgeSynchronizerTestCase(TestCase):
    '''
        Unit tests for BridgeSynchronizer operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies BridgeSynchronizer satisfies IBridgeSynchronizer.
                | test_on_state_change - Verifies hardware state changes propagate to view.
                | test_on_telemetry - Verifies telemetry poses are recorded.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies BridgeSynchronizer satisfies IBridgeSynchronizer.

            :exceptions: None.
        '''
        status_view = _MockStatusView()

        sync = BridgeSynchronizer(
            status_view=status_view,
        )

        self.assertIsInstance(sync, IBridgeSynchronizer)
        self.assertEqual(sync.get_version(), '1.0.2')

    def test_on_state_change(self) -> None:
        '''
            Verifies hardware state changes propagate to view.

            :exceptions: None.
        '''
        status_view = _MockStatusView()

        sync = BridgeSynchronizer(
            status_view=status_view,
        )

        sync.on_state_change(True)
        connected, _ = sync.get_state()
        self.assertTrue(connected)
        self.assertTrue(status_view.connected)

    def test_on_telemetry(self) -> None:
        '''
            Verifies telemetry poses are recorded.

            :exceptions: None.
        '''
        status_view = _MockStatusView()

        sync = BridgeSynchronizer(
            status_view=status_view,
        )

        pose = ScaraPose(x=10.0, y=20.0, z=30.0, phi=0.0)
        sync.on_telemetry(pose)
        _, recorded_pose = sync.get_state()
        self.assertEqual(recorded_pose, pose)


if __name__ == '__main__':
    unittest_main()
