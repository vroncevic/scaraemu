# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for LogAdapter and ILogListener protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.bridge.log.adapter import LogAdapter
from scaraemu.infrastructure.gui.console.ilog_listener import ILogListener
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LogAdapterTestCase(TestCase):
    '''
        Unit tests for LogAdapter operations.

        It defines:

            :methods:
                | test_implements_protocol_structurally - Verifies LogAdapter satisfies ILogListener.
                | test_append_log - Verifies log entry propagates to layout builder.
    '''

    def test_implements_protocol_structurally(self) -> None:
        '''
            Verifies LogAdapter satisfies ILogListener.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = LogAdapter(layout_builder=mock_builder)
        self.assertIsInstance(adapter, ILogListener)
        self.assertEqual(adapter.get_version(), '1.0.2')

    def test_append_log(self) -> None:
        '''
            Verifies log entry propagates to layout builder.

            :exceptions: None.
        '''
        mock_builder = MagicMock(spec=ILayoutBuilder)
        adapter = LogAdapter(layout_builder=mock_builder)
        adapter.append_log('Test message', 'info')
        mock_builder.append_log.assert_called_once_with('Test message', 'info')


if __name__ == '__main__':
    unittest_main()
