# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for TelemetryPanel composite container component.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.telemetry.cartesian.section import CartesianSection
from scaraemu.infrastructure.gui.telemetry.joint.section import JointSection
from scaraemu.infrastructure.gui.telemetry.panel import TelemetryPanel
from scaraemu.infrastructure.gui.telemetry.step.section import StepSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTelemetryPanel(TestCase):
    '''
        Unit tests for TelemetryPanel.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_panel_and_properties - Tests panel creation, subcomponents access, and version inquiry.
                | test_update_telemetry - Tests dispatching full Telemetry snapshot.
                | test_update_telemetry_not_mapped - Tests early return when unmapped.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_panel_and_properties(self) -> None:
        '''
            Tests panel creation, subcomponents access, and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        panel = TelemetryPanel(self._root)
        panel.pack()

        cart_sec, joint_sec, step_sec = panel.get_sections()
        self.assertIsInstance(cart_sec, CartesianSection)
        self.assertIsInstance(joint_sec, JointSection)
        self.assertIsInstance(step_sec, StepSection)
        self.assertEqual(panel.get_version(), '1.0.2')

    def test_update_telemetry(self) -> None:
        '''
            Tests dispatching full Telemetry snapshot.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        panel = TelemetryPanel(self._root)
        panel.pack()
        self._root.update_idletasks()

        telem = Telemetry(
            pose=ScaraPose(x=100.0, y=50.0, z=20.0, phi=0.0),
            joints=ScaraJoints(
                theta1=0.5,
                theta2=1.0,
                z=0.0,
                theta4=0.0,
                reachable=True,
            ),
            steps=ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=300, j4_steps=400),
            is_hardware_connected=True,
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )

        panel.update_telemetry(telem)
        cart_sec, _, step_sec = panel.get_sections()
        self.assertEqual(cart_sec.get_readouts()[0], '100.00 mm')
        self.assertEqual(step_sec.get_readouts()[0], '100')

    def test_update_telemetry_not_mapped(self) -> None:
        '''
            Tests update_telemetry returns early when panel is not mapped.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        panel = TelemetryPanel(self._root)
        telem = Telemetry(
            pose=ScaraPose(x=100.0, y=50.0, z=20.0, phi=0.0),
            joints=ScaraJoints(
                theta1=0.5,
                theta2=1.0,
                z=0.0,
                theta4=0.0,
                reachable=True,
            ),
            steps=ScaraStepCoords(j1_steps=100, j2_steps=200, z_steps=300, j4_steps=400),
            is_hardware_connected=True,
            motors_enabled=True,
            estop_active=False,
            hold_active=False,
            elbow_left=False,
        )
        panel.update_telemetry(telem)
        cart_sec, _, _ = panel.get_sections()
        self.assertEqual(cart_sec.get_readouts()[0], '0.00 mm')


if __name__ == '__main__':
    unittest_main()
