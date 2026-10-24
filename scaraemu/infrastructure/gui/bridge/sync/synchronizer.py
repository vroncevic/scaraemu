# -*- coding: UTF-8 -*-

'''
Module
    synchronizer.py
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
    Synchronizer mediating hardware bridge state and telemetry with GUI view.
'''

from __future__ import annotations

from typing import Final

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.toolbar.connection.istatus_view import IConnectionStatusView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BridgeSynchronizer:
    '''
        Synchronizes hardware bridge state and telemetry with toolbar view.

        It defines:

            :attributes:
                | _status_view - Connection status view presentation port.
                | _connected - Hardware connection active flag.
                | _hardware_pose - Latest Cartesian pose received from hardware.
            :methods:
                | __init__ - Initializes bridge synchronizer with status view.
                | on_state_change - Updates hardware connection state in view.
                | on_telemetry - Updates latest hardware position telemetry.
                | get_state - Returns tuple of connected status and latest hardware pose.
                | get_version - Returns synchronizer version.
    '''

    _status_view: IConnectionStatusView
    _connected: bool
    _hardware_pose: ScaraPose

    def __init__(
        self,
        *,
        status_view: IConnectionStatusView,
    ) -> None:
        '''
            Initializes bridge synchronizer with status view.

            :param status_view: Connection status view presentation port.
            :exceptions: None.
        '''
        self._status_view: Final[IConnectionStatusView] = status_view
        self._connected: bool = False
        self._hardware_pose: ScaraPose = ScaraPose(
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
        )

    def on_state_change(self, connected: bool) -> None:
        '''
            Updates hardware connection state in view.

            :param connected: True if connected to hardware, False otherwise.
            :exceptions: None.
        '''
        self._connected = connected
        self._status_view.set_connected_state(connected)

    def on_telemetry(self, pose: ScaraPose) -> None:
        '''
            Dispatches hardware position telemetry.

            :param pose: Physical manipulator Cartesian pose coordinate.
            :exceptions: None.
        '''
        self._hardware_pose = pose

    def get_state(self) -> tuple[bool, ScaraPose]:
        '''
            Returns tuple of connected status and latest hardware pose.

            :return: Tuple containing connection flag and latest Cartesian pose.
            :exceptions: None.
        '''
        return (self._connected, self._hardware_pose)

    def get_version(self) -> str:
        '''
            Returns synchronizer version.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
