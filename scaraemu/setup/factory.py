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

from os.path import abspath, dirname, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.emulation.provides import EmulationProvides
from scaraemu.infrastructure.dependencies import InfrastructureDependencies
from scaraemu.infrastructure.factory import InfrastructureFactory
from scaraemu.infrastructure.provides import InfrastructureProvides
from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.dependencies import SCARAEmuBundleDependencies
from scaraemu.setup.keys import SCARAEmuBundleKeys
from scaraemu.setup.kinematics.dependencies import KinematicsDependencies
from scaraemu.setup.kinematics.factory import KinematicsFactory
from scaraemu.setup.kinematics.provides import KinematicsProvides
from scaraemu.setup.opt_validator import SCARAEmuBundleOptionsValidator
from scaraemu.setup.options import SCARAEmuBundleOptions
from scaraemu.setup.registry import SCARAEmuBundleRegistry

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
                | create - Creates the scaraemu bundle with explicit pre-configured options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'scaraemu.cfg'
    )
    _geometry_config_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'scara_geometry.json'
    )
    _geometry_scheme_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'scara_geometry_scheme.json'
    )

    @classmethod
    def create(cls, options: SCARAEmuBundleOptions) -> SCARAEmuBundle:
        '''
            Creates the scaraemu bundle with explicit pre-configured options.

            :param options: Pre-configured options for the bundle.
            :return: The scaraemu bundle.
            :exceptions:
                | ATSValueError: The options or dependencies must be valid.
                | ATSTypeError: The options or dependencies must match types.
        '''
        SCARAEmuBundleOptionsValidator.validate(options)

        info_file: str = str(options.get(SCARAEmuBundleKeys.OPTION_INFO_FILE, cls._info_file))
        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle,
            )
        )

        config_path: str = str(
            options.get(SCARAEmuBundleKeys.OPTION_ROBOT_CONFIG, cls._geometry_config_file)
        )
        kinematics_deps = KinematicsDependencies(
            options=options,
            context_bundle=context_bundle,
            geometry_config_file=config_path,
            geometry_scheme_file=cls._geometry_scheme_file,
        )
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=kinematics_deps
        )

        initial_pose: ScaraPose = kinematics_provides.home_pose
        emulation_deps = EmulationDependencies(
            kinematics=kinematics_provides.kinematics,
            initial_pose=initial_pose,
            speed_mm_per_sec=kinematics_provides.bounds.speeds.default_speed,
        )
        emulation_provides: EmulationProvides = EmulationFactory.create(
            dependencies=emulation_deps
        )

        initial_script_path: str = str(options.get(SCARAEmuBundleKeys.OPTION_FILE_PATH, ''))
        infra_deps = InfrastructureDependencies(
            base_bundle=base_bundle,
            context_bundle=context_bundle,
            bounds=kinematics_provides.bounds,
            kinematics=kinematics_provides.kinematics,
            emulation_service=emulation_provides.service,
            emulation_controller=emulation_provides.controller,
            emulation_queue=emulation_provides.queue,
            motion_notifier=emulation_provides.notifier,
            home_pose=initial_pose,
            initial_script_path=initial_script_path,
        )
        infra_provides: InfrastructureProvides = InfrastructureFactory.create(
            dependencies=infra_deps
        )

        return SCARAEmuBundleRegistry.create_bundle(
            dependencies=SCARAEmuBundleDependencies(
                base=base_bundle,
                bounds=kinematics_provides.bounds,
                kinematics=kinematics_provides.kinematics,
                emulation_service=emulation_provides.service,
                gui=infra_provides.gui,
                cli=infra_provides.cli,
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
