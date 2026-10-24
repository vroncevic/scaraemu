# -*- coding: UTF-8 -*-

'''
Module
    notifier.py
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
    Motion waypoint completion notifier.
'''

from __future__ import annotations

from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionNotifier:
    '''
        Dispatches motion waypoint completion notifications to registered listeners.

        It defines:

            :attributes:
                | _completion_listeners - Registered waypoint completion listeners.
            :methods:
                | __init__ - Initializes the motion notifier.
                | set_completion_listener - Associates a motion waypoint completion listener.
                | notify_waypoint_completed - Dispatches completion event to registered listeners.
                | get_version - Returns motion notifier version string.
    '''

    _completion_listeners: list[IMotionCompletionListener]

    def __init__(self) -> None:
        '''
            Initializes the motion notifier.

            :exceptions: None.
        '''
        self._completion_listeners: list[IMotionCompletionListener] = []

    def set_completion_listener(self, listener: IMotionCompletionListener) -> None:
        '''
            Associates a motion waypoint completion listener.

            :param listener: IMotionCompletionListener collaborator.
            :exceptions: None.
        '''
        self._completion_listeners = [listener]

    def notify_waypoint_completed(self, seq_num: int) -> None:
        '''
            Dispatches completion event to registered listeners.

            :param seq_num: Sequence number of the completed waypoint.
            :exceptions: None.
        '''
        for listener in self._completion_listeners:
            listener.on_waypoint_completed(seq_num)

    def get_version(self) -> str:
        '''
            Returns motion notifier version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
