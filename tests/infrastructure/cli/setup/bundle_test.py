# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for CLIBundle.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from scaraemu.infrastructure.cli.setup.bundle import CLIBundle


class TestCLIBundle(TestCase):
    '''
        Test cases verifying CLIBundle dataclass.

        It defines:

            :methods:
                | test_bundle_creation - Verifies dataclass attributes.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies dataclass attributes.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        bundle = CLIBundle(parser=parser, commands=[])
        self.assertEqual(bundle.parser, parser)
        self.assertEqual(bundle.commands, [])


if __name__ == '__main__':
    unittest_main()
