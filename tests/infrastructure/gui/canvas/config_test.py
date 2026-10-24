# -*- coding: UTF-8 -*-

'''
Module
    config_test.py
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
    Unit test cases for CanvasConfig parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasConfigTestCase(TestCase):
    '''
        Unit tests for CanvasConfig.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        mock_bounds = MagicMock(spec=ScaraBounds)
        mock_listener = MagicMock(spec=ITargetClickListener)
        config = CanvasConfig(
            bounds=mock_bounds,
            width=500,
            height=400,
            target_click_listener=mock_listener
        )
        self.assertIs(config.bounds, mock_bounds)
        self.assertEqual(config.width, 500)
        self.assertEqual(config.height, 400)
        self.assertIs(config.target_click_listener, mock_listener)


if __name__ == '__main__':
    unittest_main()
