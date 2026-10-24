# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Emulation mode and safety controller.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.service.emulation.controller.flags import EmulationFlags
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulationController:
    '''
        Controls emulation interlocks, motor enable, emergency stop, and kinematics mode.

        It defines:

            :attributes:
                | _flags - Emulation state flags reference.
                | _queue - Motion queue port reference.
            :methods:
                | __init__ - Initializes the emulation controller.
                | set_motors_enabled - Enables or disables virtual stepper motor power.
                | set_estop - Activates or clears emergency stop condition.
                | set_hold - Activates or clears feed-hold pause state.
                | set_elbow_mode - Sets kinematic elbow orientation mode.
                | get_flags - Returns current emulation state flags.
    '''

    _flags: EmulationFlags
    _queue: IEmulationQueue

    def __init__(
        self,
        *,
        flags: EmulationFlags,
        queue: IEmulationQueue,
    ) -> None:
        '''
            Initializes the emulation controller.

            :param flags: Emulation state flags reference.
            :param queue: Motion queue port reference.
            :exceptions: None.
        '''
        self._flags: Final[EmulationFlags] = flags
        self._queue: Final[IEmulationQueue] = queue

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables virtual stepper motor power stages.

            :param enabled: True to energize motors, False to unpower.
            :exceptions: None.
        '''
        self._flags.motors_enabled = enabled

        if not enabled:
            self._queue.clear_queue()

    def set_estop(self, active: bool) -> None:
        '''
            Sets emergency stop state, stopping motion and clearing queue.

            :param active: True to assert emergency stop, False to clear.
            :exceptions: None.
        '''
        self._flags.estop_active = active

        if active:
            self._queue.clear_queue()

    def set_hold(self, active: bool) -> None:
        '''
            Sets feed-hold pause state without clearing motion queue.

            :param active: True to pause motion progression, False to resume.
            :exceptions: None.
        '''
        self._flags.hold_active = active

    def set_elbow_mode(self, is_left: bool) -> None:
        '''
            Sets kinematic elbow orientation mode.

            :param is_left: True for Lefty configuration, False for Righty.
            :exceptions: None.
        '''
        self._flags.elbow_left = is_left

    def get_flags(self) -> EmulationFlags:
        '''
            Returns current emulation state flags.

            :return: EmulationFlags instance.
            :exceptions: None.
        '''
        return self._flags
