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
    Composite container panel assembling machine configuration and safety controls.
'''

from __future__ import annotations

from tkinter import LabelFrame, Widget, X
from typing import Final

from scaraemu.infrastructure.gui.machine.configuration.idelegate import IConfigurationDelegate
from scaraemu.infrastructure.gui.machine.configuration.section import ConfigurationSection
from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate
from scaraemu.infrastructure.gui.machine.safety.section import SafetySection
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MachinePanel(LabelFrame):
    '''
        Composite container panel assembling machine configuration and safety overrides.

        It defines:

            :attributes:
                | _config_section - Machine orientation and motor power configuration section.
                | _safety_section - Feed-hold pause and emergency stop safety section.
            :methods:
                | __init__ - Initializes and packs child machine subcomponents.
                | get_sections - Returns child machine subcomponents tuple.
                | get_version - Returns composite panel version string.
    '''

    _config_section: ConfigurationSection
    _safety_section: SafetySection

    def __init__(
        self,
        parent: Widget,
        *,
        config_delegate: IConfigurationDelegate,
        safety_delegate: ISafetyDelegate,
    ) -> None:
        '''
            Initializes and packs child machine subcomponents.

            :param parent: Parent Tkinter widget container.
            :param config_delegate: Delegate for machine orientation and power.
            :param safety_delegate: Delegate for hold and emergency stop.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Machine Controls  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8,
        )

        self._config_section: Final[ConfigurationSection] = (
            ConfigurationSection(
                self,
                config_delegate=config_delegate,
            )
        )
        self._config_section.pack(fill=X, pady=(0, 6))

        self._safety_section: Final[SafetySection] = (
            SafetySection(
                self,
                safety_delegate=safety_delegate,
            )
        )
        self._safety_section.pack(fill=X)

    def get_sections(self) -> tuple[ConfigurationSection, SafetySection]:
        '''
            Returns child machine subcomponents tuple.

            :return: Tuple containing (configuration_section, safety_section).
            :exceptions: None.
        '''
        return (self._config_section, self._safety_section)

    def get_version(self) -> str:
        '''
            Returns composite panel version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
