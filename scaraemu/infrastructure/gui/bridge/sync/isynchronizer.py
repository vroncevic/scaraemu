# -*- coding: UTF-8 -*-

'''
Module
    isynchronizer.py
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
    Interface protocol for hardware bridge state and telemetry synchronization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBridgeSynchronizer(Protocol):
    '''
        Structural protocol for synchronizing hardware bridge state and telemetry with GUI.

        It defines:

            :methods:
                | on_state_change - Handles serial connection state changes.
                | on_telemetry - Handles physical manipulator position telemetry.
                | get_version - Returns synchronizer interface version.
    '''

    def on_state_change(self, connected: bool) -> None:
        '''
            Handles serial connection state changes.

            :param connected: True if connected to hardware, False otherwise.
            :exceptions: None.
        '''

    def on_telemetry(self, pose: ScaraPose) -> None:
        '''
            Handles physical manipulator position telemetry.

            :param pose: ScaraPose coordinate snapshot reported by hardware.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns synchronizer interface version.

            :return: Semantic version string.
            :exceptions: None.
        '''
