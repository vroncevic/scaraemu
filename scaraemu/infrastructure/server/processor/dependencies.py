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
    Parameter bundle dataclass encapsulating dependencies for binary frame processor.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class BinaryProcessorDependencies:
    '''
        Parameter bundle dataclass encapsulating dependencies for binary frame processor assembly.

        It defines:

            :attributes:
                | emulation_controller - Emulation safety and mode controller.
                | emulation_service - Manipulator digital twin emulation and integration service.
                | emulation_queue - Motion trajectory waypoint queue service.
                | kinematics - Forward and inverse kinematics calculator.
                | response_builder - Binary protocol wire response frame builder adapter.
                | decoder - Injected binary payload decoder adapter.
                | home_pose - Manipulator canonical home pose.
                | motion_validator - Injected motion safety and dead zone validator adapter.
                | log_listener - Injected server log listener for console diagnostics.
    '''

    emulation_controller: IEmulationController
    emulation_service: IEmulationService
    emulation_queue: IEmulationQueue
    kinematics: IManipulatorKinematics
    response_builder: IBinaryResponseBuilderAdapter
    decoder: IBinaryPayloadDecoderAdapter
    home_pose: ScaraPose
    motion_validator: IMotionValidatorAdapter
    log_listener: IServerLogListener
