# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Unit test cases for EmulationService implementation.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.motion.stepper import EmulationStepper
from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener
from scaraemu.core.service.emulation.notification.notifier import MotionNotifier
from scaraemu.core.service.emulation.queue.queue import EmulationQueue
from scaraemu.core.service.emulation.service import EmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationServiceTestCase(TestCase):
    '''
        Test case verifying behavior of EmulationService.

        It defines:

            :methods:
                | setUp - Initializes test fixture with collaborators.
                | test_implements_protocol - Verifies structural interface satisfaction.
                | test_get_telemetry_initial - Tests initial telemetry state.
                | test_get_simulation_state - Tests initial simulation state.
                | test_step_idle_when_empty - Tests simulation step when queue is empty.
                | test_enqueue_and_step - Tests stepping through trajectory.
                | test_estop_blocks_step - Tests that estop blocks simulation step.
                | test_motors_disabled_blocks_step - Tests that disabled motors block step.
                | test_hold_blocks_step - Tests feed-hold pause behavior during step.
                | test_planned_path_and_completion_notification - Tests notifications on completion.
                | test_step_trail_points_limit - Tests trail points ring buffer trimming.
                | test_clear_trail - Tests clearing motion trail points back to current pose.
    '''

    def setUp(self) -> None:
        self.kinematics = MagicMock(spec=IManipulatorKinematics)
        self.default_joints = ScaraJoints(
            theta1=0.0, theta2=0.0, z=20.0, theta4=0.0, reachable=True
        )
        self.default_steps = ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0)
        self.kinematics.solve_ik.return_value = self.default_joints
        self.kinematics.joints_to_steps.return_value = self.default_steps

        self.initial_pose = ScaraPose(x=180.0, y=0.0, z=20.0, phi=0.0)
        self.flags = EmulationFlags()
        self.queue = EmulationQueue(flags=self.flags)
        self.stepper = EmulationStepper(speed_mm_per_sec=100.0)
        self.notifier = MotionNotifier()
        self.service = EmulationService(
            kinematics=self.kinematics,
            flags=self.flags,
            queue=self.queue,
            stepper=self.stepper,
            notifier=self.notifier,
            initial_pose=self.initial_pose,
        )

    def test_implements_protocol(self) -> None:
        '''
            Tests that EmulationService satisfies IEmulationService structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.service, IEmulationService)

    def test_get_telemetry_initial(self) -> None:
        '''
            Tests initial telemetry query.

            :exceptions: None.
        '''
        telemetry = self.service.get_telemetry()
        self.assertEqual(telemetry.pose, self.initial_pose)
        self.assertEqual(telemetry.joints, self.default_joints)
        self.assertTrue(telemetry.motors_enabled)
        self.assertFalse(telemetry.estop_active)

    def test_get_simulation_state(self) -> None:
        '''
            Tests initial simulation state query.

            :exceptions: None.
        '''
        state = self.service.get_simulation_state()
        self.assertFalse(state.is_animating)
        self.assertEqual(state.queue_depth, 0)
        self.assertFalse(state.has_target)
        self.assertEqual(state.current_target, self.initial_pose)

    def test_step_idle_when_empty(self) -> None:
        '''
            Tests simulation step when queue is empty.

            :exceptions: None.
        '''
        self.assertFalse(self.service.step(0.01))

    def test_enqueue_and_step(self) -> None:
        '''
            Tests waypoint enqueuing and stepping through trajectory.

            :exceptions: None.
        '''
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        enqueued = self.queue.enqueue_waypoint(target)
        self.assertTrue(enqueued)

        moved = self.service.step(0.05)
        self.assertTrue(moved)
        telemetry = self.service.get_telemetry()
        self.assertAlmostEqual(telemetry.pose.x, 185.0)

        sim_state = self.service.get_simulation_state()
        self.assertTrue(sim_state.is_animating)

        moved = self.service.step(0.1)
        self.assertTrue(moved)
        telemetry = self.service.get_telemetry()
        self.assertEqual(telemetry.pose.x, 190.0)

        self.assertFalse(self.service.step(0.01))

    def test_estop_blocks_step(self) -> None:
        '''
            Tests that estop blocks simulation step.

            :exceptions: None.
        '''
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.flags.estop_active = True
        self.assertFalse(self.service.step(0.01))

    def test_motors_disabled_blocks_step(self) -> None:
        '''
            Tests that disabled motors block step.

            :exceptions: None.
        '''
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.flags.motors_enabled = False
        self.assertFalse(self.service.step(0.01))

    def test_hold_blocks_step(self) -> None:
        '''
            Tests feed-hold pause behavior during step.

            :exceptions: None.
        '''
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.flags.hold_active = True
        self.assertFalse(self.service.step(0.01))
        self.flags.hold_active = False
        self.assertTrue(self.service.step(0.01))

    def test_planned_path_and_completion_notification(self) -> None:
        '''
            Tests planned path telemetry and completion listener callbacks.

            :exceptions: None.
        '''
        mock_listener = MagicMock(spec=IMotionCompletionListener)
        self.notifier.set_completion_listener(mock_listener)
        target1 = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        target2 = ScaraPose(x=200.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target1, seq_num=10)
        self.queue.enqueue_waypoint(target2, seq_num=11)

        sim_state = self.service.get_simulation_state()
        self.assertEqual(sim_state.planned_path, ((190.0, 0.0), (200.0, 0.0)))

        self.service.step(0.15)
        mock_listener.on_waypoint_completed.assert_called_with(10)

        self.service.step(0.15)
        mock_listener.on_waypoint_completed.assert_called_with(11)

    def test_step_trail_points_limit(self) -> None:
        '''
            Tests trail points ring buffer trimming beyond 5000 items.

            :exceptions: None.
        '''
        trail: list[tuple[float, float]] = getattr(self.service, '_trail_points')
        trail.clear()
        trail.extend([(0.0, 0.0)] * 5000)
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.assertTrue(self.service.step(0.01))
        self.assertEqual(len(self.service.get_simulation_state().trail_points), 5000)

    def test_clear_trail(self) -> None:
        '''
            Tests clearing motion trail points back to current pose.

            :exceptions: None.
        '''
        target = ScaraPose(x=190.0, y=0.0, z=20.0, phi=0.0)
        self.queue.enqueue_waypoint(target)
        self.service.step(0.05)
        self.assertGreater(len(self.service.get_simulation_state().trail_points), 1)

        self.service.clear_trail()
        trail = self.service.get_simulation_state().trail_points
        self.assertEqual(len(trail), 1)
        current = self.service.get_telemetry().pose
        self.assertEqual(trail[0], (current.x, current.y))


if __name__ == '__main__':
    unittest_main()
