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
    Factory instantiating BinaryFrameCodecAdapter instances.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

from scaraemu.infrastructure.scaralang.protocol.codec.adapter import BinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameCodecAdapterFactory:
    '''
        Factory providing BinaryFrameCodecAdapter instances.

        It defines:

            :methods:
                | create - Builds an adapter wired with standard scaralang codecs.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IBinaryFrameCodecAdapter:
        '''
            Builds and returns a BinaryFrameCodecAdapter instance wired with
            standard scaralang parser and builder components.

            :return: Configured IBinaryFrameCodecAdapter instance.
            :exceptions: None.
        '''
        parser: IBinaryFrameParser = ParserFactory.create().parser
        builder: IBinaryFramePacker = BuilderFactory.create().packer

        return BinaryFrameCodecAdapter(
            parser=parser,
            builder=builder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
