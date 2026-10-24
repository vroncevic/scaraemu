# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for InfrastructureFactory.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from unittest import TestCase, main as unittest_main

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.emulation.dependencies import EmulationDependencies
from scaraemu.core.service.emulation.factory import EmulationFactory
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.infrastructure.dependencies import InfrastructureDependencies
from scaraemu.infrastructure.factory import InfrastructureFactory
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.provides import InfrastructureProvides
from scaraemu.setup.kinematics.dependencies import KinematicsDependencies
from scaraemu.setup.kinematics.factory import KinematicsFactory
from scaraemu.setup.kinematics.provides import KinematicsProvides
from scaraemu.setup.options import SCARAEmuBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfrastructureFactory(TestCase):
    '''
        Test cases verifying InfrastructureFactory.

        It defines:

            :methods:
                | test_create_infrastructure - Verifies instantiating infrastructure provides.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(InfrastructureFactory.get_version(), '1.0.2')

    def test_create_infrastructure(self) -> None:
        '''
            Verifies instantiating infrastructure provides container.

            :exceptions: None.
        '''
        base_dir: str = dirname(dirname(dirname(abspath(__file__))))
        info_file: str = join(base_dir, 'scaraemu', 'infrastructure', 'config', 'scaraemu.cfg')
        geom_file: str = join(base_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry.json')
        scheme_file: str = join(
            base_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry_scheme.json'
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle,
            )
        )

        options: SCARAEmuBundleOptions = {}
        kinematics_deps = KinematicsDependencies(
            options=options,
            context_bundle=context_bundle,
            geometry_config_file=geom_file,
            geometry_scheme_file=scheme_file,
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
        emulation_provides = EmulationFactory.create(
            dependencies=emulation_deps
        )

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
            initial_script_path='',
        )
        infra_provides: InfrastructureProvides = InfrastructureFactory.create(
            dependencies=infra_deps
        )

        self.assertIsInstance(infra_provides, InfrastructureProvides)
        self.assertTrue(isinstance(infra_provides.gui, IGUI))
        self.assertTrue(isinstance(infra_provides.cli, ICLI))


if __name__ == '__main__':
    unittest_main()
