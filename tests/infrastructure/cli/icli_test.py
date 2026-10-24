# -*- coding: UTF-8 -*-

'''
Module
    icli_test.py
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
    Unit tests for ICLI structural protocol.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.cli.icli import ICLI


class _DummyCLI:
    '''
        Dummy class conforming to ICLI structurally.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the CLI adapter is initialized.

            :exceptions: None.
        '''
        return True

    def run(self) -> Mapping[str, object]:
        '''
            Executes CLI command line parsing and strategy dispatch.

            :exceptions: None.
        '''
        return {'status': 0}


class _InvalidCLI:
    '''
        Dummy class missing required protocol methods.
    '''
    pass


class TestICLI(TestCase):
    '''
        Test cases verifying ICLI structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy conforming class satisfies ICLI structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy ICLI.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies ICLI structurally.

            :exceptions: None.
        '''
        cli = _DummyCLI()
        self.assertIsInstance(cli, ICLI)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy ICLI.

            :exceptions: None.
        '''
        invalid = _InvalidCLI()
        self.assertNotIsInstance(invalid, ICLI)


if __name__ == '__main__':
    unittest_main()
