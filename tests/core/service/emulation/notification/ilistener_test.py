# -*- coding: UTF-8 -*-

'''
Module
    ilistener_test.py
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
    Unit test for IMotionCompletionListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyCompletionListener:
    '''
        Dummy class implementing IMotionCompletionListener structurally.

        It defines:

            :attributes:
                | completed_sequences - List of completed sequence numbers.
            :methods:
                | __init__ - Initializes dummy completion listener.
                | on_waypoint_completed - Records completed sequence number.
                | get_version - Returns version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes dummy completion listener.

            :exceptions: None.
        '''
        self.completed_sequences: list[int] = []

    def on_waypoint_completed(self, seq_num: int) -> None:
        '''
            Records completed sequence number.

            :param seq_num: Waypoint sequence number.
            :exceptions: None.
        '''
        self.completed_sequences.append(seq_num)

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


class TestIMotionCompletionListener(TestCase):
    '''
        Unit tests for IMotionCompletionListener protocol compliance.

        It defines:

            :methods:
                | test_protocol_compliance - Verifies structural protocol compliance.
                | test_callback_execution - Verifies callback recording.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Verifies structural protocol compliance.

            :exceptions: None.
        '''
        listener = DummyCompletionListener()
        self.assertIsInstance(listener, IMotionCompletionListener)
        self.assertEqual(listener.get_version(), __version__)

    def test_callback_execution(self) -> None:
        '''
            Verifies callback recording.

            :exceptions: None.
        '''
        listener = DummyCompletionListener()
        listener.on_waypoint_completed(42)
        self.assertEqual(listener.completed_sequences, [42])


if __name__ == '__main__':
    unittest_main()
