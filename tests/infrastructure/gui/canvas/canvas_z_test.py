# -*- coding: UTF-8 -*-

'''
Module
    canvas_z_test.py
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
    Unit test cases for CanvasZ interactive canvas implementation.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scaraemu.core.model.kinematics.pose import ScaraPose
from scaraemu.infrastructure.gui.canvas.config import CanvasConfig
from scaraemu.infrastructure.gui.canvas.canvas_z import CanvasZ
from scaraemu.infrastructure.gui.canvas.icanvas_z import ICanvasZ
from scaraemu.infrastructure.gui.canvas.target.itarget_click_listener import ITargetClickListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasZTestCase(TestCase):
    '''
        Test case verifying behavior of CanvasZ widget.

        It defines:

            :methods:
                | setUp - Sets up test fixtures before each test method.
                | tearDown - Cleans up Tkinter resources.
                | test_implements_protocol - Verifies structural protocol conformance to ICanvasZ.
                | test_redraw_and_clear - Verifies redraw renders elements and clear empties canvas.
                | test_on_resize - Verifies canvas dimensions update on resize event.
                | test_on_mouse_click - Verifies mouse click triggers target click listener.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.bounds = ScaraBounds(
            links=LinkDimensions(l1=160.0, l2=130.0),
            vertical=VerticalBounds(z_min=0.0, z_max=120.0),
            speeds=SpeedLimits(
                min_speed=2.0, max_speed=250.0, default_speed=60.0,
                default_accel=120.0, max_accel=600.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.8, j1_max_rad=2.8,
                j2_min_rad=-2.7, j2_max_rad=2.7,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=4.0,
                singularity_inner_margin_mm=4.0,
                singularity_theta2_min_rad=0.09,
                deadzone_r_min=25.0,
            ),
        )
        self.listener = MagicMock(spec=ITargetClickListener)
        config = CanvasConfig(
            bounds=self.bounds,
            width=290,
            height=320,
            target_click_listener=self.listener,
        )
        self.canvas_z = CanvasZ(
            parent=self.root,
            config=config,
        )

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter resources.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_implements_protocol(self) -> None:
        '''
            Verifies structural protocol conformance to ICanvasZ.

            :exceptions: None.
        '''
        self.assertIsInstance(self.canvas_z, ICanvasZ)

    def test_redraw_and_clear(self) -> None:
        '''
            Verifies redraw renders elements and clear empties canvas.

            :exceptions: None.
        '''
        pose = ScaraPose(x=100.0, y=0.0, z=20.0, phi=0.0)
        target = ScaraPose(x=120.0, y=0.0, z=30.0, phi=0.0)
        self.canvas_z.redraw(pose=pose, current_target=target)
        items = self.canvas_z.find_all()
        self.assertGreater(len(items), 0)

        self.canvas_z.clear()
        cleared_items = self.canvas_z.find_all()
        self.assertEqual(len(cleared_items), 0)

    def test_on_resize(self) -> None:
        '''
            Verifies canvas dimensions update on resize event.

            :exceptions: None.
        '''
        event = MagicMock()
        event.width = 400
        event.height = 500
        self.canvas_z.on_resize(event)
        width, height = self.canvas_z.get_dimensions()
        self.assertEqual(width, 400.0)
        self.assertEqual(height, 500.0)

    def test_on_mouse_click(self) -> None:
        '''
            Verifies mouse click triggers target click listener.

            :exceptions: None.
        '''
        event = MagicMock()
        event.y = 100
        self.canvas_z.on_mouse_click(event)
        self.listener.handle_z_click.assert_called_once()


if __name__ == '__main__':
    unittest_main()
