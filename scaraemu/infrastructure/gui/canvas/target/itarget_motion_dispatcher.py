# -*- coding: UTF-8 -*-

'''
Module
    itarget_motion_dispatcher.py
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
    Interface protocol for dispatching validated canvas target motions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITargetMotionDispatcher(Protocol):
    '''
        Defines structural contract for dispatching accepted canvas target motions.

        It defines:

            :methods:
                | dispatch_motion - Queues target pose and dispatches hardware move.
                | get_version - Returns protocol version string.
    '''

    def dispatch_motion(self, target_pose: ScaraPose) -> None:
        '''
            Queues target pose and dispatches hardware move.

            :param target_pose: Validated target pose to dispatch.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns protocol version string.

            :return: Version string.
            :exceptions: None.
        '''
