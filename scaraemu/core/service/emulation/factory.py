# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring emulation subsystem components.
'''

from __future__ import annotations

from scaraemu.core.service.emulation.controller.controller import EmulationController
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.notification.notifier import MotionNotifier
from scaraemu.core.service.emulation.provides import EmulationProvides
from scaraemu.core.service.emulation.queue.queue import EmulationQueue
from scaraemu.core.service.emulation.service import EmulationService
from scaraemu.core.service.emulation.motion.stepper import EmulationStepper

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationFactory:
    '''
        Factory instantiating and wiring emulation subsystem components.

        It defines:

            :methods:
                | create - Builds and returns an EmulationProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: EmulationDependencies) -> EmulationProvides:
        '''
            Builds and returns an EmulationProvides container.

            :param dependencies: Encapsulated emulation dependencies.
            :return: EmulationProvides instance.
            :exceptions: None.
        '''
        flags = EmulationFlags()
        queue = EmulationQueue(flags=flags)
        controller = EmulationController(flags=flags, queue=queue)
        notifier = MotionNotifier()
        stepper = EmulationStepper(speed_mm_per_sec=dependencies.speed_mm_per_sec)
        service = EmulationService(
            kinematics=dependencies.kinematics,
            flags=flags,
            queue=queue,
            stepper=stepper,
            notifier=notifier,
            initial_pose=dependencies.initial_pose,
        )

        return EmulationProvides(
            service=service,
            controller=controller,
            queue=queue,
            notifier=notifier,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
