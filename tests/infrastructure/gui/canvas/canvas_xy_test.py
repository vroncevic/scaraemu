# -*- coding: UTF-8 -*-

'''
Module
    canvas_xy_test.py
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
    Unit test cases for CanvasXY interactive canvas implementation.
'''

from __future__ import annotations

from tkinter import Event, Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaralang.core.service.kinematics.workspace.boundary.factory import BoundaryFactory

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.canvas_xy import CanvasXY
from scaraemu.infrastructure.gui.canvas.icanvas_xy import ICanvasXY
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener
from scaraemu.infrastructure.scaralang.kinematics.linkage.factory import LinkageAdapterFactory
from scaraemu.infrastructure.scaralang.kinematics.linkage.iadapter import ILinkageAdapter
from scaraemu.infrastructure.scaralang.reach.factory import WorkspaceReachAdapterFactory
from scaraemu.infrastructure.scaralang.reach.iadapter import IWorkspaceReachAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasXYTestCase(TestCase):
    '''
        Test case verifying behavior of CanvasXY widget.

        It defines:

            :methods:
                | setUp - Sets up test fixtures before each test method.
                | tearDown - Cleans up Tkinter resources.
                | test_implements_protocol - Verifies structural protocol conformance to ICanvasXY.
                | test_redraw - Verifies redraw renders elements on canvas.
                | test_on_resize - Verifies resize updates canvas viewport.
                | test_on_mouse_click - Verifies mouse click triggers target click listener.
                | test_on_mouse_click_unreachable - Verifies mouse click triggers flash unreachable on rejection.
                | test_flash_unreachable - Verifies flash unreachable creates indicator items.
    '''

    root: Tk
    bounds: ScaraBounds
    listener: MagicMock
    canvas_xy: CanvasXY

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.bounds = ScaraBounds(
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
        self.listener = MagicMock(spec=ITargetClickListener)
        config = CanvasConfig(
            bounds=self.bounds,
            width=400,
            height=400,
            target_click_listener=self.listener,
        )
        manipulator_linkage_adapter: ILinkageAdapter = (
            LinkageAdapterFactory.create(self.bounds)
        )
        reach_adapter: IWorkspaceReachAdapter = (
            WorkspaceReachAdapterFactory.create(bounds=self.bounds)
        )
        boundary_service = BoundaryFactory.create().service
        self.canvas_xy = CanvasXY(
            parent=self.root,
            config=config,
            manipulator_linkage_adapter=manipulator_linkage_adapter,
            reach_adapter=reach_adapter,
            boundary_service=boundary_service,
        )

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter resources.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_implements_protocol(self) -> None:
        '''
            Verifies structural protocol conformance to ICanvasXY.

            :exceptions: None.
        '''
        self.assertIsInstance(self.canvas_xy, ICanvasXY)

    def test_redraw(self) -> None:
        '''
            Verifies redraw renders elements on canvas.

            :exceptions: None.
        '''
        pose: ScaraPose = ScaraPose(x=150.0, y=50.0, z=20.0, phi=0.0)
        joints: ScaraJoints = ScaraJoints(
            theta1=0.2, theta2=0.4, z=20.0, theta4=0.0, reachable=True
        )
        trail_points: list[tuple[float, float]] = [(100.0, 50.0), (150.0, 50.0)]
        target: ScaraPose = ScaraPose(x=160.0, y=60.0, z=20.0, phi=0.0)

        self.canvas_xy.redraw(
            pose=pose,
            joints=joints,
            trail_points=trail_points,
            current_target=target,
        )
        items = self.canvas_xy.find_all()
        self.assertGreater(len(items), 0)

    def test_on_resize(self) -> None:
        '''
            Verifies resize updates canvas viewport.

            :exceptions: None.
        '''
        event: Event = Event()
        event.width = 500
        event.height = 500
        self.canvas_xy.on_resize(event)
        width, height = self.canvas_xy.get_dimensions()
        self.assertEqual(width, 500.0)
        self.assertEqual(height, 500.0)

    def test_on_mouse_click(self) -> None:
        '''
            Verifies mouse click triggers target click listener.

            :exceptions: None.
        '''
        self.listener.handle_xy_click.return_value = True
        event: Event = Event()
        event.x = 200
        event.y = 200
        self.canvas_xy.on_mouse_click(event)
        self.listener.handle_xy_click.assert_called_once()

    def test_on_mouse_click_unreachable(self) -> None:
        '''
            Verifies mouse click triggers flash unreachable on rejection.

            :exceptions: None.
        '''
        self.listener.handle_xy_click.return_value = False
        event: Event = Event()
        event.x = 200
        event.y = 200
        self.canvas_xy.on_mouse_click(event)
        tag: str = f'unreachable_{id(self.canvas_xy)}'
        items = self.canvas_xy.find_withtag(tag)
        self.assertGreater(len(items), 0)

    def test_flash_unreachable(self) -> None:
        '''
            Verifies flash unreachable creates indicator items.

            :exceptions: None.
        '''
        self.canvas_xy.flash_unreachable(300.0, 300.0)
        tag: str = f'unreachable_{id(self.canvas_xy)}'
        items = self.canvas_xy.find_withtag(tag)
        self.assertGreater(len(items), 0)


if __name__ == '__main__':
    unittest_main()
