# -*- coding: UTF-8 -*-

'''
Module
    iloader_test.py
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
    Unit test for ITransmissionLoader interface protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.infrastructure.settings.transmission.iloader import ITransmissionLoader
from scaraemu.infrastructure.settings.transmission.loader import TransmissionLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITransmissionLoader(TestCase):
    '''
        Unit tests verifying ITransmissionLoader protocol structural conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies TransmissionLoader satisfies ITransmissionLoader.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies TransmissionLoader satisfies ITransmissionLoader protocol.

            :exceptions: None.
        '''
        context = ContextBundleFactory.create_bundle()
        loader = TransmissionLoader(context)
        self.assertIsInstance(loader, ITransmissionLoader)


if __name__ == '__main__':
    unittest_main()
