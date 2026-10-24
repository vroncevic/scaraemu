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
    Manual Cartesian and joint jog control panel composite container component.
'''

from __future__ import annotations

from tkinter import LabelFrame, Widget, X
from typing import Final

from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate
from scaraemu.infrastructure.gui.jog.dpad.section import JogDpad
from scaraemu.infrastructure.gui.jog.step.section import JogStepSection
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanel(LabelFrame):
    '''
        Composite container panel assembling jog step selection and directional D-pad.

        It defines:

            :attributes:
                | _step_section - Step distance resolution radio button section.
                | _dpad - Directional jog and homing button matrix.
            :methods:
                | __init__ - Initializes and packs child jog subcomponents.
                | get_sections - Returns tuple of jog subcomponents for inspection.
                | get_version - Returns composite panel version string.
    '''

    _step_section: JogStepSection
    _dpad: JogDpad

    def __init__(
        self,
        parent: Widget,
        *,
        jog_delegate: IJogActionDelegate,
    ) -> None:
        '''
            Initializes and packs child jog subcomponents.

            :param parent: Parent Tkinter widget container.
            :param jog_delegate: Delegate for incremental jog and homing.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Manual Jog Controls  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8,
        )

        self._step_section: Final[JogStepSection] = JogStepSection(self)
        self._step_section.pack(fill=X, pady=(0, 8))

        self._dpad: Final[JogDpad] = JogDpad(
            self,
            step_provider=self._step_section,
            delegate=jog_delegate,
        )
        self._dpad.pack(fill=X, pady=4)

    def get_sections(self) -> tuple[JogStepSection, JogDpad]:
        '''
            Returns tuple of jog subcomponents for inspection.

            :return: Tuple containing step section and dpad.
            :exceptions: None.
        '''
        return (self._step_section, self._dpad)

    def get_version(self) -> str:
        '''
            Returns composite panel version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
