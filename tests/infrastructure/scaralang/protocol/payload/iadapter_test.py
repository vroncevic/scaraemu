# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for IBinaryPayloadDecoderAdapter Protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.joint_steps import JointSteps

from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockPayloadDecoder:
    def unpack_tool_cmd(self, payload: bytes) -> tuple[int, bool]:
        return (0, True)

    def unpack_jog_joint(self, payload: bytes) -> tuple[int, int]:
        return (1, 100)

    def unpack_joint_steps(self, payload: bytes) -> JointSteps:
        return JointSteps(
            target_j1_steps=0,
            target_j2_steps=0,
            target_z_steps=0,
            target_j4_steps=0,
            duration_us=1000,
            feedrate_scale=100,
        )

    def get_version(self) -> str:
        return '1.0.2'


class TestIBinaryPayloadDecoderAdapter(TestCase):
    '''
        Validates IBinaryPayloadDecoderAdapter protocol conformance.

        It defines:

            :methods:
                | test_conforming_class_satisfies_protocol - Verifies structural typing.
                | test_non_conforming_class_fails_protocol - Verifies non-conforming fails.
    '''

    def test_conforming_class_satisfies_protocol(self) -> None:
        '''
            Verifies structural typing.

            :exceptions: None.
        '''
        decoder = _MockPayloadDecoder()
        self.assertIsInstance(decoder, IBinaryPayloadDecoderAdapter)

    def test_non_conforming_class_fails_protocol(self) -> None:
        '''
            Verifies non-conforming fails.

            :exceptions: None.
        '''
        class _Bad:
            pass

        self.assertNotIsInstance(_Bad(), IBinaryPayloadDecoderAdapter)


if __name__ == '__main__':
    unittest_main()
