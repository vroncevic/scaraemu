# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Outbound provides container exposing scaralang subsystem adapters.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.provides import ProtocolProvides
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ScaralangProvides:
    '''
        Encapsulates all adapters provided by the scaralang infrastructure subsystem.

        It defines:

            :attributes:
                | bypass - Dead zone bypass calculation adapter.
                | demo - Trajectory preset demo shape generator adapter.
                | linkage - Manipulator linkage forward kinematics adapter.
                | reach - Manipulator workspace reach and boundary adapter.
                | safety - Motion validator adapter.
                | script - Script file loader and parser adapter.
                | protocol - Bundled protocol adapters.
                | boundary - Manipulator workspace boundary service.
            :methods:
                | codec - Convenience property returning binary wire frame codec adapter.
                | payload_decoder - Convenience property returning binary command payload decoder.
                | response_builder - Convenience property returning binary response frame builder.
                | response_decoder - Convenience property returning binary response payload decoder.
    '''

    bypass: IDeadZoneBypassAdapter
    demo: ITrajectoryDemoAdapter
    linkage: ILinkageAdapter
    reach: IWorkspaceReachAdapter
    safety: IMotionValidatorAdapter
    script: IScriptLoaderAdapter
    protocol: ProtocolProvides
    boundary: IWorkspaceBoundaryService

    @property
    def codec(self) -> IBinaryFrameCodecAdapter:
        '''
            Returns wire frame codec adapter from protocol bundle.

            :return: IBinaryFrameCodecAdapter instance.
            :exceptions: None.
        '''
        return self.protocol.codec

    @property
    def payload_decoder(self) -> IBinaryPayloadDecoderAdapter:
        '''
            Returns payload decoder adapter from protocol bundle.

            :return: IBinaryPayloadDecoderAdapter instance.
            :exceptions: None.
        '''
        return self.protocol.payload_decoder

    @property
    def response_builder(self) -> IBinaryResponseBuilderAdapter:
        '''
            Returns response builder adapter from protocol bundle.

            :return: IBinaryResponseBuilderAdapter instance.
            :exceptions: None.
        '''
        return self.protocol.response_builder

    @property
    def response_decoder(self) -> IBinaryResponseDecoderAdapter:
        '''
            Returns response decoder adapter from protocol bundle.

            :return: IBinaryResponseDecoderAdapter instance.
            :exceptions: None.
        '''
        return self.protocol.response_decoder
