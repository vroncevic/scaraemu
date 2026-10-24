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
    Unit tests for KinematicsFactory.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from unittest import TestCase, main as unittest_main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
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


class TestKinematicsFactory(TestCase):
    '''
        Test cases verifying KinematicsFactory.

        It defines:

            :methods:
                | test_create_kinematics_provides - Verifies creating kinematics provides with overrides.
                | test_get_version - Verifies version retrieval.
    '''

    def test_get_version(self) -> None:
        '''
            Verifies version retrieval.

            :exceptions: None.
        '''
        self.assertEqual(KinematicsFactory.get_version(), '1.0.2')

    def test_create_kinematics_provides(self) -> None:
        '''
            Verifies creating kinematics provides with overrides.

            :exceptions: None.
        '''
        base_dir: str = dirname(dirname(dirname(dirname(abspath(__file__)))))
        geom_file: str = join(base_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry.json')
        scheme_file: str = join(
            base_dir, 'scaraemu', 'infrastructure', 'config', 'scara_geometry_scheme.json'
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()
        options: SCARAEmuBundleOptions = {'l1': 160.0, 'l2': 110.0}

        deps = KinematicsDependencies(
            options=options,
            context_bundle=context_bundle,
            geometry_config_file=geom_file,
            geometry_scheme_file=scheme_file,
        )
        provides: KinematicsProvides = KinematicsFactory.create(dependencies=deps)

        self.assertIsInstance(provides, KinematicsProvides)
        self.assertEqual(provides.bounds.links.l1, 160.0)
        self.assertEqual(provides.bounds.links.l2, 110.0)
        self.assertTrue(isinstance(provides.kinematics, IManipulatorKinematics))
        self.assertIsInstance(provides.home_pose, ScaraPose)
        self.assertAlmostEqual(provides.home_pose.x, (160.0 + 110.0) * 0.65)
        self.assertAlmostEqual(provides.home_pose.y, 0.0)
        self.assertAlmostEqual(provides.home_pose.z, provides.bounds.vertical.z_min + 20.0)
        self.assertAlmostEqual(provides.home_pose.phi, 0.0)


if __name__ == '__main__':
    unittest_main()
