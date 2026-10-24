# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Concrete adapter for decoding binary protocol command payloads.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.core.service.protocol.isystem_unpacker import IBinarySystemPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPayloadDecoderAdapter:
    '''
        Adapter decoding raw binary payload bytes into structured types and models.

        It defines:

            :attributes:
                | _actuator - Injected scaralang actuator payload unpacker.
                | _system - Injected scaralang system payload unpacker.
                | _motion - Injected scaralang motion payload unpacker.
            :methods:
                | __init__ - Initializes adapter with unpacker collaborators.
                | unpack_tool_cmd - Decodes tool command payload into (tool_id, state).
                | unpack_jog_joint - Decodes joint jog command payload into (joint_id, step).
                | unpack_joint_steps - Decodes joint step motion payload into JointSteps.
                | get_version - Returns adapter component version string.
    '''

    _actuator: IBinaryActuatorPayloadUnpacker
    _system: IBinarySystemPayloadUnpacker
    _motion: IBinaryMotionPayloadUnpacker

    def __init__(
        self,
        *,
        actuator: IBinaryActuatorPayloadUnpacker,
        system: IBinarySystemPayloadUnpacker,
        motion: IBinaryMotionPayloadUnpacker,
    ) -> None:
        '''
            Initializes adapter with unpacker collaborators.

            :param actuator: Injected IBinaryActuatorPayloadUnpacker instance.
            :param system: Injected IBinarySystemPayloadUnpacker instance.
            :param motion: Injected IBinaryMotionPayloadUnpacker instance.
            :exceptions: None.
        '''
        self._actuator: Final[IBinaryActuatorPayloadUnpacker] = actuator
        self._system: Final[IBinarySystemPayloadUnpacker] = system
        self._motion: Final[IBinaryMotionPayloadUnpacker] = motion

    def unpack_tool_cmd(self, payload: bytes) -> tuple[int, bool]:
        '''
            Deserializes a tool actuation payload into tool ID and boolean state.

            :param payload: Raw body bytes of CMD_TOOL_PUMP or CMD_TOOL_VALVE frame.
            :return: Tuple containing (tool_id, state).
            :exceptions: None.
        '''
        return self._actuator.unpack_tool_cmd(payload)

    def unpack_jog_joint(self, payload: bytes) -> tuple[int, int]:
        '''
            Deserializes a joint jog command payload into joint index and step delta.

            :param payload: Raw body bytes of CMD_JOG_JOINT frame.
            :return: Tuple containing (joint_id, step).
            :exceptions: None.
        '''
        joint_id, step, _ = self._system.unpack_jog_payload(payload)
        return joint_id, step

    def unpack_joint_steps(self, payload: bytes) -> JointSteps:
        '''
            Deserializes a joint step motion command payload into JointSteps model.

            :param payload: Raw body bytes of CMD_MOVE_JOINT_STEPS frame.
            :return: JointSteps target model instance.
            :exceptions: None.
        '''
        return self._motion.unpack_joint_steps(payload)

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
