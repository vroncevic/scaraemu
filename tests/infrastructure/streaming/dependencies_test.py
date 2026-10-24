# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit test cases for StreamingDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.transport.itransport import ITransport

from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.streaming.dependencies import StreamingDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamingDependenciesTestCase(TestCase):
    '''
        Test cases verifying StreamingDependencies parameter container.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores and exposes attributes.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle correctly stores and exposes attributes.
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

        self.assertIs(deps.transport, mock_transport)
        self.assertIs(deps.log_listener, mock_log)
        self.assertIs(deps.kinematics, mock_kinematics)
        self.assertIs(deps.codec, mock_codec)


if __name__ == '__main__':
    unittest_main()
