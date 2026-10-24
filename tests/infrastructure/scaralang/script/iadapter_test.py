# -*- coding: UTF-8 -*-

'''
Module
    iadapter_test.py
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
    Unit tests for IScriptLoaderAdapter protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.scaralang.script.factory import ScriptLoaderAdapterFactory
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockScriptLoaderAdapter:
    '''
        Mock implementation verifying IScriptLoaderAdapter structural protocol.
    '''

    def load_from_text(self, source: str) -> list[ScaraPose]:
        '''
            Compiles DSL source script text into a sequence of Cartesian poses.
        '''
        return [ScaraPose(x=100.0, y=100.0, z=0.0, phi=0.0)]

    def load_from_file(self, filepath: str) -> list[ScaraPose]:
        '''
            Loads script or trajectory plan file and compiles into Cartesian poses.
        '''
        return [ScaraPose(x=100.0, y=100.0, z=0.0, phi=0.0)]

    def get_version(self) -> str:
        '''
            Returns adapter component version string representation.
        '''
        return '1.0.2'


class _NonConformingScriptLoader:
    '''
        Non-conforming class lacking required script loader methods.
    '''

    def dummy(self) -> None:
        '''
            Non-conforming dummy method.
        '''


class TestScriptLoaderAdapterProtocol(TestCase):
    '''
        Test cases verifying IScriptLoaderAdapter protocol conformance.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies mock satisfies IScriptLoaderAdapter structurally.
        '''
        mock_adapter = _MockScriptLoaderAdapter()
        self.assertIsInstance(mock_adapter, IScriptLoaderAdapter)

    def test_concrete_adapter_conformance(self) -> None:
        '''
            Verifies concrete ScriptLoaderAdapter satisfies IScriptLoaderAdapter structurally.
        '''
        adapter: IScriptLoaderAdapter = ScriptLoaderAdapterFactory.create()
        self.assertIsInstance(adapter, IScriptLoaderAdapter)

    def test_non_conforming_fails(self) -> None:
        '''
            Verifies invalid object fails IScriptLoaderAdapter protocol check.
        '''
        invalid = _NonConformingScriptLoader()
        self.assertNotIsInstance(invalid, IScriptLoaderAdapter)


if __name__ == '__main__':
    unittest_main()
