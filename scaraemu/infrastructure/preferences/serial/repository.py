# -*- coding: UTF-8 -*-

'''
Module
    repository.py
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
from typing import Final

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.utils.reflection import to_str

from scaracom.transport.preference.preference import SerialPreference

from scaraemu.infrastructure.preferences.exceptions.preference_not_found_error import PreferenceNotFoundError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPreferenceRepository:
    '''
        Repository managing file-based persistence for serial connection preferences using ats_utilities.

        It defines:

            :attributes:
                | _config_file - Path to configuration storage file.
                | _context - ATS context bundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes repository with storage path and context bundle.
                | has_preference - Checks if valid stored preferences exist.
                | load_preference - Reads previously saved port and baud rate using ATS Loader.
                | save_preference - Persists active port and baud rate to storage using ATS Storer.
                | get_version - Returns repository component version string.
                | __str__ - Returns repository instance as string representation.
    '''

    def __init__(
        self,
        config_file: Path,
        context_bundle: ContextBundle
    ) -> None:
        '''
            Initializes repository with required storage path and context bundle.

            :param config_file: File path to configuration JSON.
            :param context_bundle: ATS ContextBundle instance.
            :exceptions: None.
        '''
        self._config_file: Final[Path] = config_file.resolve()
        self._context: Final[ContextBundle] = context_bundle

    def has_preference(self) -> bool:
        '''
            Checks if valid stored connection preferences exist.

            :return: True if preference file exists and is valid, False otherwise.
            :exceptions: None.
        '''
        if not self._config_file.is_file():
            return False

        try:
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context
                )
            )
            loader = Loader(bundle)
            payload: dict[str, object] = loader.load_configuration()

            return 'port' in payload and 'baud' in payload

        except Exception:
            return False

    def load_preference(self) -> SerialPreference:
        '''
            Reads previously saved serial port and baud rate using ATS Loader.

            :return: SerialPreference value object.
            :exceptions: PreferenceNotFoundError.
        '''
        if not self._config_file.is_file():
            raise PreferenceNotFoundError(
                f"Configuration file not found: {self._config_file}"
            )

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

            if raw_port is None or raw_baud is None:
                raise PreferenceNotFoundError(
                    f"Incomplete preferences in: {self._config_file}"
                )

            return SerialPreference(port=str(raw_port), baud=int(raw_baud))

        except PreferenceNotFoundError:
            raise
        except Exception as exc:
            raise PreferenceNotFoundError(
                f"Failed to load preferences from {self._config_file}"
            ) from exc

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Persists active port and baud rate to storage using ATS Storer.

            :param preference: SerialPreference value object.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
        if not preference.port or preference.port == 'Virtual / None':
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
            storer.store_configuration(
                {'port': preference.port, 'baud': str(preference.baud)}
            )
            return True

        except Exception:
            return False

    def get_version(self) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__

    def __str__(self) -> str:
        '''
            Returns the SerialPreferenceRepository instance as string representation.

            :return: The SerialPreferenceRepository instance as string representation.
            :exceptions: None.
        '''
        return to_str(self)
