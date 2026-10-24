# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating script parsing and trajectory plan compilation to scaralang.
'''

from __future__ import annotations

from json import loads as json_loads
from pathlib import Path
from typing import Final

from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptLoaderAdapter:
    '''
        Adapter implementing domain script loader port via scaralang plan compiler.

        It defines:

            :attributes:
                | _compiler - Injected scaralang plan compiler service.
            :methods:
                | __init__ - Initializes adapter with injected scaralang plan compiler.
                | load_from_text - Compiles DSL text into Cartesian poses.
                | load_from_file - Reads file and parses into Cartesian poses.
                | get_version - Returns adapter version string.
    '''

    _compiler: IScriptPlanCompiler

    def __init__(self, *, compiler: IScriptPlanCompiler) -> None:
        '''
            Initializes the script loader adapter with injected scaralang compiler.

            :param compiler: Injected IScriptPlanCompiler plan compilation service.
            :exceptions: None.
        '''
        self._compiler: Final[IScriptPlanCompiler] = compiler

    def load_from_text(self, source: str) -> list[ScaraPose]:
        '''
            Compiles DSL source script text into a sequence of Cartesian poses.

            :param source: Raw script text content.
            :return: List of Cartesian poses for trajectory execution.
            :exceptions: None.
        '''
        plan: ITrajectoryPlan = self._compiler.compile_script(source=source)

        return [
            ScaraPose(x=wp.x, y=wp.y, z=wp.z, phi=wp.phi)
            for wp in plan.waypoints
        ]

    def load_from_file(self, filepath: str) -> list[ScaraPose]:
        '''
            Loads script or trajectory plan file and compiles into Cartesian poses.

            :param filepath: Path to .scara or JSON trajectory plan file.
            :return: List of Cartesian poses for trajectory execution.
            :exceptions: None.
        '''
        path = Path(filepath)

        if not path.is_file():
            return []

        text_content = path.read_text(encoding='utf-8')

        if path.suffix.lower() == '.json':
            raw_data: object = json_loads(text_content)
            waypoints_data: list[dict[str, object]] = (
                raw_data.get('waypoints', []) if isinstance(raw_data, dict)
                else raw_data if isinstance(raw_data, list)
                else []
            )

            return [
                ScaraPose(
                    x=float(item.get('x', 0.0)),
                    y=float(item.get('y', 0.0)),
                    z=float(item.get('z', 0.0)),
                    phi=float(item.get('phi', 0.0)),
                )
                for item in waypoints_data
                if isinstance(item, dict)
            ]

        return self.load_from_text(text_content)

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
