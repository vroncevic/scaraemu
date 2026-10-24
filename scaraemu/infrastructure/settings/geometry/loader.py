# -*- coding: UTF-8 -*-

'''
Module
    loader.py
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
    Infrastructure configuration loader for robot geometry and kinematics limits.
'''

from __future__ import annotations

from os.path import exists
from typing import Final

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.context.bundle import ContextBundle

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.profile.factory import ProfileFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GeometryLoader:
    '''
        Configuration loader constructing ScaraBounds and LinkDimensions from JSON config.

        It defines:

            :attributes:
                | _context - Shared ATS context bundle.
            :methods:
                | __init__ - Initializes loader with shared context bundle.
                | load_bounds - Loads validated ScaraBounds from JSON configuration.
                | get_version - Returns loader version string.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes loader with shared context bundle.

            :param context_bundle: Shared ATS ContextBundle instance.
            :exceptions: None.
        '''
        self._context: Final[ContextBundle] = context_bundle

    def load_bounds(self, *, config_path: str, scheme_path: str) -> ScaraBounds:
        '''
            Loads validated kinematics bounds and limits from JSON files.

            :param config_path: Path to robot geometry JSON configuration file.
            :param scheme_path: Path to JSON validation scheme file.
            :return: ScaraBounds value object.
            :exceptions: None.
        '''
        if not exists(config_path) or not exists(scheme_path):
            return DefaultScaraProfile.create_bounds()

        try:
            scheme_bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions({
                    ConfigIOBundleKeys.OPTION_FILE_PATH: scheme_path,
                    ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: self._context,
                })
            )
            scheme = Loader(scheme_bundle).load_configuration()

            config_bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions({
                    ConfigIOBundleKeys.OPTION_FILE_PATH: config_path,
                    ConfigIOBundleKeys.OPTION_SCHEME: scheme,
                    ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: self._context,
                })
            )
            config_data: dict[str, object] = Loader(config_bundle).load_configuration()

            return ProfileFactory.create_bounds_from_dict(config_data)

        except Exception:
            return DefaultScaraProfile.create_bounds()

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
