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
    Unit test cases for PumperDependencies.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.flow.pacing.iwindow import IFlowWindow
from scaracom.transport.itransport import ITransport

from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.streaming.pumper.dependencies import PumperDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PumperDependenciesTestCase(TestCase):
    '''
        Test cases verifying PumperDependencies behavior.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores and exposes attributes.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle correctly stores and exposes attributes.
        '''
        transport = MagicMock(spec=ITransport)
        log_listener = MagicMock(spec=ILogListener)
        flow_window = MagicMock(spec=IFlowWindow)
        kinematics = MagicMock(spec=IManipulatorKinematics)
        codec = MagicMock(spec=IBinaryFrameCodecAdapter)

        bundle = PumperDependencies(
            transport=transport,
            log_listener=log_listener,
            flow_window=flow_window,
            kinematics=kinematics,
            codec=codec,
        )

        self.assertIs(bundle.transport, transport)
        self.assertIs(bundle.log_listener, log_listener)
        self.assertIs(bundle.flow_window, flow_window)
        self.assertIs(bundle.kinematics, kinematics)
        self.assertIs(bundle.codec, codec)


if __name__ == '__main__':
    unittest_main()
