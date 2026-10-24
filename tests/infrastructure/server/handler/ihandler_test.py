# -*- coding: UTF-8 -*-

'''
Module
    ihandler_test.py
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
    Unit tests for IBinaryCommandHandler protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId

from scaraemu.infrastructure.server.handler.ihandler import IBinaryCommandHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ValidBinaryCommandHandler:
    '''
        Dummy class conforming to IBinaryCommandHandler structurally.
    '''

    def can_handle(self, msg_id: MessageId) -> bool:
        '''
            Tests can handle.

            :param msg_id: Input msg_id.
            :return: True if handled.
            :exceptions: None.
        '''
        return msg_id == MessageId.CMD_PING

    def handle(self, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Tests handle.

            :param frame: Input frame.
            :return: List of response frames.
            :exceptions: None.
        '''
        if frame.seq_num >= 0:
            return []
        return []

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidBinaryCommandHandler:
    '''
        Dummy class missing required protocol methods.
    '''

    def dummy_method_a(self) -> None:
        '''Dummy method A.'''

    def dummy_method_b(self) -> None:
        '''Dummy method B.'''


class TestIBinaryCommandHandler(TestCase):
    '''
        Test cases verifying IBinaryCommandHandler structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming class satisfies protocol.
                | test_non_conforming_instance - Verifies non-conforming class fails protocol.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming class satisfies IBinaryCommandHandler structurally.

            :exceptions: None.
        '''
        handler = _ValidBinaryCommandHandler()
        self.assertIsInstance(handler, IBinaryCommandHandler)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy IBinaryCommandHandler.

            :exceptions: None.
        '''
        invalid = _InvalidBinaryCommandHandler()
        self.assertNotIsInstance(invalid, IBinaryCommandHandler)


if __name__ == '__main__':
    unittest_main()
