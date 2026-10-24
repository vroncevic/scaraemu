# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Top-level GUI orchestration engine for SCARA robot emulator.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.server.manager.imanager import IVirtualServerManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraEmuGUI:
    '''
        Top-level GUI orchestration engine for SCARA robot emulator.

        It defines:

            :attributes:
                | _bounds - Manipulator kinematic boundaries and link lengths.
                | _target_click_listener - Injected canvas target click listener.
                | _delegates - Injected GUI action delegates bundle.
                | _server_manager - Virtual robot TCP server lifecycle manager.
                | _startup_config - Startup configuration parameters.
                | _layout_builder - UI widget layout builder.
                | _lifecycle_runner - GUI execution lifecycle runner.
            :methods:
                | __init__ - Initializes GUI engine with injected collaborators.
                | is_initialized - Returns initialization status.
                | load_file - Sets initial plan or DSL script to load upon GUI startup.
                | run - Triggers window and simulation execution lifecycle.
                | get_version - Returns GUI engine version string.
    '''

    _bounds: ScaraBounds
    _target_click_listener: ITargetClickListener
    _delegates: GuiDelegatesBundle
    _server_manager: IVirtualServerManager
    _initial_script: str
    _layout_builder: ILayoutBuilder
    _lifecycle_runner: IGuiLifecycleRunner

    def __init__(
        self,
        *,
        bounds: ScaraBounds,
        target_click_listener: ITargetClickListener,
        delegates: GuiDelegatesBundle,
        server_manager: IVirtualServerManager,
        layout_builder: ILayoutBuilder,
        lifecycle_runner: IGuiLifecycleRunner,
        initial_script: str = '',
    ) -> None:
        '''
            Initializes GUI engine with injected services, delegates, and builder.

            :param bounds: Manipulator kinematic boundaries and link lengths.
            :param target_click_listener: Injected canvas click listener.
            :param delegates: Injected GUI action delegates bundle.
            :param server_manager: Virtual robot TCP server manager.
            :param layout_builder: UI widget layout builder.
            :param lifecycle_runner: GUI execution lifecycle runner.
            :param initial_script: Optional initial script path to execute.
            :exceptions: None.
        '''
        self._bounds: Final[ScaraBounds] = bounds
        self._target_click_listener: Final[ITargetClickListener] = target_click_listener
        self._delegates: Final[GuiDelegatesBundle] = delegates
        self._server_manager: Final[IVirtualServerManager] = server_manager
        self._initial_script: Final[str] = initial_script
        self._layout_builder: Final[ILayoutBuilder] = layout_builder
        self._lifecycle_runner: Final[IGuiLifecycleRunner] = lifecycle_runner

    def is_initialized(self) -> bool:
        '''
            Returns initialization status.

            :return: True if GUI is initialized, False otherwise.
            :exceptions: None.
        '''
        return bool(
            self._bounds
            and self._delegates.preset
            and self._delegates.script
            and self._layout_builder
        )

    def load_file(self, file_path: str) -> None:
        '''
            Sets initial plan or DSL script to load upon GUI startup.

            :param file_path: Path to script or plan file.
            :exceptions: None.
        '''
        self._delegates.script.handle_load_script(file_path)

    def run(self) -> None:
        '''
            Constructs Tkinter widgets, layouts, and starts event loop.

            :exceptions: None.
        '''
        if self._initial_script:
            self._delegates.script.handle_load_script(self._initial_script)

        self._lifecycle_runner.run_lifecycle(
            bounds=self._bounds,
            target_click_listener=self._target_click_listener,
            delegates=self._delegates,
            layout_builder=self._layout_builder,
        )

    def get_version(self) -> str:
        '''
            Returns GUI engine component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
