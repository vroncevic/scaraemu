# -*- coding: UTF-8 -*-

'''
Module
    assembly_test.py
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
    Unit test cases for GuiDelegatesAssembly value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.assembly import GuiDelegatesAssembly
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.server.manager.imanager import IVirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiDelegatesAssemblyTestCase(TestCase):
    '''
        Unit tests for GuiDelegatesAssembly.

        It defines:

            :methods:
                | test_assembly_attributes - Verifies assembly attribute assignment.
    '''

    def test_assembly_attributes(self) -> None:
        '''
            Verifies assembly attribute assignment.

            :exceptions: None.
        '''
        mock_delegates = MagicMock(spec=GuiDelegatesBundle)
        mock_target = MagicMock(spec=ITargetClickListener)
        mock_server = MagicMock(spec=IVirtualServerManager)

        assembly = GuiDelegatesAssembly(
            delegates=mock_delegates,
            target_click_coordinator=mock_target,
            server_manager=mock_server,
        )

        self.assertIs(assembly.delegates, mock_delegates)
        self.assertIs(assembly.target_click_coordinator, mock_target)
        self.assertIs(assembly.server_manager, mock_server)


if __name__ == '__main__':
    unittest_main()
