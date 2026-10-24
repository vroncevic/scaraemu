# -*- coding: UTF-8 -*-

'''
Module
    elbow_auto_switch_coordinator.py
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
    Coordinates automatic elbow configuration switching when target pose is unreachable.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.gui.canvas.target.elbow_dependencies import ElbowDependencies
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ElbowAutoSwitchCoordinator:
    '''
        Evaluates alternate elbow inverse kinematics and auto-switches elbow mode.

        It defines:

            :attributes:
                | _emulation_controller - Manipulator mode state controller.
                | _kinematics - Forward and inverse kinematics solver port.
                | _log_listener - Logging sink for host diagnostics.
            :methods:
                | __init__ - Initializes coordinator with state and kinematics ports.
                | try_auto_switch - Evaluates alternate elbow IK and applies switch if reachable.
                | get_version - Returns coordinator component version string.
    '''

    _emulation_controller: IEmulationController
    _kinematics: IManipulatorKinematics
    _log_listener: ILogListener

    def __init__(
        self,
        dependencies: ElbowDependencies,
    ) -> None:
        '''
            Initializes coordinator with dependencies bundle.

            :param dependencies: Elbow auto-switch coordinator dependencies bundle.
            :exceptions: None.
        '''
        self._emulation_controller: Final[IEmulationController] = (
            dependencies.emulation_controller
        )
        self._kinematics: Final[IManipulatorKinematics] = dependencies.kinematics
        self._log_listener: Final[ILogListener] = dependencies.log_listener

    def try_auto_switch(self, target_pose: ScaraPose) -> bool:
        '''
            Evaluates alternate elbow IK and applies switch if reachable.

            :param target_pose: Target pose to evaluate with alternate elbow.
            :return: True if switch succeeded and target is reachable, False otherwise.
            :exceptions: None.
        '''
        curr_left: bool = self._emulation_controller.get_flags().elbow_left
        other_left: bool = not curr_left
        alt_joints: ScaraJoints = self._kinematics.solve_ik(
            target_pose, other_left
        )

        if not alt_joints.reachable:
            return False

        self._emulation_controller.set_elbow_mode(other_left)
        mode_str: str = 'Lefty' if other_left else 'Righty'
        self._log_listener.append_log(
            f'[HOST]: Auto-switched to {mode_str} mode for target '
            f'({target_pose.x:.1f}, {target_pose.y:.1f})',
            'info',
        )
        return True

    def get_version(self) -> str:
        '''
            Returns coordinator component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
