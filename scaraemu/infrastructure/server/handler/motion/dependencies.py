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
    Parameter bundle dataclass encapsulating dependencies for motion command handler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.pose.iholder import IVirtualPlannedPoseHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MotionHandlerDependencies:
    '''
        Parameter bundle dataclass encapsulating dependencies for motion command handler.

        It defines:

            :attributes:
                | emulation_service - Manipulator digital twin emulation and integration service.
                | emulation_queue - Motion trajectory waypoint queue port.
                | pose_holder - Planned target pose state container.
                | kinematics - Forward and inverse kinematics calculator.
                | validator - Motion safety and dead zone validator adapter.
                | response_builder - Binary protocol wire response frame builder adapter.
                | decoder - Binary protocol payload decoder adapter.
                | log_listener - Server log message listener.
    '''

    emulation_service: IEmulationService
    emulation_queue: IEmulationQueue
    pose_holder: IVirtualPlannedPoseHolder
    kinematics: IManipulatorKinematics
    validator: IMotionValidatorAdapter
    response_builder: IBinaryResponseBuilderAdapter
    decoder: IBinaryPayloadDecoderAdapter
    log_listener: IServerLogListener
