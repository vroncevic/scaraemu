# -*- coding: UTF-8 -*-

'''
Module
    theme.py
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
    Centralized theme manager and style constants for SCARA emulator GUI.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ThemeManager:
    '''
        Theme colors, fonts, and styling parameters for the SCARA emulator GUI.

        It defines:

            :attributes:
                | BG_DARK - Primary background dark tone (#1e1e2e).
                | BG_PANEL - Sidebar panel container background (#252538).
                | BG_CANVAS - Rendering canvas background (#181825).
                | BG_HEADER - Header toolbar background (#181824).
                | TEXT_PRIMARY - High contrast label text (#cdd6f4).
                | TEXT_SECONDARY - Muted descriptive text (#a6adc8).
                | ACCENT_CYAN - Primary accent color (#89dceb).
                | ACCENT_BLUE - Secondary accent color (#89b4fa).
                | ACCENT_GREEN - Status active / OK color (#a6e3a1).
                | ACCENT_RED - Alert / E-Stop / Error color (#f38ba8).
                | ACCENT_ORANGE - Warning / Reach limit color (#fab387).
                | ACCENT_YELLOW - Trajectory path point color (#f9e2af).
                | BORDER_COLOR - Widget border tone (#313244).
                | FONT_FAMILY - UI default typography family.
                | FONT_MONO - Telemetry & numerical typography family.
    '''

    BG_DARK: ClassVar[str] = '#1e1e2e'
    BG_PANEL: ClassVar[str] = '#252538'
    BG_CANVAS: ClassVar[str] = '#181825'
    BG_HEADER: ClassVar[str] = '#181824'

    TEXT_PRIMARY: ClassVar[str] = '#cdd6f4'
    TEXT_SECONDARY: ClassVar[str] = '#a6adc8'

    ACCENT_CYAN: ClassVar[str] = '#89dceb'
    ACCENT_BLUE: ClassVar[str] = '#89b4fa'
    ACCENT_GREEN: ClassVar[str] = '#a6e3a1'
    ACCENT_RED: ClassVar[str] = '#f38ba8'
    ACCENT_ORANGE: ClassVar[str] = '#fab387'
    ACCENT_YELLOW: ClassVar[str] = '#f9e2af'

    BORDER_COLOR: ClassVar[str] = '#313244'

    FONT_FAMILY: ClassVar[str] = 'Segoe UI'
    FONT_MONO: ClassVar[str] = 'Consolas'
