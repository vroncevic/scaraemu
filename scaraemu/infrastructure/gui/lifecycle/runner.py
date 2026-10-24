# -*- coding: UTF-8 -*-

'''
Module
    runner.py
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
    Executes GUI root window setup, layout building, ticker loop and Tkinter mainloop.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator
from scaraemu.infrastructure.gui.splash.ifactory import ISplashScreenFactory
from scaraemu.infrastructure.gui.splash.iscreen import ISplashScreen
from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
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


class GuiLifecycleRunner:
    '''
        Executes GUI root window setup, layout building, ticker loop and Tkinter mainloop.

        It defines:

            :attributes:
                | _emulation_service - Digital twin simulation engine.
                | _window_configurator - Root window styling and geometry configurator.
                | _splash_factory - Abstract factory providing splash screen instances.
                | _ticker_factory - Abstract factory providing simulation ticker instances.
            :methods:
                | __init__ - Initializes lifecycle runner with collaborators.
                | run_lifecycle - Constructs root window, layouts, starts ticker and mainloop.
                | get_version - Returns lifecycle runner component version string.
    '''

    _emulation_service: IEmulationService
    _window_configurator: IWindowConfigurator
    _splash_factory: ISplashScreenFactory
    _ticker_factory: ISimulationTickerFactory

    def __init__(
        self,
        *,
        emulation_service: IEmulationService,
        window_configurator: IWindowConfigurator,
        splash_factory: ISplashScreenFactory,
        ticker_factory: ISimulationTickerFactory,
    ) -> None:
        '''
            Initializes lifecycle runner with collaborators.

            :param emulation_service: Digital twin simulation engine.
            :param window_configurator: Root window styling and geometry configurator.
            :param splash_factory: Abstract factory providing splash screen instances.
            :param ticker_factory: Abstract factory providing simulation ticker instances.
            :exceptions: None.
        '''
        self._emulation_service: Final[IEmulationService] = emulation_service
        self._window_configurator: Final[IWindowConfigurator] = window_configurator
        self._splash_factory: Final[ISplashScreenFactory] = splash_factory
        self._ticker_factory: Final[ISimulationTickerFactory] = ticker_factory

    def run_lifecycle(
        self,
        *,
        bounds: ScaraBounds,
        delegates: GuiDelegatesBundle,
        layout_builder: ILayoutBuilder,
        target_click_listener: ITargetClickListener,
    ) -> None:
        '''
            Builds and executes the full GUI lifecycle from splash screen to mainloop.

            :param bounds: Mandatory kinematic and physical workspace limits.
            :param delegates: Injected UI action and event delegates bundle.
            :param layout_builder: Injected GUI frame and tab layout builder.
            :param target_click_listener: Listener for interactive canvas clicks.
            :exceptions: None.
        '''
        root: Tk = Tk()
        root.withdraw()
        self._window_configurator.setup_window(root)

        splash: ISplashScreen = self._splash_factory.create(parent=root)
        splash.set_progress(10, 'Initializing SCARA emulator...')
        splash.set_progress(30, 'Configuring styles & themes...')

        splash.set_progress(50, 'Assembling application panels...')
        layout_builder.build_layout(
            root=root,
            bounds=bounds,
            delegates=delegates,
            target_click_listener=target_click_listener,
        )

        splash.set_progress(75, 'Configuring viewports & visualizers...')
        self._window_configurator.maximize_window(root)

        splash.set_progress(90, 'Starting simulation engine & digital twin...')
        ticker_deps: SimulationTickerDependencies = SimulationTickerDependencies(
            root=root,
            emulation_service=self._emulation_service,
            canvas_xy=layout_builder.canvas_xy,
            canvas_z=layout_builder.canvas_z,
            telemetry_view=layout_builder.telemetry_view,
            queue_view=layout_builder.queue_view,
            interval_ms=25,
        )
        ticker: ISimulationTicker = self._ticker_factory.create(
            dependencies=ticker_deps,
        )
        ticker.start()

        splash.set_progress(100, 'Ready')
        splash.close()
        root.deiconify()
        root.mainloop()

    def get_version(self) -> str:
        '''
            Returns lifecycle runner component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
