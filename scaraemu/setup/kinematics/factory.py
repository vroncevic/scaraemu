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
    Factory for loading robot kinematics parameters and instantiating service.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.envelope.home import HomePoseCalculator
from scaralang.core.service.kinematics.envelope.home_factory import HomePoseCalculatorFactory

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.scaralang.kinematics.solver.factory import KinematicsAdapterFactory
from scaraemu.infrastructure.settings.dependencies import SettingsDependencies
from scaraemu.infrastructure.settings.factory import SettingsFactory
from scaraemu.infrastructure.settings.provides import SettingsProvides
from scaraemu.setup.keys import SCARAEmuBundleKeys
from scaraemu.setup.kinematics.dependencies import KinematicsDependencies
from scaraemu.setup.kinematics.provides import KinematicsProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsFactory:
    '''
        Factory for loading robot kinematics parameters and instantiating service.

        It defines:

            :methods:
                | create - Loads bounds and transmission and builds kinematics adapter.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: KinematicsDependencies) -> KinematicsProvides:
        '''
            Loads bounds and transmission and builds kinematics adapter.

            :param dependencies: Encapsulated options, context, and file paths.
            :return: The assembled kinematics provides container.
            :exceptions:
                | ATSValueError: When validation of geometry or scheme fails.
                | ATSTypeError: When configuration values do not match expected types.
        '''
        settings: SettingsProvides = SettingsFactory.create(
            dependencies=SettingsDependencies(
                context_bundle=dependencies.context_bundle
            )
        )

        raw_bounds: ScaraBounds = settings.geometry_loader.load_bounds(
            config_path=dependencies.geometry_config_file,
            scheme_path=dependencies.geometry_scheme_file,
        )
        transmission: TransmissionParameters = (
            settings.transmission_loader.load_transmission(
                config_path=dependencies.geometry_config_file,
                scheme_path=dependencies.geometry_scheme_file,
            )
        )

        l1: float = float(
            dependencies.options.get(SCARAEmuBundleKeys.OPTION_L1, raw_bounds.links.l1)
        )
        l2: float = float(
            dependencies.options.get(SCARAEmuBundleKeys.OPTION_L2, raw_bounds.links.l2)
        )
        z_min: float = float(
            dependencies.options.get(SCARAEmuBundleKeys.OPTION_Z_MIN, raw_bounds.vertical.z_min)
        )
        z_max: float = float(
            dependencies.options.get(SCARAEmuBundleKeys.OPTION_Z_MAX, raw_bounds.vertical.z_max)
        )
        min_speed: float = float(
            dependencies.options.get(
                SCARAEmuBundleKeys.OPTION_MIN_SPEED, raw_bounds.speeds.min_speed
            )
        )
        max_speed: float = float(
            dependencies.options.get(
                SCARAEmuBundleKeys.OPTION_MAX_SPEED, raw_bounds.speeds.max_speed
            )
        )

        bounds = ScaraBounds(
            links=LinkDimensions(l1=l1, l2=l2),
            vertical=VerticalBounds(z_min=z_min, z_max=z_max),
            speeds=SpeedLimits(
                min_speed=min_speed,
                max_speed=max_speed,
                default_speed=raw_bounds.speeds.default_speed,
                default_accel=raw_bounds.speeds.default_accel,
                max_accel=raw_bounds.speeds.max_accel,
            ),
            joints=raw_bounds.joints,
            singularity=raw_bounds.singularity,
        )

        home_calc: HomePoseCalculator = HomePoseCalculatorFactory.create(bounds=bounds)
        home_cartesian: CartesianPose = home_calc.calculate_home_pose()
        home_pose: ScaraPose = ScaraPose(
            x=home_cartesian.x,
            y=home_cartesian.y,
            z=home_cartesian.z,
            phi=home_cartesian.phi,
        )

        kinematics: IManipulatorKinematics = KinematicsAdapterFactory.create(
            bounds=bounds,
            transmission=transmission,
        )

        return KinematicsProvides(
            bounds=bounds,
            kinematics=kinematics,
            home_pose=home_pose,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
