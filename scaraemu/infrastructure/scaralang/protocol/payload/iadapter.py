# -*- coding: UTF-8 -*-

'''
Module
    iadapter.py
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
    Structural protocol for binary command payload decoding.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.joint_steps import JointSteps

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryPayloadDecoderAdapter(Protocol):
    '''
        Structural protocol defining binary command payload decoding contracts.

        It defines:

            :methods:
                | unpack_tool_cmd - Decodes a 2-byte tool command into (tool_id, state).
                | unpack_jog_joint - Decodes a 5-byte joint jog command into (joint_id, step).
                | unpack_joint_steps - Decodes a 22-byte joint step motion payload into JointSteps.
                | get_version - Returns protocol component version string.
    '''

    def unpack_tool_cmd(self, payload: bytes) -> tuple[int, bool]:
        '''
            Deserializes a tool actuation payload into tool ID and boolean state.

            :param payload: Raw body bytes of CMD_TOOL_PUMP or CMD_TOOL_VALVE frame.
            :return: Tuple containing (tool_id, state).
        '''

    def unpack_jog_joint(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes a joint jog command payload into joint index and step delta.

            :param payload: Raw body bytes of CMD_JOG_JOINT frame.
            :return: Tuple containing (joint_id, step).
        '''

    def unpack_joint_steps(self, payload: bytes) -> JointSteps:
        '''
            Deserializes a joint step motion command payload into JointSteps model.

            :param payload: Raw body bytes of CMD_MOVE_JOINT_STEPS frame.
            :return: JointSteps target model instance.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol component version string.

            :return: Semantic version string.
        '''
