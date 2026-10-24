# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for BinaryResponseDecoderAdapter.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main as unittest_main

from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.scaralang.protocol.response.adapter import BinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.factory import BinaryResponseDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryResponseDecoderAdapter(TestCase):
    '''
        Validates BinaryResponseDecoderAdapter execution and decoding.

        It defines:

            :methods:
                | test_satisfies_protocol - Verifies structural protocol conformity.
                | test_unpack_ack - Verifies decoding ACK payload.
                | test_unpack_nack - Verifies decoding NACK payload.
                | test_unpack_status_steps - Verifies decoding STATUS payload into ScaraStepCoords.
                | test_unpack_status_steps_short_payload - Verifies short payload handling.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies structural protocol conformity.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        self.assertIsInstance(adapter, IBinaryResponseDecoderAdapter)

    def test_unpack_ack(self) -> None:
        '''
            Verifies decoding ACK payload.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        payload = pack(BinaryStructFormat.ACK, 1, 14)
        cmd_id, free_slots = adapter.unpack_ack(payload)
        self.assertEqual(cmd_id, 1)
        self.assertEqual(free_slots, 14)

    def test_unpack_nack(self) -> None:
        '''
            Verifies decoding NACK payload.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        payload = pack(BinaryStructFormat.NACK, 1, 3)
        cmd_id, error_code = adapter.unpack_nack(payload)
        self.assertEqual(cmd_id, 1)
        self.assertEqual(error_code, 3)

    def test_unpack_status_steps(self) -> None:
        '''
            Verifies decoding STATUS payload into ScaraStepCoords.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        payload = pack(
            BinaryStructFormat.STATUS,
            1,
            0,
            0,
            100,
            200,
            300,
            400,
        )
        steps: ScaraStepCoords = adapter.unpack_status_steps(payload)
        self.assertEqual(steps.j1_steps, 100)
        self.assertEqual(steps.j2_steps, 200)
        self.assertEqual(steps.z_steps, 300)
        self.assertEqual(steps.j4_steps, 400)

    def test_unpack_status_steps_short_payload(self) -> None:
        '''
            Verifies short payload handling.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        steps: ScaraStepCoords = adapter.unpack_status_steps(b'')
        self.assertEqual(steps.j1_steps, 0)
        self.assertEqual(steps.j2_steps, 0)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        adapter: IBinaryResponseDecoderAdapter = BinaryResponseDecoderAdapterFactory.create()
        self.assertEqual(adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
