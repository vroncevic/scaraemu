# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for IJogActionDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyJogActionDelegate:
    '''
        Dummy delegate for protocol conformance verification.
    '''

    def __init__(self) -> None:
        '''
            Initializes call recorders.

            :exceptions: None.
        '''
        self.jog_calls: list[tuple[float, float, float, float]] = []
        self.home_calls: list[str] = []

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Records jog displacement parameters.

            :param dx: Delta X in mm.
            :param dy: Delta Y in mm.
            :param dz: Delta Z in mm.
            :param dphi: Delta Phi in radians.
            :exceptions: None.
        '''
        self.jog_calls.append((dx, dy, dz, dphi))

    def handle_home(self, axis: str) -> None:
        '''
            Records homing axis.

            :param axis: Target axis string.
            :exceptions: None.
        '''
        self.home_calls.append(axis)

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestJogActionDelegate(TestCase):
    '''
        Test cases verifying IJogActionDelegate protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy delegate satisfies IJogActionDelegate protocol.
                | test_jog_and_home_handling - Verifies jog and homing dispatch and version inquiry.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy delegate satisfies IJogActionDelegate protocol.

            :exceptions: None.
        '''
        delegate = _DummyJogActionDelegate()
        self.assertIsInstance(delegate, IJogActionDelegate)

    def test_jog_and_home_handling(self) -> None:
        '''
            Verifies jog and homing dispatch and version inquiry.

            :exceptions: None.
        '''
        delegate = _DummyJogActionDelegate()
        delegate.handle_jog(1.0, -2.0, 3.0, 0.5)
        self.assertEqual(delegate.jog_calls, [(1.0, -2.0, 3.0, 0.5)])

        delegate.handle_home('xy')
        self.assertEqual(delegate.home_calls, ['xy'])
        self.assertEqual(delegate.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
