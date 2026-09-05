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
    Factory for creating the scaraemu bundle.
'''

from __future__ import annotations

from os.path import exists
from typing import Any

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys

from scaraemu.core.model.scara_geometry import ScaraGeometry
from scaraemu.core.service.kinematics_service import KinematicsService
from scaraemu.core.service.emulator_service import EmulatorService
from scaraemu.core.service.engine import Service
from scaraemu.infrastructure.communication.transport.serial_transport import SerialTransport
from scaraemu.infrastructure.gui.engine import ScaraEmuGUI
from scaraemu.infrastructure.cli.engine import CLI
from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.infrastructure.cli.setup.options import CLIBundleOptions
from scaraemu.infrastructure.cli.setup.factory import CLIBundleFactory
from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.options import SCARAEmuBundleOptions
from scaraemu.setup.registry import SCARAEmuBundleRegistry
from scaraemu.setup.dependencies import SCARAEmuBundleDependencies
from scaraemu.setup.opt_validator import SCARAEmuBundleOptionsValidator
from scaraemu.setup.keys import SCARAEmuBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAEmuBundleFactory:
    '''
        Factory for creating the scaraemu bundle.

        It defines:

            :attributes:
                | _info_file - Path to the scaraemu info file.
                | _geometry_config_file - Path to default robot geometry config file.
                | _geometry_scheme_file - Path to robot geometry validation scheme.
            :methods:
                | _resolve_geometry - Resolves and constructs ScaraGeometry from JSON config and options.
                | create_bundle - Creates the scaraemu bundle with optional pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = 'scaraemu/infrastructure/config/scaraemu.cfg'
    _geometry_config_file: str = 'scaraemu/infrastructure/config/scara_geometry.json'
    _geometry_scheme_file: str = 'scaraemu/infrastructure/config/scheme.json'

    @classmethod
    def _resolve_geometry(cls, options: SCARAEmuBundleOptions | None = None) -> ScaraGeometry:
        '''
            Resolves and constructs ScaraGeometry from JSON configuration and options.

            :param options: Optional bundle configuration options.
            :return: ScaraGeometry domain model.
            :exceptions: None.
        '''
        config_path: str = cls._geometry_config_file
        if options and SCARAEmuBundleKeys.OPTION_ROBOT_CONFIG in options:
            config_path = str(options[SCARAEmuBundleKeys.OPTION_ROBOT_CONFIG])

        config_data: dict[str, Any] = {}

        if exists(config_path) and exists(cls._geometry_scheme_file):
            try:
                context: ContextBundle = ContextBundleFactory.create_bundle()
                scheme_bundle = ConfigIOBundleFactory.create_bundle(
                    ConfigIOBundleOptions({
                        ConfigIOBundleKeys.OPTION_FILE_PATH: cls._geometry_scheme_file,
                        ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context
                    })
                )
                scheme = Loader(scheme_bundle).load_configuration()

                config_bundle = ConfigIOBundleFactory.create_bundle(
                    ConfigIOBundleOptions({
                        ConfigIOBundleKeys.OPTION_FILE_PATH: config_path,
                        ConfigIOBundleKeys.OPTION_SCHEME: scheme,
                        ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context
                    })
                )
                config_data = Loader(config_bundle).load_configuration()

            except Exception:
                config_data = {}

        l1: float = (
            float(options[SCARAEmuBundleKeys.OPTION_L1])
            if options and SCARAEmuBundleKeys.OPTION_L1 in options
            else float(config_data.get('l1', 150.0))
        )
        l2: float = (
            float(options[SCARAEmuBundleKeys.OPTION_L2])
            if options and SCARAEmuBundleKeys.OPTION_L2 in options
            else float(config_data.get('l2', 120.0))
        )
        z_min: float = (
            float(options[SCARAEmuBundleKeys.OPTION_Z_MIN])
            if options and SCARAEmuBundleKeys.OPTION_Z_MIN in options
            else float(config_data.get('z_min', 0.0))
        )
        z_max: float = (
            float(options[SCARAEmuBundleKeys.OPTION_Z_MAX])
            if options and SCARAEmuBundleKeys.OPTION_Z_MAX in options
            else float(config_data.get('z_max', 100.0))
        )
        min_speed: float = (
            float(options[SCARAEmuBundleKeys.OPTION_MIN_SPEED])
            if options and SCARAEmuBundleKeys.OPTION_MIN_SPEED in options
            else float(config_data.get('min_speed', 1.0))
        )
        max_speed: float = (
            float(options[SCARAEmuBundleKeys.OPTION_MAX_SPEED])
            if options and SCARAEmuBundleKeys.OPTION_MAX_SPEED in options
            else float(config_data.get('max_speed', 100.0))
        )

        j1_min_rad: float = float(config_data.get('j1_min_rad', -2.617994))
        j1_max_rad: float = float(config_data.get('j1_max_rad', 2.617994))
        j2_min_rad: float = float(config_data.get('j2_min_rad', -2.530727))
        j2_max_rad: float = float(config_data.get('j2_max_rad', 2.530727))
        singularity_outer_margin_mm: float = float(
            config_data.get('singularity_outer_margin_mm', 3.0)
        )
        singularity_inner_margin_mm: float = float(
            config_data.get('singularity_inner_margin_mm', 3.0)
        )
        singularity_theta2_min_rad: float = float(
            config_data.get('singularity_theta2_min_rad', 0.087266)
        )

        return ScaraGeometry(
            l1=l1,
            l2=l2,
            z_min=z_min,
            z_max=z_max,
            min_speed=min_speed,
            max_speed=max_speed,
            j1_min_rad=j1_min_rad,
            j1_max_rad=j1_max_rad,
            j2_min_rad=j2_min_rad,
            j2_max_rad=j2_max_rad,
            singularity_outer_margin_mm=singularity_outer_margin_mm,
            singularity_inner_margin_mm=singularity_inner_margin_mm,
            singularity_theta2_min_rad=singularity_theta2_min_rad
        )

    @classmethod
    def create_bundle(cls, options: SCARAEmuBundleOptions | None = None) -> SCARAEmuBundle:
        '''
            Creates the scaraemu bundle with optional pre-configured options.

            :param options: Optional pre-configured options for the bundle.
            :return: The scaraemu bundle.
            :exceptions:
                | ATSValueError: The options or dependencies must be valid.
                | ATSTypeError: The options or dependencies must match types.
        '''
        if options is not None:
            SCARAEmuBundleOptionsValidator.validate(options)

        info_file: str = (
            options[SCARAEmuBundleKeys.OPTION_INFO_FILE]
            if options and SCARAEmuBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        geometry: ScaraGeometry = cls._resolve_geometry(options=options)
        kinematics: KinematicsService = KinematicsService(geometry=geometry)
        emulator: EmulatorService = EmulatorService(kinematics=kinematics)
        service: Service = Service(kinematics=kinematics, emulator=emulator)
        transport: SerialTransport = SerialTransport()
        gui: ScaraEmuGUI = ScaraEmuGUI(
            service=service,
            transport=transport,
            initial_script=options.get('file_path') if options else None
        )

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(
                service=service,
                parser=base_bundle.option_manager,
                gui=gui
            )
        )

        cli: CLI = CLI(cli_bundle)

        return SCARAEmuBundleRegistry.create_bundle(
            dependencies=SCARAEmuBundleDependencies(
                base=base_bundle,
                service=service,
                gui=gui,
                transport=transport,
                cli=cli
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version.

            :return: The factory version string.
            :exceptions: None.
        '''
        return __version__
