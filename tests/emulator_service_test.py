# -*- coding: UTF-8 -*-

'''
Module
    emulator_service_test.py
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
    Unit tests for EmulatorService simulation engine.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.service.kinematics_service import KinematicsService
from scaraemu.core.service.emulator_service import EmulatorService
from scaraemu.core.service.demo_generator import TrajectoryDemoGenerator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestEmulatorService(unittest.TestCase):
    '''Unit test cases for EmulatorService.'''

    def setUp(self) -> None:
        '''Sets up emulator service instance.'''
        self.geom = ScaraGeometry(l1=150.0, l2=120.0)
        self.kin = KinematicsService(geometry=self.geom)
        self.emu = EmulatorService(kinematics=self.kin, initial_pose=ScaraPose(x=180.0, y=0.0, z=20.0))

    def test_initial_state(self) -> None:
        '''Tests initial pose and telemetry readout.'''
        pose = self.emu.get_current_pose()
        self.assertEqual(pose.x, 180.0)
        self.assertEqual(pose.y, 0.0)
        self.assertEqual(pose.z, 20.0)

        telem = self.emu.get_telemetry()
        self.assertTrue(telem.motors_enabled)
        self.assertFalse(telem.estop_active)

    def test_direct_move(self) -> None:
        '''Tests immediate direct pose update without queue.'''
        target = ScaraPose(x=160.0, y=30.0, z=15.0)
        success = self.emu.set_target_pose(target, direct=True)
        self.assertTrue(success)
        self.assertEqual(self.emu.get_current_pose().x, 160.0)

    def test_interpolated_motion_queue(self) -> None:
        '''Tests queued motion and step_simulation progression.'''
        target = ScaraPose(x=185.0, y=10.0, z=20.0)
        success = self.emu.set_target_pose(target, direct=False)
        self.assertTrue(success)

        state = self.emu.get_simulation_state()
        self.assertTrue(state.is_animating)
        self.assertGreater(state.queue_depth, 0)

        # Step through until queue is emptied
        while self.emu.step_simulation():
            pass

        self.assertAlmostEqual(self.emu.get_current_pose().x, 185.0, places=1)
        self.assertAlmostEqual(self.emu.get_current_pose().y, 10.0, places=1)

    def test_estop_and_clear_queue(self) -> None:
        '''Tests emergency stop clearing queue.'''
        target = ScaraPose(x=170.0, y=40.0, z=20.0)
        self.emu.set_target_pose(target, direct=False)
        self.assertGreater(self.emu.get_simulation_state().queue_depth, 0)

        self.emu.set_estop(True)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, 0)
        self.assertTrue(self.emu.get_telemetry().estop_active)

    def test_hold_and_resume(self) -> None:
        '''Tests feed-hold pausing motion queue without clearing it.'''
        target = ScaraPose(x=185.0, y=10.0, z=20.0)
        self.emu.set_target_pose(target, direct=False)
        initial_depth = self.emu.get_simulation_state().queue_depth
        self.assertGreater(initial_depth, 0)

        self.emu.set_hold(True)
        self.assertTrue(self.emu.get_telemetry().hold_active)
        stepped = self.emu.step_simulation()
        self.assertFalse(stepped)
        self.assertEqual(self.emu.get_simulation_state().queue_depth, initial_depth)

        self.emu.set_hold(False)
        self.assertFalse(self.emu.get_telemetry().hold_active)
        stepped = self.emu.step_simulation()
        self.assertTrue(stepped)

    def test_demo_generators(self) -> None:
        '''Tests preset demo trajectory point generators.'''
        circle = TrajectoryDemoGenerator.generate_circle(center_x=150.0, center_y=0.0, radius=30.0, z=20.0)
        self.assertGreater(len(circle), 10)

        square = TrajectoryDemoGenerator.generate_square(center_x=150.0, center_y=0.0, side=50.0, z=20.0)
        self.assertEqual(len(square), 5)

        star = TrajectoryDemoGenerator.generate_star(center_x=150.0, center_y=0.0, r_outer=40.0, r_inner=20.0, z=20.0)
        self.assertEqual(len(star), 11)

        helix = TrajectoryDemoGenerator.generate_helix(center_x=150.0, center_y=0.0, radius=30.0, z_start=10.0, z_end=50.0)
        self.assertGreater(len(helix), 50)

    def test_update_hardware_pose(self) -> None:
        '''Tests updating robot pose directly from hardware telemetry.'''
        hw_pose = ScaraPose(x=200.0, y=50.0, z=30.0, phi=0.2)
        self.emu.update_hardware_pose(hw_pose)
        self.assertEqual(self.emu.get_current_pose().x, 200.0)
        self.assertEqual(self.emu.get_current_pose().y, 50.0)
        self.assertEqual(self.emu.get_current_pose().z, 30.0)
        self.assertTrue(self.emu.get_current_joints().reachable)



if __name__ == '__main__':
    unittest.main()
