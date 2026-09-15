# -*- coding: UTF-8 -*-

'''
Module
    connection_preferences_repository.py
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
    Infrastructure repository persisting and retrieving serial connection preferences using ats_utilities.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionPreferencesRepository:
    '''
        Repository managing file-based persistence for connection preferences using ats_utilities.

        It defines:

            :attributes:
                | DEFAULT_CONFIG_FILE - Default file path for storing connection preferences.
                | _config_file - Path to configuration storage file.
                | _context - ATS context bundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes repository with optional custom storage path and context bundle.
                | load_preference - Reads previously saved port and baud rate using ATS Loader.
                | save_preference - Persists active port and baud rate to storage using ATS Storer.
                | __str__ - Returns repository instance as string representation.
    '''

    DEFAULT_CONFIG_FILE: ClassVar[Path] = Path.home() / '.config' / 'scara' / 'serial_device.json'
    _config_file: Path
    _context: ContextBundle

    def __init__(
        self,
        config_file: Path | str | None = None,
        context_bundle: ContextBundle | None = None
    ) -> None:
        '''
            Initializes repository with optional custom storage path and context bundle.

            :param config_file: Optional file path to configuration JSON.
            :param context_bundle: Optional ATS ContextBundle instance.
            :exceptions: None.
        '''
        if config_file is not None:
            self._config_file = Path(config_file).resolve()
        else:
            self._config_file = self.DEFAULT_CONFIG_FILE

        self._context = context_bundle or ContextBundleFactory.create_bundle()

    def load_preference(self) -> tuple[str | None, int | None]:
        '''
            Reads previously saved serial port and baud rate using ATS Loader.

            :return: Tuple of (port, baud) or (None, None) if not found.
            :exceptions: None.
        '''
        if not self._config_file.is_file():
            return None, None

        try:
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context
                )
            )
            loader = Loader(bundle)
            payload: dict[str, object] = loader.load_configuration()
            raw_port = payload.get('port')
            raw_baud = payload.get('baud')
            port: str | None = str(raw_port) if raw_port is not None else None
            baud: int | None = int(raw_baud) if raw_baud is not None else None

            return port, baud

        except Exception:
            return None, None

    def save_preference(self, port: str, baud: int = 115200) -> bool:
        '''
            Persists active port and baud rate to storage using ATS Storer.

            :param port: Serial port identifier (e.g. '/dev/ttyACM0').
            :param baud: Communication baud rate integer.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
        if not port or port == 'Virtual / None':
            return False

        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.touch(exist_ok=True)
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context
                )
            )
            storer = Storer(bundle)
            storer.store_configuration({'port': port, 'baud': str(baud)})
            return True

        except Exception:
            return False

    def __str__(self) -> str:
        '''
            Returns the ConnectionPreferencesRepository instance as string representation.

            :return: The ConnectionPreferencesRepository instance as string representation.
            :exceptions: None.
        '''
        return to_str(self)
