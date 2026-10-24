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
    Unit test for GuiFactory.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaracom.transport.preference.preference import SerialPreference

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.kinematics.step_coords import ScaraStepCoords
from scaraemu.infrastructure.gui.dependencies import GuiDependencies
from scaraemu.infrastructure.gui.engine import ScaraEmuGUI
from scaraemu.infrastructure.gui.factory import GuiFactory
from scaraemu.infrastructure.gui.provides import GuiProvides
from scaraemu.infrastructure.gui.services import GuiServicesBundle
from scaraemu.infrastructure.server.logger.holder import ServerLogListenerHolder


class MockTransport:
    '''
        Mock implementation of ITransport protocol.

        It defines:

            :methods:
                | __init__ - Initializes mock transport.
                | is_connected - Tests is connected.
                | connect - Tests connect.
                | disconnect - Tests disconnect.
                | read_bytes - Tests read bytes.
                | write_bytes - Tests write bytes.
    '''

    def __init__(self) -> None:
        '''
            Initializes mock transport.
        '''
        self.connected: bool = True
        self.written: list[bytes] = []

    def is_connected(self) -> bool:
        '''
            Tests is connected.
        '''
        return self.connected

    def connect(self, port: str, baudrate: int) -> bool:
        '''
            Tests connect.

            :param port: Input port.
            :param baudrate: Input baudrate.
        '''
        _ = (port, baudrate)
        self.connected = True
        return True

    def disconnect(self) -> None:
        '''
            Tests disconnect.
        '''
        self.connected = False

    def read_bytes(self, size: int = 1024) -> bytes:
        '''
            Tests read bytes.

            :param size: Number of bytes to read.
        '''
        _ = size
        return b''

    def write_bytes(self, data: bytes) -> bool:
        '''
            Tests write bytes.

            :param data: Data to write.
        '''
        self.written.append(data)
        return True


class MockKinematics:
    '''
        Mock implementation of IManipulatorKinematics protocol.

        It defines:

            :methods:
                | solve_fk - Tests solve fk.
                | solve_ik - Tests solve ik.
                | steps_to_joints - Tests steps to joints.
                | joints_to_steps - Tests joints to steps.
    '''

    def solve_fk(self, joints: ScaraJoints) -> ScaraPose:
        '''
            Tests solve fk.

            :param joints: Input joints.
            :exceptions: None.
        '''
        return ScaraPose(x=150.0, y=100.0, z=joints.z, phi=joints.theta4)

    def solve_ik(self, pose: ScaraPose, elbow_left: bool) -> ScaraJoints:
        '''
            Tests solve ik.

            :param pose: Input pose.
            :param elbow_left: Input elbow_left.
            :exceptions: None.
        '''
        _ = elbow_left
        return ScaraJoints(theta1=0.5, theta2=-0.8, z=pose.z, theta4=pose.phi, reachable=True)

    def steps_to_joints(self, steps: ScaraStepCoords) -> ScaraJoints:
        '''
            Tests steps to joints.

            :param steps: Input steps.
            :exceptions: None.
        '''
        _ = steps
        return ScaraJoints(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0, reachable=True)

    def joints_to_steps(self, joints: ScaraJoints) -> ScaraStepCoords:
        '''
            Tests joints to steps.

            :param joints: Input joints.
            :exceptions: None.
        '''
        _ = joints
        return ScaraStepCoords(j1_steps=0, j2_steps=0, z_steps=0, j4_steps=0)


class MockVirtualServer:
    '''
        Mock implementation of IVirtualManipulatorServer protocol.

        It defines:

            :methods:
                | start - Tests start.
                | stop - Tests stop.
                | is_running - Tests is running.
    '''

    def start(self, port: int) -> bool:
        '''
            Tests start.

            :param port: Input port.
            :exceptions: None.
        '''
        _ = port
        return True

    def stop(self) -> None:
        '''
            Tests stop.

            :exceptions: None.
        '''

    def is_running(self) -> bool:
        '''
            Tests is running.

            :exceptions: None.
        '''
        return False


class MockPreferenceRepository:
    '''
        Mock implementation of ISerialPreferenceRepository protocol.

        It defines:

            :methods:
                | has_preference - Tests has preference.
                | load_preference - Tests load preference.
                | save_preference - Tests save preference.
    '''

    def has_preference(self) -> bool:
        '''
            Tests has preference.

            :exceptions: None.
        '''
        return False

    def load_preference(self) -> SerialPreference:
        '''
            Tests load preference.

            :exceptions: None.
        '''
        return SerialPreference(port='/dev/ttyACM0', baud=115200)

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Tests save preference.

            :param preference: Input preference.
            :exceptions: None.
        '''
        _ = preference
        return True


class TestGuiFactory(TestCase):
    '''
        Unit tests for GuiFactory.

        It defines:

            :methods:
                | test_factory_creation - Tests assembling and instantiating GUI via GuiFactory.
                | test_get_version - Tests version string retrieval.
    '''

    def test_factory_creation(self) -> None:
        '''
            Tests assembling and instantiating GUI via GuiFactory.

            :exceptions: None.
        '''
        mock_server = MagicMock()
        mock_server.server = MockVirtualServer()
        mock_server.log_holder = ServerLogListenerHolder()

        mock_preferences = MagicMock()
        mock_preferences.serial = MockPreferenceRepository()
        mock_preferences.server = MagicMock()

        mock_scaralang = MagicMock()

        services = GuiServicesBundle(
            transport=MockTransport(),
            kinematics=MockKinematics(),
            emulation_service=MagicMock(),
            emulation_controller=MagicMock(),
            emulation_queue=MagicMock(),
            server=mock_server,
            preferences=mock_preferences,
            scaralang=mock_scaralang,
            port_scanner=MagicMock(),
        )
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
        provides = GuiFactory.create(
            dependencies=GuiDependencies(
                bounds=bounds,
                services=services,
            )
        )
        self.assertIsInstance(provides, GuiProvides)
        self.assertIsInstance(provides.gui, ScaraEmuGUI)
        self.assertTrue(provides.gui.is_initialized())

    def test_get_version(self) -> None:
        '''
            Tests version string retrieval.

            :exceptions: None.
        '''
        version = GuiFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    unittest_main()
