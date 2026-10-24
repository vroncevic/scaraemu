# -*- coding: UTF-8 -*-

'''
Module
    iservice_test.py
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
    Unit test cases for IEmulationService structural protocol definition.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.iservice import IEmulationService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockEmulationService:
    '''
        Mock class satisfying IEmulationService structural protocol.

        It defines:

            :methods:
                | step - Advances simulation.
                | get_telemetry - Returns telemetry snapshot.
                | get_simulation_state - Returns simulation state.
                | clear_trail - Clears historical motion trail coordinates.
    '''

    def step(self, dt: float) -> bool:
        '''
            Advances simulation.

            :param dt: Time delta in seconds.
            :return: True if active.
            :exceptions: None.
        '''
        _ = dt
        return True

    def get_telemetry(self) -> Telemetry:
        '''
            Returns telemetry snapshot.

            :return: Telemetry model.
            :exceptions: None.
        '''
        return Telemetry(
            pose=ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0),
            joints=ScaraJoints(theta1=0.0, theta2=0.0, z=20.0, theta4=0.0, reachable=True),
            steps=ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0),
            is_hardware_connected=False,
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )

    def get_simulation_state(self) -> SimulationState:
        '''
            Returns simulation state.

            :return: SimulationState model.
            :exceptions: None.
        '''
        return SimulationState(
            is_animating=False,
            queue_depth=0,
            trail_points=((180.0, 0.0),),
            has_target=False,
            current_target=ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0),
        )

    def clear_trail(self) -> None:
        '''
            Clears historical motion trail coordinates.

            :exceptions: None.
        '''


class _IncompleteEmulationService:
    '''
        Mock class missing methods of IEmulationService.

        It defines:

            :methods:
                | step - Advances simulation.
                | get_version - Returns version string.
    '''

    def step(self, dt: float) -> bool:
        '''
            Advances simulation.

            :param dt: Time delta in seconds.
            :return: True if active.
            :exceptions: None.
        '''
        _ = dt
        return True

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__


class IEmulationServiceTestCase(TestCase):
    '''
        Test case verifying runtime checkability of IEmulationService.

        It defines:

            :methods:
                | test_structural_conformance - Verifies complete protocol conformance.
                | test_incomplete_conformance - Verifies rejection of incomplete class.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies complete protocol conformance.

            :exceptions: None.
        '''
        mock = _MockEmulationService()
        self.assertIsInstance(mock, IEmulationService)

    def test_incomplete_conformance(self) -> None:
        '''
            Verifies rejection of incomplete class.

            :exceptions: None.
        '''
        incomplete = _IncompleteEmulationService()
        self.assertNotIsInstance(incomplete, IEmulationService)


if __name__ == '__main__':
    unittest_main()
