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
    Unit tests for ProtocolFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.scaralang.protocol.factory import ProtocolFactory
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.provides import ProtocolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocolFactory(TestCase):
    '''
        Validates ProtocolFactory assembly and versioning.

        It defines:

            :methods:
                | test_create - Verifies creation of ProtocolProvides with all adapters.
                | test_get_version - Verifies factory version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates ProtocolProvides with all protocol adapters wired.

            :exceptions: None.
        '''
        provides = ProtocolFactory.create()
        self.assertIsInstance(provides, ProtocolProvides)
        self.assertIsInstance(provides.codec, IBinaryFrameCodecAdapter)
        self.assertIsInstance(provides.payload_decoder, IBinaryPayloadDecoderAdapter)
        self.assertIsInstance(provides.response_builder, IBinaryResponseBuilderAdapter)
        self.assertIsInstance(provides.response_decoder, IBinaryResponseDecoderAdapter)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(ProtocolFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
