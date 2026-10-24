# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Composite container panel assembling trajectory demo sections.
'''

from __future__ import annotations

from tkinter import LabelFrame, Widget, X
from typing import Final

from scaraemu.infrastructure.gui.theme.theme import ThemeManager
from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate
from scaraemu.infrastructure.gui.trajectory.preset.section import TrajectoryPresetSection
from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate
from scaraemu.infrastructure.gui.trajectory.queue.section import TrajectoryQueueSection
from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate
from scaraemu.infrastructure.gui.trajectory.script.section import ScriptLoaderSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoPanel(LabelFrame):
    '''
        Composite container panel assembling demo presets, script loader, and queue status.

        It defines:

            :attributes:
                | _preset_section - Preset autonomous trajectory button grid.
                | _script_section - Script and plan file loader sub-panel.
                | _queue_section - Queue depth monitor and clear action section.
            :methods:
                | __init__ - Initializes and packs child trajectory subcomponents.
                | queue_section - Returns the queue section leaf subcomponent.
                | get_sections - Returns child trajectory subcomponents for inspection.
                | get_version - Returns composite panel version string.
    '''

    _preset_section: TrajectoryPresetSection
    _script_section: ScriptLoaderSection
    _queue_section: TrajectoryQueueSection

    def __init__(
        self,
        parent: Widget,
        preset_delegate: ITrajectoryPresetDelegate,
        script_delegate: IScriptLoaderDelegate,
        queue_delegate: IQueueActionDelegate,
    ) -> None:
        '''
            Initializes and packs child trajectory subcomponents.

            :param parent: Parent Tkinter widget container.
            :param preset_delegate: Delegate for demo preset selection.
            :param script_delegate: Delegate for script and plan loading.
            :param queue_delegate: Delegate for queue flushing and control.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Demo Trajectories  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8,
        )

        self._preset_section: Final[TrajectoryPresetSection] = TrajectoryPresetSection(
            self,
            delegate=preset_delegate,
        )
        self._preset_section.pack(fill=X, pady=(0, 8))

        self._script_section: Final[ScriptLoaderSection] = ScriptLoaderSection(
            self,
            delegate=script_delegate,
        )
        self._script_section.pack(fill=X, pady=(4, 6))

        self._queue_section: Final[TrajectoryQueueSection] = TrajectoryQueueSection(
            self,
            delegate=queue_delegate,
        )
        self._queue_section.pack(fill=X, pady=(4, 0))

    @property
    def queue_section(self) -> TrajectoryQueueSection:
        '''
            Returns the queue section leaf subcomponent.

            :return: TrajectoryQueueSection instance.
            :exceptions: None.
        '''
        return self._queue_section

    def get_sections(
        self,
    ) -> tuple[TrajectoryPresetSection, ScriptLoaderSection, TrajectoryQueueSection]:
        '''
            Returns child trajectory subcomponents for inspection.

            :return: Tuple containing preset section, script section, and queue section.
            :exceptions: None.
        '''
        return (self._preset_section, self._script_section, self._queue_section)

    def get_version(self) -> str:
        '''
            Returns composite panel version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
