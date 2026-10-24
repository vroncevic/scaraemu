# -*- coding: UTF-8 -*-

'''
Module
    runner_test.py
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
    Unit tests for GuiLifecycleRunner component.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator
from scaraemu.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from scaraemu.infrastructure.gui.lifecycle.runner import GuiLifecycleRunner
from scaraemu.infrastructure.gui.splash.ifactory import ISplashScreenFactory
from scaraemu.infrastructure.gui.splash.iscreen import ISplashScreen
from scaraemu.infrastructure.gui.ticker.ifactory import ISimulationTickerFactory
from scaraemu.infrastructure.gui.ticker.iticker import ISimulationTicker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLifecycleRunnerTestCase(TestCase):
    '''
        Unit tests for GuiLifecycleRunner.

        It defines:

            :methods:
                | setUp - Prepares mock collaborators and runner instance.
                | test_structural_typing - Verifies conformance to IGuiLifecycleRunner protocol.
                | test_get_version - Verifies version string retrieval.
                | test_run_lifecycle - Verifies window setup and lifecycle orchestration.
    '''

    _emulation_service: MagicMock
    _window_configurator: MagicMock
    _splash_factory: MagicMock
    _ticker_factory: MagicMock
    _runner: GuiLifecycleRunner

    def setUp(self) -> None:
        '''
            Prepares mock collaborators and runner instance.

            :exceptions: None.
        '''
        self._emulation_service = MagicMock(spec=IEmulationService)
        self._window_configurator = MagicMock(spec=IWindowConfigurator)
        self._splash_factory = MagicMock(spec=ISplashScreenFactory)
        self._ticker_factory = MagicMock(spec=ISimulationTickerFactory)
        self._runner = GuiLifecycleRunner(
            emulation_service=self._emulation_service,
            window_configurator=self._window_configurator,
            splash_factory=self._splash_factory,
            ticker_factory=self._ticker_factory,
        )

    def test_structural_typing(self) -> None:
        '''
            Verifies conformance to IGuiLifecycleRunner protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self._runner, IGuiLifecycleRunner)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self._runner.get_version(), '1.0.2')

    @patch('scaraemu.infrastructure.gui.lifecycle.runner.Tk')
    def test_run_lifecycle(
        self,
        mock_tk_cls: MagicMock,
    ) -> None:
        '''
            Verifies window setup and lifecycle orchestration.

            :param mock_tk_cls: Input mock_tk_cls.
            :exceptions: None.
        '''
        mock_root = MagicMock()
        mock_tk_cls.return_value = mock_root
        mock_ticker = MagicMock(spec=ISimulationTicker)
        self._ticker_factory.create.return_value = mock_ticker
        mock_splash = MagicMock(spec=ISplashScreen)
        self._splash_factory.create.return_value = mock_splash

        bounds = MagicMock(spec=ScaraBounds)

        mock_delegates = MagicMock(spec=GuiDelegatesBundle)
        mock_layout_builder = MagicMock(spec=ILayoutBuilder)
        mock_layout_builder.canvas_xy = MagicMock()
        mock_layout_builder.canvas_z = MagicMock()
        mock_layout_builder.telemetry_view = MagicMock()
        mock_layout_builder.queue_view = MagicMock()
        mock_target_listener = MagicMock(spec=ITargetClickListener)

        self._runner.run_lifecycle(
            bounds=bounds,
            delegates=mock_delegates,
            layout_builder=mock_layout_builder,
            target_click_listener=mock_target_listener,
        )

        mock_tk_cls.assert_called_once()
        mock_root.withdraw.assert_called_once()
        self._window_configurator.setup_window.assert_called_once_with(mock_root)
        self._splash_factory.create.assert_called_once_with(parent=mock_root)

        mock_layout_builder.build_layout.assert_called_once_with(
            root=mock_root,
            bounds=bounds,
            delegates=mock_delegates,
            target_click_listener=mock_target_listener,
        )

        self._window_configurator.maximize_window.assert_called_once_with(mock_root)
        self._ticker_factory.create.assert_called_once()
        mock_ticker.start.assert_called_once()
        mock_splash.close.assert_called_once()
        mock_root.deiconify.assert_called_once()
        mock_root.mainloop.assert_called_once()


if __name__ == '__main__':
    unittest_main()
