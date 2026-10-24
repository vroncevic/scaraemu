# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for TransmissionLoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.infrastructure.settings.transmission.factory import TransmissionLoaderFactory
from scaraemu.infrastructure.settings.transmission.loader import TransmissionLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransmissionLoaderFactory(TestCase):
    '''
        Unit tests for TransmissionLoaderFactory.

        It defines:

            :methods:
                | test_create - Verifies create returns TransmissionLoader instance.
                | test_get_version - Verifies get_version returns valid version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns TransmissionLoader instance.

            :exceptions: None.
        '''
        context = ContextBundleFactory.create_bundle()
        loader = TransmissionLoaderFactory.create(context)
        self.assertIsInstance(loader, TransmissionLoader)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        version = TransmissionLoaderFactory.get_version()
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
