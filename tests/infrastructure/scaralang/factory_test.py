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
    Unit tests for ScaralangFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaraemu.infrastructure.scaralang.bypass.iadapter import IDeadZoneBypassAdapter
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter
from scaraemu.infrastructure.scaralang.dependencies import ScaralangDependencies
from scaraemu.infrastructure.scaralang.factory import ScaralangFactory
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.scaralang.protocol.payload.iadapter import IBinaryPayloadDecoderAdapter
from scaraemu.infrastructure.scaralang.protocol.response.iadapter import IBinaryResponseDecoderAdapter
from scaraemu.infrastructure.scaralang.provides import ScaralangProvides
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter
from scaraemu.infrastructure.scaralang.safety.iadapter import IMotionValidatorAdapter
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangFactory(TestCase):
    '''
        Validates ScaralangFactory assembly and versioning.

        It defines:

            :methods:
                | test_create - Verifies creation of ScaralangProvides with all adapters.
                | test_get_version - Verifies factory version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates ScaralangProvides with all adapters correctly wired.

            :exceptions: None.
        '''
        bounds = ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=120.0),
            vertical=VerticalBounds(z_min=0.0, z_max=100.0),
            speeds=SpeedLimits(
                min_speed=1.0, max_speed=200.0, default_speed=50.0,
                default_accel=100.0, max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.6, j1_max_rad=2.6,
                j2_min_rad=-2.5, j2_max_rad=2.5,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=3.0,
                singularity_inner_margin_mm=3.0,
                singularity_theta2_min_rad=0.08,
                deadzone_r_min=20.0,
            ),
        )
        deps = ScaralangDependencies(bounds=bounds)
        provides = ScaralangFactory.create(dependencies=deps)

        self.assertIsInstance(provides, ScaralangProvides)
        self.assertIsInstance(provides.bypass, IDeadZoneBypassAdapter)
        self.assertIsInstance(provides.demo, ITrajectoryDemoAdapter)
        self.assertIsInstance(provides.linkage, ILinkageAdapter)
        self.assertIsInstance(provides.reach, IWorkspaceReachAdapter)
        self.assertIsInstance(provides.safety, IMotionValidatorAdapter)
        self.assertIsInstance(provides.script, IScriptLoaderAdapter)
        self.assertIsInstance(provides.boundary, IWorkspaceBoundaryService)

        self.assertIsInstance(provides.codec, IBinaryFrameCodecAdapter)
        self.assertIsInstance(provides.payload_decoder, IBinaryPayloadDecoderAdapter)
        self.assertIsInstance(provides.response_builder, IBinaryResponseBuilderAdapter)
        self.assertIsInstance(provides.response_decoder, IBinaryResponseDecoderAdapter)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(ScaralangFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
