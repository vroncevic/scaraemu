# -*- coding: UTF-8 -*-

'''
Module
    inotifier_test.py
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
    Unit test for IMotionNotifier protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyNotifier:
    '''
        Dummy class implementing IMotionNotifier structurally.

        It defines:

            :attributes:
                | registered_listener - Held completion listener instance.
            :methods:
                | __init__ - Initializes dummy notifier.
                | set_completion_listener - Associates completion listener.
                | get_version - Returns version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes dummy notifier.

            :exceptions: None.
        '''
        self.registered_listener: IMotionCompletionListener | None = None

    def set_completion_listener(self, listener: IMotionCompletionListener) -> None:
        '''
            Associates completion listener.

            :param listener: Completion listener collaborator.
            :exceptions: None.
        '''
        self.registered_listener = listener

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


class DummyListenerForNotifier:
    '''
        Dummy listener collaborator for notifier testing.

        It defines:

            :methods:
                | on_waypoint_completed - Records completed sequence.
                | get_version - Returns version string.
    '''

    def on_waypoint_completed(self, seq_num: int) -> None:
        '''
            Records completed sequence.

            :param seq_num: Waypoint sequence.
            :exceptions: None.
        '''
        _ = seq_num

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


class TestIMotionNotifier(TestCase):
    '''
        Unit tests for IMotionNotifier protocol compliance.

        It defines:

            :methods:
                | test_protocol_compliance - Verifies structural protocol compliance.
                | test_set_listener - Verifies association of completion listener.
    '''

    def test_protocol_compliance(self) -> None:
        '''
            Verifies structural protocol compliance.

            :exceptions: None.
        '''
        notifier = DummyNotifier()
        self.assertIsInstance(notifier, IMotionNotifier)
        self.assertEqual(notifier.get_version(), __version__)

    def test_set_listener(self) -> None:
        '''
            Verifies association of completion listener.

            :exceptions: None.
        '''
        notifier = DummyNotifier()
        listener = DummyListenerForNotifier()
        notifier.set_completion_listener(listener)
        self.assertIs(notifier.registered_listener, listener)


if __name__ == '__main__':
    unittest_main()
