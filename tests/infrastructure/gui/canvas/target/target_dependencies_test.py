# -*- coding: UTF-8 -*-

'''
Module
    target_dependencies_test.py
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
    Unit test cases for TargetDependencies parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.target.ielbow_auto_switch_coordinator import IElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.itarget_motion_dispatcher import ITargetMotionDispatcher
from scaraemu.infrastructure.gui.canvas.target.target_dependencies import TargetDependencies
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TargetDependenciesTestCase(TestCase):
    '''
        Unit tests for TargetDependencies.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        mock_emulation = MagicMock(spec=IEmulationService)
        mock_validator = MagicMock(spec=IMotionValidatorAdapter)
        mock_elbow = MagicMock(spec=IElbowAutoSwitchCoordinator)
        mock_bypass = MagicMock(spec=IDeadZoneBypassAdapter)
        mock_dispatcher = MagicMock(spec=ITargetMotionDispatcher)
        mock_logger = MagicMock(spec=ILogListener)

        bundle = TargetDependencies(
            emulation_service=mock_emulation,
            validator=mock_validator,
            elbow_coordinator=mock_elbow,
            bypass_adapter=mock_bypass,
            motion_dispatcher=mock_dispatcher,
            log_listener=mock_logger,
        )

        self.assertIs(bundle.emulation_service, mock_emulation)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.elbow_coordinator, mock_elbow)
        self.assertIs(bundle.bypass_adapter, mock_bypass)
        self.assertIs(bundle.motion_dispatcher, mock_dispatcher)
        self.assertIs(bundle.log_listener, mock_logger)


if __name__ == '__main__':
    unittest_main()
