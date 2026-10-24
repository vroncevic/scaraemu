# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for ScaralangProvides.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.provides import ProtocolProvides
from scaraemu.infrastructure.scaralang.provides import ScaralangProvides
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


class TestScaralangProvides(TestCase):
    '''
        Validates ScaralangProvides container attributes and convenience properties.

        It defines:

            :methods:
                | test_attributes_and_properties - Verifies access to all adapters and properties.
    '''

    def test_attributes_and_properties(self) -> None:
        '''
            Verifies ScaralangProvides holds injected adapters and delegates convenience properties.

            :exceptions: None.
        '''
        mock_bypass = MagicMock(spec=IDeadZoneBypassAdapter)
        mock_demo = MagicMock(spec=ITrajectoryDemoAdapter)
        mock_linkage = MagicMock(spec=ILinkageAdapter)
        mock_reach = MagicMock(spec=IWorkspaceReachAdapter)
        mock_safety = MagicMock(spec=IMotionValidatorAdapter)
        mock_script = MagicMock(spec=IScriptLoaderAdapter)
        mock_boundary = MagicMock(spec=IWorkspaceBoundaryService)

        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        mock_payload_decoder = MagicMock(spec=IBinaryPayloadDecoderAdapter)
        mock_response_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        mock_response_decoder = MagicMock(spec=IBinaryResponseDecoderAdapter)

        protocol = ProtocolProvides(
            codec=mock_codec,
            payload_decoder=mock_payload_decoder,
            response_builder=mock_response_builder,
            response_decoder=mock_response_decoder,
        )

        provides = ScaralangProvides(
            bypass=mock_bypass,
            demo=mock_demo,
            linkage=mock_linkage,
            reach=mock_reach,
            safety=mock_safety,
            script=mock_script,
            protocol=protocol,
            boundary=mock_boundary,
        )

        self.assertIs(provides.bypass, mock_bypass)
        self.assertIs(provides.demo, mock_demo)
        self.assertIs(provides.linkage, mock_linkage)
        self.assertIs(provides.reach, mock_reach)
        self.assertIs(provides.safety, mock_safety)
        self.assertIs(provides.script, mock_script)
        self.assertIs(provides.protocol, protocol)
        self.assertIs(provides.boundary, mock_boundary)

        self.assertIs(provides.codec, mock_codec)
        self.assertIs(provides.payload_decoder, mock_payload_decoder)
        self.assertIs(provides.response_builder, mock_response_builder)
        self.assertIs(provides.response_decoder, mock_response_decoder)


if __name__ == '__main__':
    unittest_main()
