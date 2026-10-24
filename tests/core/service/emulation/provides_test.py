# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit test cases for EmulationProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.provides import EmulationProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationProvidesTestCase(TestCase):
    '''
        Test case verifying EmulationProvides container behavior.

        It defines:

            :methods:
                | test_initialization - Verifies initialization of ports.
                | test_immutability - Verifies frozen container immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies initialization of ports.

            :exceptions: None.
        '''
        service = MagicMock(spec=IEmulationService)
        controller = MagicMock(spec=IEmulationController)
        queue = MagicMock(spec=IEmulationQueue)
        notifier = MagicMock(spec=IMotionNotifier)

        provides = EmulationProvides(
            service=service,
            controller=controller,
            queue=queue,
            notifier=notifier,
        )
        self.assertEqual(provides.service, service)
        self.assertEqual(provides.controller, controller)
        self.assertEqual(provides.queue, queue)
        self.assertEqual(provides.notifier, notifier)

    def test_immutability(self) -> None:
        '''
            Verifies frozen container immutability.

            :exceptions: None.
        '''
        service = MagicMock(spec=IEmulationService)
        controller = MagicMock(spec=IEmulationController)
        queue = MagicMock(spec=IEmulationQueue)
        notifier = MagicMock(spec=IMotionNotifier)

        provides = EmulationProvides(
            service=service,
            controller=controller,
            queue=queue,
            notifier=notifier,
        )
        with self.assertRaises(AttributeError):
            provides.service = service  # type: ignore[misc]


if __name__ == '__main__':
    unittest_main()
