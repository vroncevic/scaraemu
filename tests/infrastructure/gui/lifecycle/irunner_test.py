# -*- coding: UTF-8 -*-

'''
Module
    irunner_test.py
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
    Unit tests for IGuiLifecycleRunner interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from scaraemu.infrastructure.gui.lifecycle.runner import GuiLifecycleRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyRunner:
    '''Dummy runner implementation for protocol testing.'''

    def run_lifecycle(
        self,
        *,
        bounds: ScaraBounds,
        target_click_listener: ITargetClickListener,
        delegates: GuiDelegatesBundle,
        layout_builder: ILayoutBuilder,
    ) -> None:
        '''Executes lifecycle steps.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.2'


class TestIGuiLifecycleRunner(TestCase):
    '''
        Tests verifying IGuiLifecycleRunner protocol definition and subtyping.
    '''

    def test_protocol_methods(self) -> None:
        '''Verifies methods declared on IGuiLifecycleRunner protocol.'''
        self.assertTrue(hasattr(IGuiLifecycleRunner, 'run_lifecycle'))
        self.assertTrue(hasattr(IGuiLifecycleRunner, 'get_version'))

    def test_runner_subtyping(self) -> None:
        '''Verifies structural satisfaction of IGuiLifecycleRunner protocol.'''
        dummy = _DummyRunner()
        self.assertIsInstance(dummy, IGuiLifecycleRunner)

    def test_concrete_runner_satisfies_protocol(self) -> None:
        '''Verifies GuiLifecycleRunner satisfies protocol via structural subtyping.'''
        self.assertTrue(issubclass(GuiLifecycleRunner, IGuiLifecycleRunner))


if __name__ == '__main__':
    main()
