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
    Unit tests for BinaryPayloadDecoderAdapter.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.joint_steps import JointSteps

from scaraemu.infrastructure.scaralang.protocol.payload.adapter import BinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryPayloadDecoderAdapter(TestCase):
    '''
        Validates BinaryPayloadDecoderAdapter methods.

        It defines:

            :methods:
                | setUp - Initializes adapter instance for testing.
                | test_unpack_tool_cmd - Verifies tool command unpacking.
                | test_unpack_jog_joint - Verifies jog command unpacking.
                | test_unpack_joint_steps - Verifies joint steps unpacking.
                | test_get_version - Verifies component version string.
    '''

    adapter: BinaryPayloadDecoderAdapter

    def setUp(self) -> None:
        '''
            Initializes adapter instance for testing.

            :exceptions: None.
        '''
        raw_adapter = BinaryPayloadDecoderAdapterFactory.create()
        self.assertIsInstance(raw_adapter, BinaryPayloadDecoderAdapter)
        self.adapter = raw_adapter

    def test_unpack_tool_cmd(self) -> None:
        '''
            Verifies tool command unpacking.

            :exceptions: None.
        '''
        self.assertIsInstance(self.adapter, IBinaryPayloadDecoderAdapter)

        tool_id, state = self.adapter.unpack_tool_cmd(b'\x01\x01')
        self.assertEqual(tool_id, 1)
        self.assertTrue(state)

    def test_unpack_jog_joint(self) -> None:
        '''
            Verifies jog command unpacking.

            :exceptions: None.
        '''
        payload = pack('<Bi', 2, -500)

        joint_id, step = self.adapter.unpack_jog_joint(payload)
        self.assertEqual(joint_id, 2)
        self.assertEqual(step, -500)

    def test_unpack_joint_steps(self) -> None:
        '''
            Verifies joint steps unpacking.

            :exceptions: None.
        '''
        payload = pack('<iiiiIH', 10, 20, 30, 40, 1000, 100)

        steps: JointSteps = self.adapter.unpack_joint_steps(payload)
        self.assertIsInstance(steps, JointSteps)
        self.assertEqual(steps.target_j1_steps, 10)
        self.assertEqual(steps.target_j2_steps, 20)
        self.assertEqual(steps.target_z_steps, 30)
        self.assertEqual(steps.target_j4_steps, 40)

    def test_get_version(self) -> None:
        '''
            Verifies component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.adapter.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
