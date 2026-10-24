# -*- coding: UTF-8 -*-

'''
Module
    discovery.py
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
    Utility class for discovering bundled SCARA DSL example scripts.
'''

from __future__ import annotations

from pathlib import Path

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptExampleDiscovery:
    '''
        Discovers bundled SCARA DSL example scripts from search directories.

        It defines:

            :methods:
                | discover_examples - Discovers example scripts and returns mapping.
                | get_version - Returns discovery component version string.
    '''

    @classmethod
    def discover_examples(cls) -> dict[str, str]:
        '''
            Discovers example scripts and returns mapping from name to filepath.

            :return: Dictionary mapping script filenames to paths.
            :exceptions: None.
        '''
        search_dirs: list[Path] = [
            Path.cwd() / 'examples',
            Path.home() / '.scara' / 'examples',
        ]

        current_file: Path = Path(__file__).resolve()

        for parent_dir in current_file.parents:
            candidate_dir: Path = (
                parent_dir / 'scarajectory' / 'github' / 'scarajectory' / 'examples'
            )

            if candidate_dir.is_dir():
                search_dirs.append(candidate_dir)
                break

        script_paths: dict[str, str] = {}

        for directory in search_dirs:
            if directory.is_dir():
                for script_file in sorted(directory.glob('*.scara')):
                    script_paths[script_file.name] = str(script_file)

                if script_paths:
                    break

        return script_paths

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns discovery component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
