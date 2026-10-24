# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring all scaralang protocol adapters.
'''

from __future__ import annotations

from scaraemu.infrastructure.scaralang.protocol.builder.factory import BinaryResponseBuilderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.codec.factory import BinaryFrameCodecAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.payload.factory import BinaryPayloadDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.response.factory import BinaryResponseDecoderAdapterFactory
from scaraemu.infrastructure.scaralang.protocol.provides import ProtocolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolFactory:
    '''
        Factory assembling the protocol subsystem provided adapters.

        It defines:

            :methods:
                | create - Instantiates and bundles all binary protocol adapters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ProtocolProvides:
        '''
            Builds and bundles all binary protocol adapters.

            :return: Immutable ProtocolProvides container.
            :exceptions: None.
        '''
        return ProtocolProvides(
            codec=BinaryFrameCodecAdapterFactory.create(),
            payload_decoder=BinaryPayloadDecoderAdapterFactory.create(),
            response_builder=BinaryResponseBuilderAdapterFactory.create(),
            response_decoder=BinaryResponseDecoderAdapterFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
