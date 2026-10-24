# -*- coding: UTF-8 -*-

'''
Module
    isynchronizer_test.py
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
    Unit tests for IBridgeSynchronizer protocol interface.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.bridge.sync.isynchronizer import IBridgeSynchronizer

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingBridgeSynchronizer:
    '''
        Stub satisfying IBridgeSynchronizer protocol structurally.
    '''

    def on_state_change(self, connected: bool) -> None:
        '''Handles connection state changes.'''

    def on_telemetry(self, pose: ScaraPose) -> None:
        '''Handles telemetry snapshots.'''

    def get_version(self) -> str:
        '''Returns component version.'''
        return '1.0.2'


class _NonConformingBridgeSynchronizer:
    '''
        Stub missing methods for IBridgeSynchronizer protocol.
    '''

    def dummy(self) -> None:
        '''Dummy method for public methods count.'''

    def get_version(self) -> str:
        '''Returns component version.'''
        return '1.0.2'


class TestIBridgeSynchronizer(TestCase):
    '''
        Unit tests verifying IBridgeSynchronizer runtime checkability.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Tests that structurally compliant stub satisfies protocol.
        '''
        sync = _ConformingBridgeSynchronizer()
        self.assertIsInstance(sync, IBridgeSynchronizer)

    def test_protocol_non_conformance(self) -> None:
        '''
            Tests that incomplete stub fails protocol check.
        '''
        sync = _NonConformingBridgeSynchronizer()
        self.assertNotIsInstance(sync, IBridgeSynchronizer)


if __name__ == '__main__':
    unittest_main()
