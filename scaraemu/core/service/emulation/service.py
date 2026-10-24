# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Concrete digital twin manipulator emulation service.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.simulation.state import SimulationState
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.notification.notifier import MotionNotifier
from scaraemu.core.service.emulation.queue.queue import EmulationQueue, EmulationQueueSnapshot
from scaraemu.core.service.emulation.motion.stepper import EmulationStepper
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationService:
    '''
        Executes manipulator digital twin emulation, motion progression, and telemetry.

        It defines:

            :attributes:
                | _kinematics - Injected kinematics solver port.
                | _flags - State flags for interlocks and orientation modes.
                | _queue - Motion queue manager.
                | _stepper - Motion step interpolator.
                | _notifier - Waypoint completion notifier.
                | _current_pose - Current simulated Cartesian pose.
                | _trail_points - Historical 2D path coordinates for visualization.
            :methods:
                | __init__ - Initializes the emulation service with collaborating components.
                | step - Advances simulation by time delta in seconds.
                | get_telemetry - Returns live telemetry snapshot DTO.
                | get_simulation_state - Returns animation and queue state snapshot DTO.
                | clear_trail - Clears historical motion trail coordinates and resets to current pose.
    '''

    _kinematics: IManipulatorKinematics
    _flags: EmulationFlags
    _queue: EmulationQueue
    _stepper: EmulationStepper
    _notifier: MotionNotifier
    _current_pose: ScaraPose
    _trail_points: list[tuple[float, float]]

    def __init__(
        self,
        *,
        kinematics: IManipulatorKinematics,
        flags: EmulationFlags,
        queue: EmulationQueue,
        stepper: EmulationStepper,
        notifier: MotionNotifier,
        initial_pose: ScaraPose,
    ) -> None:
        '''
            Initializes the emulation service with collaborating components.

            :param kinematics: Injected IManipulatorKinematics solver.
            :param flags: Injected EmulationFlags state flags.
            :param queue: Injected EmulationQueue manager.
            :param stepper: Injected EmulationStepper interpolator.
            :param notifier: Injected MotionNotifier completion notifier.
            :param initial_pose: Mandatory starting Cartesian pose.
            :exceptions: None.
        '''
        self._kinematics: Final[IManipulatorKinematics] = kinematics
        self._flags: Final[EmulationFlags] = flags
        self._queue: Final[EmulationQueue] = queue
        self._stepper: Final[EmulationStepper] = stepper
        self._notifier: Final[MotionNotifier] = notifier
        self._current_pose: ScaraPose = initial_pose
        self._trail_points: list[tuple[float, float]] = [(initial_pose.x, initial_pose.y)]

    def step(self, dt: float) -> bool:
        '''
            Advances simulation by delta time in seconds.

            :param dt: Time delta in seconds.
            :return: True if motion occurred, False if idle or stopped.
            :exceptions: None.
        '''
        if self._flags.estop_active or not self._flags.motors_enabled or self._flags.hold_active:
            return False

        active = self._queue.get_active_or_next()

        if not active:
            return False

        target, seq_num = active
        self._current_pose, arrived = self._stepper.step_towards(
            self._current_pose, target, dt
        )

        if arrived:
            self._queue.complete_active()
            self._notifier.notify_waypoint_completed(seq_num)

        self._trail_points.append((self._current_pose.x, self._current_pose.y))

        if len(self._trail_points) > 5000:
            self._trail_points.pop(0)

        return True

    def get_telemetry(self) -> Telemetry:
        '''
            Builds and returns comprehensive live telemetry snapshot.

            :return: Live Telemetry snapshot DTO.
            :exceptions: None.
        '''
        joints: ScaraJoints = self._kinematics.solve_ik(
            self._current_pose, self._flags.elbow_left
        )
        steps = self._kinematics.joints_to_steps(joints)

        return Telemetry(
            pose=self._current_pose,
            joints=joints,
            steps=steps,
            is_hardware_connected=False,
            motors_enabled=self._flags.motors_enabled,
            estop_active=self._flags.estop_active,
            hold_active=self._flags.hold_active,
            elbow_left=self._flags.elbow_left,
        )

    def get_simulation_state(self) -> SimulationState:
        '''
            Builds and returns simulation queue and trail state snapshot.

            :return: Live SimulationState snapshot DTO.
            :exceptions: None.
        '''
        snapshot: EmulationQueueSnapshot = self._queue.get_snapshot(self._current_pose)

        return SimulationState(
            is_animating=snapshot.has_target or snapshot.queue_depth > 0,
            queue_depth=snapshot.queue_depth,
            trail_points=tuple(self._trail_points),
            has_target=snapshot.has_target,
            current_target=snapshot.current_target,
            planned_path=snapshot.planned_path,
        )

    def clear_trail(self) -> None:
        '''
            Clears historical motion trail coordinates and resets to current pose.

            :exceptions: None.
        '''
        self._trail_points = [(self._current_pose.x, self._current_pose.y)]
