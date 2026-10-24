# -*- coding: UTF-8 -*-

'''
Module
    iprocessor_test.py
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
    Unit tests for IVirtualBinaryFrameProcessor protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame

from scaraemu.infrastructure.server.processor.iprocessor import IVirtualBinaryFrameProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyFrameProcessor:
    '''
        Dummy class satisfying IVirtualBinaryFrameProcessor structurally.
    '''

    def process_frame(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Processes dummy frame.

            :param frame: Inbound frame.
            :return: Empty list.
            :exceptions: None.
        '''
        return []

    def reset(self) -> None:
        '''
            Resets dummy state.

            :exceptions: None.
        '''
        pass

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version.
            :exceptions: None.
        '''
        return '1.0.2'


class TestIVirtualBinaryFrameProcessor(TestCase):
    '''
        Test cases verifying IVirtualBinaryFrameProcessor protocol checkability.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy processor satisfies protocol.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy processor satisfies IVirtualBinaryFrameProcessor protocol.

            :exceptions: None.
        '''
        processor = _DummyFrameProcessor()
        self.assertIsInstance(processor, IVirtualBinaryFrameProcessor)


if __name__ == '__main__':
    unittest_main()
