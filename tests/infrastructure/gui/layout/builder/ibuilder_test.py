# -*- coding: UTF-8 -*-

'''
Module
    ibuilder_test.py
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
    Unit tests for ILayoutBuilder structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from tkinter import Tk
from unittest import TestCase, main as unittest_main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.layout.builder.builder import LayoutBuilder
from scaraemu.infrastructure.gui.layout.builder.ibuilder import ILayoutBuilder
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView
from scaraemu.infrastructure.gui.trajectory.queue.iview import IQueueDepthView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyCanvasXY:
    '''
        Dummy conforming implementation of ICanvasXY.

        It defines:

            :methods:
                | redraw - Renders robot links and joints.
                | flash_unreachable - Flashes unreachable indicator.
                | get_version - Returns version string.
    '''

    def redraw(
        self,
        *,
        pose: ScaraPose,
        joints: ScaraJoints,
        trail_points: Sequence[tuple[float, float]],
        current_target: ScaraPose,
        planned_path: Sequence[tuple[float, float]] = (),
    ) -> None:
        '''
            Renders robot links and joints.

            :param pose: Robot pose.
            :param joints: Robot joints.
            :param trail_points: Historical path trail points.
            :param current_target: Active target pose.
            :param planned_path: Planned trajectory coordinates.
            :exceptions: None.
        '''
        _ = (pose, joints, trail_points, current_target, planned_path)

    def flash_unreachable(self) -> None:
        '''
            Flashes unreachable indicator.

            :exceptions: None.
        '''
        _ = self

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _DummyCanvasZ:
    '''
        Dummy conforming implementation of ICanvasZ.

        It defines:

            :methods:
                | redraw - Renders vertical position.
                | clear - Clears canvas elements.
                | get_version - Returns version string.
    '''

    def redraw(self, *, z_mm: float) -> None:
        '''
            Renders vertical position.

            :param z_mm: Height in mm.
            :exceptions: None.
        '''
        _ = z_mm

    def clear(self) -> None:
        '''
            Clears canvas.

            :exceptions: None.
        '''
        _ = self

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _DummyTelemetryView:
    '''
        Dummy conforming implementation of ITelemetryView.

        It defines:

            :methods:
                | update_telemetry - Updates telemetry readout.
                | get_version - Returns version string.
    '''

    def update_telemetry(self, telemetry: Telemetry) -> None:
        '''
            Updates telemetry readout.

            :param telemetry: Telemetry data model.
            :exceptions: None.
        '''
        _ = telemetry

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _DummyQueueView:
    '''
        Dummy conforming implementation of IQueueDepthView.

        It defines:

            :methods:
                | update_depth - Updates queue depth display.
                | get_version - Returns version string.
    '''

    def update_depth(self, depth: int) -> None:
        '''
            Updates queue depth display.

            :param depth: Queue depth count.
            :exceptions: None.
        '''
        _ = depth

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _ValidLayoutBuilder:
    '''
        Dummy class conforming to ILayoutBuilder structurally.

        It defines:

            :attributes:
                | canvas_xy - Planar view canvas.
                | canvas_z - Elevation side view canvas.
                | telemetry_view - Telemetry monitor port.
                | queue_view - Trajectory queue depth observer.
            :methods:
                | build_layout - Builds layout hierarchy.
                | set_connected_state - Updates hardware connection state.
                | set_server_state - Updates virtual server state.
                | append_log - Appends diagnostic log entry.
                | get_version - Returns version string.
    '''

    canvas_xy: ICanvasXY = _DummyCanvasXY()
    canvas_z: ICanvasZ = _DummyCanvasZ()
    telemetry_view: ITelemetryView = _DummyTelemetryView()
    queue_view: IQueueDepthView = _DummyQueueView()

    def build_layout(
        self,
        *,
        root: Tk,
        bounds: ScaraBounds,
        target_click_listener: ITargetClickListener,
        delegates: GuiDelegatesBundle,
    ) -> None:
        '''
            Builds layout hierarchy.

            :param root: Root Tk widget.
            :param bounds: Kinematic bounds.
            :param target_click_listener: Click target listener.
            :param delegates: GUI delegates bundle.
            :exceptions: None.
        '''
        _ = (root, bounds, target_click_listener, delegates)

    def set_connected_state(self, connected: bool) -> None:
        '''
            Updates hardware connection state.

            :param connected: True if connected to hardware, False otherwise.
            :exceptions: None.
        '''
        _ = connected

    def set_server_state(self, running: bool, port: int = 8888) -> None:
        '''
            Updates virtual server state.

            :param running: True if server active, False otherwise.
            :param port: Listening TCP port number.
            :exceptions: None.
        '''
        _ = (running, port)

    def append_log(self, message: str, tag: str) -> None:
        '''
            Appends diagnostic log entry.

            :param message: Diagnostic log message.
            :param tag: Log entry category tag.
            :exceptions: None.
        '''
        _ = (message, tag)

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidLayoutBuilder:
    '''
        Dummy class missing required protocol methods and attributes.

        It defines:

            :methods:
                | dummy_action - Dummy action method.
                | get_status - Returns status flag.
    '''

    def dummy_action(self) -> None:
        '''
            Performs dummy action.

            :exceptions: None.
        '''
        _ = self

    def get_status(self) -> bool:
        '''
            Returns dummy status.

            :return: Boolean flag.
            :exceptions: None.
        '''
        return False


class TestILayoutBuilder(TestCase):
    '''
        Test cases verifying ILayoutBuilder structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy class satisfies protocol.
                | test_non_conforming_instance - Verifies invalid class fails protocol check.
                | test_concrete_class_satisfies_protocol - Verifies LayoutBuilder satisfies protocol.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies ILayoutBuilder structurally.

            :exceptions: None.
        '''
        builder = _ValidLayoutBuilder()
        self.assertIsInstance(builder, ILayoutBuilder)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy ILayoutBuilder.

            :exceptions: None.
        '''
        invalid = _InvalidLayoutBuilder()
        self.assertNotIsInstance(invalid, ILayoutBuilder)

    def test_concrete_class_satisfies_protocol(self) -> None:
        '''
            Verifies LayoutBuilder has required protocol attributes.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(LayoutBuilder, 'build_layout'))
        self.assertTrue(hasattr(LayoutBuilder, 'set_connected_state'))
        self.assertTrue(hasattr(LayoutBuilder, 'set_server_state'))
        self.assertTrue(hasattr(LayoutBuilder, 'append_log'))
        self.assertTrue(hasattr(LayoutBuilder, 'get_version'))


if __name__ == '__main__':
    unittest_main()
