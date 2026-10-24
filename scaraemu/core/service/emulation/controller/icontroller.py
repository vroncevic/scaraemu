# -*- coding: UTF-8 -*-

'''
Module
    icontroller.py
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
    Interface protocol defining control commands for digital twin emulation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.service.emulation.controller.flags import EmulationFlags

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEmulationController(Protocol):
    '''
        Structural interface protocol for controlling manipulator state and queue.

        It defines:

            :methods:
                | set_motors_enabled - Enables or disables virtual stepper motor power.
                | set_estop - Activates or clears emergency stop condition.
                | set_hold - Activates or clears feed-hold pause without clearing queue.
                | set_elbow_mode - Toggles between Lefty and Righty kinematic mode.
                | get_flags - Returns current emulation state flags.
    '''

    def set_motors_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables virtual stepper motor drivers.

            :param enabled: True to energize motors, False to unpower.
        '''

    def set_estop(self, active: bool) -> None:
        '''
            Sets emergency stop state, immediately stopping motion.

            :param active: True to assert emergency stop, False to clear.
        '''

    def set_hold(self, active: bool) -> None:
        '''
            Sets feed-hold pause state without clearing motion queue.

            :param active: True to pause motion progression, False to resume.
        '''

    def set_elbow_mode(self, is_left: bool) -> None:
        '''
            Sets kinematic elbow orientation mode.

            :param is_left: True for Lefty configuration, False for Righty.
        '''

    def get_flags(self) -> EmulationFlags:
        '''
            Returns current emulation state flags.

            :return: EmulationFlags instance.
        '''
