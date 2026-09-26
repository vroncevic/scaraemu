# -*- coding: UTF-8 -*-

'''
Module
    ivirtual_binary_frame_processor.py
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
    Interface definition for processing binary wire protocol frames in virtual robot server.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IVirtualBinaryFrameProcessor(Protocol):
    '''
        Protocol defining virtual robot binary frame processor contract.

        It defines:

            :methods:
                | process_frame - Processes an inbound binary frame and produces response frames.
                | reset - Clears any internal state caches or planned target poses.
    '''

    def process_frame(self, *, frame: BinaryFrame) -> list[BinaryFrame]:
        '''
            Processes an inbound binary frame and produces response frames.

            :param frame: Decoded BinaryFrame from host client.
            :return: List of response BinaryFrame instances to transmit back.
            :exceptions: None.
        '''
        ...

    def reset(self) -> None:
        '''
            Clears any internal state caches or planned target poses.

            :exceptions: None.
        '''
        ...
