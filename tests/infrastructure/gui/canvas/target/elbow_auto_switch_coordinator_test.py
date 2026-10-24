# -*- coding: UTF-8 -*-

'''
Module
    elbow_auto_switch_coordinator_test.py
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
    Unit tests for ElbowAutoSwitchCoordinator component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.infrastructure.gui.canvas.target.elbow_auto_switch_coordinator import ElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.elbow_dependencies import ElbowDependencies
from scaraemu.infrastructure.gui.canvas.target.ielbow_auto_switch_coordinator import IElbowAutoSwitchCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationController:
    '''
        Mock emulation controller for testing elbow coordination.
    '''
    elbow_left: bool = False

    def set_elbow_mode(self, is_left: bool) -> None:
        '''
            Sets elbow mode.
        '''
        self.elbow_left = is_left

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Sets motors enabled.
        '''
        _ = enabled

    def set_estop(self, active: bool) -> None:
        '''
            Sets estop.
        '''
        _ = active

    def set_hold(self, active: bool) -> None:
        '''
            Sets hold.
        '''
        _ = active

    def set_hardware_connected(self, connected: bool) -> None:
        '''
            Sets hardware connected.
        '''
        _ = connected

    def reset(self) -> None:
        '''
            Resets controller.
        '''

    def get_flags(self) -> EmulationFlags:
        '''
            Returns current emulation safety and operational flags.
        '''
        return EmulationFlags(
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=self.elbow_left,
        )


class _MockKinematics:
    '''
        Mock kinematics solver for testing elbow coordination.
    '''
    reachable: bool = True

    def solve_ik(self, pose: ScaraPose, is_left: bool) -> ScaraJoints:
        '''
            Solves inverse kinematics.
        '''
        _ = is_left
        return ScaraJoints(
            theta1=0.1,
            theta2=0.2,
            z=pose.z,
            theta4=pose.phi,
            reachable=self.reachable,
        )

    def get_version(self) -> str:
        '''
            Returns mock version.
        '''
        return '1.0.2'


class _MockLogListener:
    '''
        Mock log listener for capturing logs.
    '''
    def __init__(self) -> None:
        self.logs: list[tuple[str, str]] = []

    def append_log(self, text: str, tag: str = 'info') -> None:
        '''
            Appends log message.
        '''
        self.logs.append((text, tag))

    def get_version(self) -> str:
        '''
            Returns mock version.
        '''
        return '1.0.2'


class TestElbowAutoSwitchCoordinator(TestCase):
    '''
        Unit tests verifying ElbowAutoSwitchCoordinator behavior.

        It defines:

            :methods:
                | setUp - Tests setUp.
                | test_structural_protocol_typing - Verifies ElbowAutoSwitchCoordinator satisfies protocol structurally.
                | test_try_auto_switch_success - Verifies reachable alternate IK toggles elbow and logs switch.
                | test_try_auto_switch_unreachable - Verifies unreachable alternate IK returns False without toggling mode.
                | test_get_version - Verifies semantic version string retrieval.
    '''

    def setUp(self) -> None:
        self.emulation_controller = _MockEmulationController()
        self.kinematics = _MockKinematics()
        self.log_listener = _MockLogListener()

        bundle = ElbowDependencies(
            emulation_controller=self.emulation_controller,
            kinematics=self.kinematics,
            log_listener=self.log_listener,
        )
        self.coordinator = ElbowAutoSwitchCoordinator(dependencies=bundle)

    def test_structural_protocol_typing(self) -> None:
        '''
            Verifies ElbowAutoSwitchCoordinator satisfies protocol structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.coordinator, IElbowAutoSwitchCoordinator)

    def test_try_auto_switch_success(self) -> None:
        '''
            Verifies reachable alternate IK toggles elbow and logs switch.

            :exceptions: None.
        '''
        self.emulation_controller.elbow_left = False
        self.kinematics.reachable = True

        target: ScaraPose = ScaraPose(x=150.0, y=-50.0, z=20.0, phi=0.0)
        result: bool = self.coordinator.try_auto_switch(target)

        self.assertTrue(result)
        self.assertTrue(self.emulation_controller.elbow_left)
        self.assertEqual(len(self.log_listener.logs), 1)
        self.assertIn('Lefty', self.log_listener.logs[0][0])

    def test_try_auto_switch_unreachable(self) -> None:
        '''
            Verifies unreachable alternate IK returns False without toggling mode.

            :exceptions: None.
        '''
        self.emulation_controller.elbow_left = True
        self.kinematics.reachable = False

        target: ScaraPose = ScaraPose(x=999.0, y=999.0, z=20.0, phi=0.0)
        result: bool = self.coordinator.try_auto_switch(target)

        self.assertFalse(result)
        self.assertTrue(self.emulation_controller.elbow_left)
        self.assertEqual(len(self.log_listener.logs), 0)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.coordinator.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
