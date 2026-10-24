# -*- coding: UTF-8 -*-

'''
Module
    target_dependencies.py
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
    Parameter bundle dataclass for TargetActionCoordinator collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.target.ielbow_auto_switch_coordinator import IElbowAutoSwitchCoordinator
from scaraemu.infrastructure.gui.canvas.target.itarget_motion_dispatcher import ITargetMotionDispatcher
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


@dataclass(frozen=True, slots=True)
class TargetDependencies:
    '''
        Parameter bundle dataclass for TargetActionCoordinator collaborators.

        It defines:

            :attributes:
                | emulation_service - Active emulation and telemetry query port.
                | validator - Pose safety and reachability validator.
                | elbow_coordinator - Elbow auto-switch coordinator.
                | motion_dispatcher - Target motion queue and stream dispatcher.
                | log_listener - Logging sink for host diagnostics.
                | bypass_adapter - Dead zone avoidance and bypass trajectory adapter.
            :methods: None.
    '''

    emulation_service: IEmulationService
    validator: IMotionValidatorAdapter
    elbow_coordinator: IElbowAutoSwitchCoordinator
    motion_dispatcher: ITargetMotionDispatcher
    log_listener: ILogListener
    bypass_adapter: IDeadZoneBypassAdapter
