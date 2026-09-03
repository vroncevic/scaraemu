# -*- coding: UTF-8 -*-

'''
Module
    theme_manager_test.py
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
    Unit tests for ThemeManager.
'''

from __future__ import annotations

import unittest
from scaraemu.infrastructure.gui.theme import ThemeManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestThemeManager(unittest.TestCase):
    '''Unit test cases for ThemeManager.'''

    def test_theme_constants(self) -> None:
        '''Tests that theme constants are valid hex color codes and font names.'''
        self.assertTrue(ThemeManager.BG_DARK.startswith('#'))
        self.assertTrue(ThemeManager.ACCENT_CYAN.startswith('#'))
        self.assertTrue(ThemeManager.ACCENT_BLUE.startswith('#'))
        self.assertIsInstance(ThemeManager.FONT_FAMILY, str)


if __name__ == '__main__':
    unittest.main()
