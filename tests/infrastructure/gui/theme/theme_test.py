# -*- coding: UTF-8 -*-

'''
Module
    theme_test.py
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
    Unit tests for ThemeManager class constants.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.theme.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThemeManagerTestCase(TestCase):
    '''
        Unit tests for ThemeManager.

        It defines:

            :methods:
                | test_color_constants - Verifies that theme color constants start with hash.
                | test_font_constants - Verifies that font family constants are non-empty strings.
                | test_palette_uniqueness - Verifies distinct background and foreground accent colors.
    '''

    def test_color_constants(self) -> None:
        '''
            Verifies that theme color constants start with hash.

            :exceptions: None.
        '''
        colors: list[str] = [
            ThemeManager.BG_DARK,
            ThemeManager.BG_PANEL,
            ThemeManager.BG_CANVAS,
            ThemeManager.BG_HEADER,
            ThemeManager.TEXT_PRIMARY,
            ThemeManager.TEXT_SECONDARY,
            ThemeManager.ACCENT_CYAN,
            ThemeManager.ACCENT_BLUE,
            ThemeManager.ACCENT_GREEN,
            ThemeManager.ACCENT_RED,
            ThemeManager.ACCENT_ORANGE,
            ThemeManager.ACCENT_YELLOW,
            ThemeManager.BORDER_COLOR,
        ]
        for color in colors:
            self.assertTrue(color.startswith('#'))
            self.assertEqual(len(color), 7)

    def test_font_constants(self) -> None:
        '''
            Verifies that font family constants are non-empty strings.

            :exceptions: None.
        '''
        self.assertIsInstance(ThemeManager.FONT_FAMILY, str)
        self.assertTrue(len(ThemeManager.FONT_FAMILY) > 0)
        self.assertIsInstance(ThemeManager.FONT_MONO, str)
        self.assertTrue(len(ThemeManager.FONT_MONO) > 0)

    def test_palette_uniqueness(self) -> None:
        '''
            Verifies distinct background and foreground accent colors.

            :exceptions: None.
        '''
        self.assertNotEqual(ThemeManager.BG_CANVAS, ThemeManager.ACCENT_CYAN)
        self.assertNotEqual(ThemeManager.TEXT_PRIMARY, ThemeManager.BG_DARK)


if __name__ == '__main__':
    unittest_main()
