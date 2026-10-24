# -*- coding: UTF-8 -*-

'''
Module
    irunner.py
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
    Interface protocol for GUI window and ticker execution lifecycle runners.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGuiLifecycleRunner(Protocol):
    '''
        Structural interface protocol for GUI window and ticker execution lifecycle.

        It defines:

            :methods:
                | run_lifecycle - Constructs root window, layouts, starts ticker and mainloop.
                | get_version - Returns lifecycle runner component version string.
    '''

    def run_lifecycle(
        self,
        *,
        bounds: ScaraBounds,
        target_click_listener: ITargetClickListener,
        delegates: GuiDelegatesBundle,
        layout_builder: ILayoutBuilder,
    ) -> None:
        '''
            Constructs root window, builds layout, starts ticker loop and main event loop.

            :param bounds: Manipulator kinematic boundaries.
            :param target_click_listener: Injected canvas click listener.
            :param delegates: Injected GUI action delegates bundle.
            :param layout_builder: Injected widget layout builder.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns lifecycle runner component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
