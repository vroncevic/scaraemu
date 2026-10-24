# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Dependencies bundle for InfrastructureFactory instantiation.
'''

from __future__ import annotations

from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.context.bundle import ContextBundle

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.notification.inotifier import IMotionNotifier
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class InfrastructureDependencies:
    '''
        Encapsulates required parameters and dependencies for InfrastructureFactory.

        :param base_bundle: Base bundle containing option manager.
        :param context_bundle: Context bundle for logging and preferences.
        :param bounds: Geometric and dynamic SCARA bounds.
        :param kinematics: Manipulator kinematics adapter service.
        :param emulation_service: Manipulator digital twin emulation and integration service.
        :param emulation_controller: Manipulator mode and safety controller port.
        :param emulation_queue: Motion trajectory waypoint queue port.
        :param motion_notifier: Waypoint completion motion notifier port.
        :param home_pose: Initial home pose coordinates.
        :param initial_script_path: Path to initial script file or empty.
    '''

    base_bundle: BaseBundle
    context_bundle: ContextBundle
    bounds: ScaraBounds
    kinematics: IManipulatorKinematics
    emulation_service: IEmulationService
    emulation_controller: IEmulationController
    emulation_queue: IEmulationQueue
    motion_notifier: IMotionNotifier
    home_pose: ScaraPose
    initial_script_path: str = ''
