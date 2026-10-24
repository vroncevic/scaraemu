# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Bundle encapsulating user action and interaction delegates for the GUI.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate
from scaraemu.infrastructure.gui.machine.configuration.idelegate import IConfigurationDelegate
from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate as IToolbarActionDelegate
from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate
from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate
from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class GuiDelegatesBundle:
    '''
        Bundle encapsulating all user interaction and action delegates for GUI.

        It defines:

            :attributes:
                | jog - Action delegate for manual jog operations.
                | config - Action delegate for machine configuration operations.
                | safety - Action delegate for machine safety operations.
                | preset - Action delegate for demo preset operations.
                | script - Action delegate for script loading operations.
                | serial_bar - Action delegate for top serial toolbar.
                | queue - Action delegate for motion queue flushing.
    '''

    jog: IJogActionDelegate
    config: IConfigurationDelegate
    safety: ISafetyDelegate
    preset: ITrajectoryPresetDelegate
    script: IScriptLoaderDelegate
    serial_bar: IToolbarActionDelegate
    queue: IQueueActionDelegate
