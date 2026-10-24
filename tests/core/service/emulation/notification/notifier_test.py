# -*- coding: UTF-8 -*-

'''
Module
    notifier_test.py
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
    Unit test cases for MotionNotifier.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.notification.notifier import MotionNotifier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionNotifierTestCase(TestCase):
    '''
        Test case verifying MotionNotifier dispatching and version query.

        It defines:

            :methods:
                | setUp - Prepares test environment with notifier instance.
                | test_structural_compliance - Verifies satisfaction of IMotionNotifier.
                | test_notification_dispatch - Verifies dispatch of completion callbacks.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        self.notifier = MotionNotifier()

    def test_structural_compliance(self) -> None:
        '''
            Verifies satisfaction of IMotionNotifier protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.notifier, IMotionNotifier)

    def test_notification_dispatch(self) -> None:
        '''
            Verifies dispatch of completion callbacks to registered listeners.

            :exceptions: None.
        '''
        listener = MagicMock(spec=IMotionCompletionListener)
        self.notifier.set_completion_listener(listener)
        self.notifier.notify_waypoint_completed(42)
        listener.on_waypoint_completed.assert_called_once_with(42)

    def test_get_version(self) -> None:
        '''
            Verifies version string.

            :exceptions: None.
        '''
        self.assertEqual(self.notifier.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
