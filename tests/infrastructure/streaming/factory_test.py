# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit test cases for StreamingFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.transport.itransport import ITransport

from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.streaming.dependencies import StreamingDependencies
from scaraemu.infrastructure.streaming.factory import StreamingFactory
from scaraemu.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamingFactoryTestCase(TestCase):
    '''
        Test cases verifying StreamingFactory subsystem wiring and version.

        It defines:

            :methods:
                | test_create - Verifies factory creates and wires streaming subsystem provides.
                | test_get_version - Verifies factory version retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates and wires streaming subsystem provides.
        '''
        mock_transport = MagicMock(spec=ITransport)
        mock_log = MagicMock(spec=ILogListener)
        mock_kinematics = MagicMock(spec=IManipulatorKinematics)
        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)

        deps = StreamingDependencies(
            transport=mock_transport,
            log_listener=mock_log,
            kinematics=mock_kinematics,
            codec=mock_codec,
        )

        provides = StreamingFactory.create(dependencies=deps)

        self.assertIsInstance(provides, StreamingProvides)
        self.assertIsNotNone(provides.streamer)
        self.assertIsNotNone(provides.motion_coordinator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version retrieval.
        '''
        version = StreamingFactory.get_version()
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
