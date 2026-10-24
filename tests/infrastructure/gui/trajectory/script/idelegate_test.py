# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for IScriptLoaderDelegate protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyScriptLoaderDelegate:
    '''
        Dummy implementation satisfying IScriptLoaderDelegate.
    '''

    def handle_load_script(self, script_path: str) -> None:
        '''
            Tests handle load script.

            :param script_path: Input script_path.
            :exceptions: None.
        '''
        _ = script_path

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidScriptLoaderDelegate:
    '''
        Dummy class missing required protocol methods.
    '''

    def invalid_action(self) -> None:
        '''
            Tests invalid action.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestScriptLoaderDelegate(TestCase):
    '''
        Test cases verifying IScriptLoaderDelegate protocol conformance.

        It defines:

            :methods:
                | test_protocol_implementation - Verifies dummy delegate satisfies IScriptLoaderDelegate protocol.
                | test_protocol_rejection - Verifies incomplete class fails IScriptLoaderDelegate conformance.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies dummy delegate satisfies IScriptLoaderDelegate protocol.

            :exceptions: None.
        '''
        delegate = _DummyScriptLoaderDelegate()
        self.assertIsInstance(delegate, IScriptLoaderDelegate)

    def test_protocol_rejection(self) -> None:
        '''
            Verifies incomplete class fails IScriptLoaderDelegate conformance.

            :exceptions: None.
        '''
        delegate = _InvalidScriptLoaderDelegate()
        self.assertNotIsInstance(delegate, IScriptLoaderDelegate)


if __name__ == '__main__':
    unittest_main()
