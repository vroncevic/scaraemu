# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for InfrastructureProvides.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.provides import InfrastructureProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfrastructureProvides(TestCase):
    '''
        Test cases verifying InfrastructureProvides.

        It defines:

            :methods:
                | test_provides_creation - Verifies provides properties.
    '''

    def test_provides_creation(self) -> None:
        '''
            Verifies provides properties.

            :exceptions: None.
        '''
        mock_gui = MagicMock(spec=IGUI)
        mock_cli = MagicMock(spec=ICLI)

        provides = InfrastructureProvides(
            gui=mock_gui,
            cli=mock_cli,
        )

        self.assertIs(provides.gui, mock_gui)
        self.assertIs(provides.cli, mock_cli)


if __name__ == '__main__':
    unittest_main()
