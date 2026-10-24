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
    Real-time telemetry readout and hardware status monitor composite container panel.
'''

from __future__ import annotations

from tkinter import BOTH, Frame, LabelFrame, Widget, X
from typing import Final

from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.telemetry.cartesian.section import CartesianSection
from scaraemu.infrastructure.gui.telemetry.joint.section import JointSection
from scaraemu.infrastructure.gui.telemetry.step.section import StepSection
from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPanel(LabelFrame):
    '''
        Composite container panel assembling Cartesian, joint, and stepper telemetry sections.

        It defines:

            :attributes:
                | _cartesian_section - Cartesian pose telemetry readout section.
                | _joint_section - Robot joint angles telemetry readout section.
                | _step_section - Stepper motor step counts telemetry readout section.
            :methods:
                | __init__ - Initializes telemetry layout and child sections.
                | update_telemetry - Updates display values across all telemetry sections.
                | get_sections - Returns child telemetry subcomponents tuple.
                | get_version - Returns telemetry panel component version string.
    '''

    _cartesian_section: CartesianSection
    _joint_section: JointSection
    _step_section: StepSection

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes telemetry layout and child sections.

            :param parent: Parent Tkinter widget container.
            :exceptions: None.
        '''
        super().__init__(
            parent,
            text='  Live Robot Telemetry  ',
            bg=ThemeManager.BG_PANEL,
            fg=ThemeManager.ACCENT_CYAN,
            font=(ThemeManager.FONT_FAMILY, 9, 'bold'),
            padx=10,
            pady=8,
        )

        content: Frame = Frame(self, bg=ThemeManager.BG_PANEL)
        content.pack(fill=BOTH, expand=True)

        self._cartesian_section: Final[CartesianSection] = CartesianSection(content)
        self._cartesian_section.pack(fill=X)

        sep1: Frame = Frame(content, height=1, bg=ThemeManager.BORDER_COLOR)
        sep1.pack(fill=X, pady=5)

        self._joint_section: Final[JointSection] = JointSection(content)
        self._joint_section.pack(fill=X)

        sep2: Frame = Frame(content, height=1, bg=ThemeManager.BORDER_COLOR)
        sep2.pack(fill=X, pady=5)

        self._step_section: Final[StepSection] = StepSection(content)
        self._step_section.pack(fill=X)

    def update_telemetry(self, telem: Telemetry) -> None:
        '''
            Updates display values across all telemetry sections from Telemetry snapshot.

            :param telem: Current Telemetry snapshot.
            :exceptions: None.
        '''
        if not self.winfo_ismapped():
            return

        self._cartesian_section.update_pose(telem.pose)
        self._joint_section.update_joints(telem.joints)
        self._step_section.update_steps(telem.steps)

    def get_sections(self) -> tuple[CartesianSection, JointSection, StepSection]:
        '''
            Returns child telemetry subcomponents tuple.

            :return: Tuple containing (cartesian, joint, step) sections.
            :exceptions: None.
        '''
        return (
            self._cartesian_section,
            self._joint_section,
            self._step_section,
        )

    def get_version(self) -> str:
        '''
            Returns telemetry panel component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
