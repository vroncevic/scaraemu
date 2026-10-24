# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit tests for LayoutBuilder.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService

from scaracom.transport.preference.preference import SerialPreference
from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.builder import LayoutBuilder
from scaraemu.infrastructure.gui.layout.builder.dependencies import LayoutDependencies
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _MockSerialBarDelegate:
    '''
        Mock delegate for serial bar actions.
    '''

    def handle_connect_toggle(self, port: str, baudrate: int) -> None:
        '''
            Tests handle connect toggle.

            :param port: Input port.
            :param baudrate: Input baudrate.
            :exceptions: None.
        '''
        _ = (port, baudrate)

    def handle_server_toggle(self) -> None:
        '''
            Tests handle server toggle.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'



class _MockQueueActionDelegate:
    '''
        Mock delegate for queue actions.
    '''

    def handle_clear_queue(self) -> None:
        '''
            Tests handle clear queue.

            :exceptions: None.
        '''

    def handle_clear_trail(self) -> None:
        '''
            Tests handle clear trail.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _MockCanvasTargetClickListener:
    '''
        Mock listener for canvas clicks.
    '''

    def handle_xy_click(self, x: float, y: float) -> None:
        '''
            Tests handle xy click.

            :param x: Input x.
            :param y: Input y.
            :exceptions: None.
        '''
        _ = (x, y)

    def handle_z_click(self, z: float) -> None:
        '''
            Tests handle z click.

            :param z: Input z.
            :exceptions: None.
        '''
        _ = z

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockJogDelegate:
    '''
        Mock delegate for jog actions.
    '''

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Tests handle jog.

            :param dx: Input dx.
            :param dy: Input dy.
            :param dz: Input dz.
            :param dphi: Input dphi.
            :exceptions: None.
        '''
        _ = (dx, dy, dz, dphi)

    def handle_home(self, axis: str) -> None:
        '''
            Tests handle home.

            :param axis: Input axis.
            :exceptions: None.
        '''
        _ = axis

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockMachineConfigurationDelegate:
    '''
        Mock delegate for machine configuration actions.
    '''

    def handle_toggle_elbow(self) -> None:
        '''
            Tests handle toggle elbow.

            :exceptions: None.
        '''

    def handle_toggle_motors(self) -> None:
        '''
            Tests handle toggle motors.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockMachineSafetyDelegate:
    '''
        Mock delegate for machine safety actions.
    '''

    def handle_toggle_hold(self) -> None:
        '''
            Tests handle toggle hold.

            :exceptions: None.
        '''

    def handle_estop(self) -> None:
        '''
            Tests handle estop.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockTrajectoryPresetDelegate:
    '''
        Mock delegate for trajectory preset actions.
    '''

    def handle_demo_select(self, preset_name: str) -> None:
        '''
            Tests handle demo select.

            :param preset_name: Input preset_name.
            :exceptions: None.
        '''
        _ = preset_name

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class _MockScriptLoaderDelegate:
    '''
        Mock delegate for script loader actions.
    '''

    def handle_load_script(self, script_path: str) -> None:
        '''
            Tests handle load script.

            :param script_path: Input script_path.
            :exceptions: None.
        '''
        _ = script_path

    def get_version(self) -> str:
        '''
            Tests get version.

            :exceptions: None.
        '''
        return '1.0.2'


class TestLayoutBuilder(TestCase):
    '''
        Unit tests for LayoutBuilder.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_get_version - Tests builder version retrieval.
                | test_build_layout - Tests building and packing entire widget hierarchy.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

        self._port_scanner = MagicMock(spec=IPortScanner)
        self._port_scanner.scan_ports.return_value = ['/dev/ttyUSB0']
        self._port_scanner.get_version.return_value = '1.0.2'

        self._preference_repository = MagicMock(spec=ISerialPreferenceRepository)
        self._preference_repository.has_preference.return_value = True
        self._preference_repository.load_preference.return_value = SerialPreference(
            port='/dev/ttyUSB0', baud=115200
        )
        self._preference_repository.save_preference.return_value = True
        self._preference_repository.get_version.return_value = '1.0.2'

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_get_version(self) -> None:
        '''
            Tests builder version retrieval.

            :exceptions: None.
        '''
        deps = LayoutDependencies(
            port_scanner=self._port_scanner,
            preference_repository=self._preference_repository,
            manipulator_linkage_adapter=MagicMock(spec=ILinkageAdapter),
            reach_adapter=MagicMock(spec=IWorkspaceReachAdapter),
            boundary_service=MagicMock(spec=IWorkspaceBoundaryService),
        )
        builder = LayoutBuilder(dependencies=deps)
        self.assertEqual(builder.get_version(), '1.0.2')
        builder.set_connected_state(True)
        builder.set_server_state(True, 8888)
        builder.append_log('Pre-build log', 'info')

    def test_build_layout(self) -> None:
        '''
            Tests building and packing entire widget hierarchy.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

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
        deps = LayoutDependencies(
            port_scanner=self._port_scanner,
            preference_repository=self._preference_repository,
            manipulator_linkage_adapter=MagicMock(spec=ILinkageAdapter),
            reach_adapter=MagicMock(spec=IWorkspaceReachAdapter),
            boundary_service=MagicMock(spec=IWorkspaceBoundaryService),
        )
        builder = LayoutBuilder(dependencies=deps)
        delegates = GuiDelegatesBundle(
            jog=_MockJogDelegate(),
            config=_MockMachineConfigurationDelegate(),
            safety=_MockMachineSafetyDelegate(),
            preset=_MockTrajectoryPresetDelegate(),
            script=_MockScriptLoaderDelegate(),
            serial_bar=_MockSerialBarDelegate(),
            queue=_MockQueueActionDelegate(),
        )
        builder.build_layout(
            root=self._root,
            bounds=bounds,
            target_click_listener=_MockCanvasTargetClickListener(),
            delegates=delegates,
        )

        self.assertIsNotNone(builder.serial_bar)
        self.assertIsNotNone(builder.canvas_xy)
        self.assertIsNotNone(builder.canvas_z)
        self.assertIsNotNone(builder.telemetry_panel)
        self.assertIsNotNone(builder.jog_panel)
        self.assertIsNotNone(builder.machine_panel)
        self.assertIsNotNone(builder.demo_panel)
        self.assertIsNotNone(builder.console_panel)

        builder.set_connected_state(True)
        builder.set_server_state(True, 8888)
        builder.append_log('Post-build log', 'info')


if __name__ == '__main__':
    unittest_main()
