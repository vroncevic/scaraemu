# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating GuiLifecycleRunner instances.
'''

from __future__ import annotations

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.gui.window.iconfigurator import IWindowConfigurator
from scaraemu.infrastructure.gui.lifecycle.runner import GuiLifecycleRunner
from scaraemu.infrastructure.gui.splash.factory import SplashScreenFactory
from scaraemu.infrastructure.gui.ticker.factory import SimulationTickerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLifecycleRunnerFactory:
    '''
        Factory providing configured GuiLifecycleRunner instances.

        It defines:

            :methods:
                | create - Returns a new GuiLifecycleRunner instance with injected configurator.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        emulation_service: IEmulationService,
        window_configurator: IWindowConfigurator,
    ) -> GuiLifecycleRunner:
        '''
            Builds and returns a GuiLifecycleRunner instance.

            :param emulation_service: Injected IEmulationService instance.
            :param window_configurator: Injected IWindowConfigurator instance.
            :return: GuiLifecycleRunner instance.
            :exceptions: None.
        '''
        return GuiLifecycleRunner(
            emulation_service=emulation_service,
            window_configurator=window_configurator,
            splash_factory=SplashScreenFactory,
            ticker_factory=SimulationTickerFactory,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
