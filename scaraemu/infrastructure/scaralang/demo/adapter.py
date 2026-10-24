# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating trajectory demonstration generation to scaralang.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.discretization.circle.icircle import ICircleDiscretizer
from scaralang.core.service.trajectory.discretization.rectangle.irectangle import IRectangleDiscretizer

from scaraemu.core.model.kinematics.pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoAdapter:
    '''
        Adapter generating demonstration trajectories via scaralang shape discretization.

        It defines:

            :attributes:
                | _circle - Injected scaralang circle discretizer service.
                | _rectangle - Injected scaralang rectangle discretizer service.
            :methods:
                | __init__ - Initializes adapter with injected scaralang discretizers.
                | generate - Generates demonstration Cartesian waypoints for a preset pattern.
                | get_version - Returns adapter component version string.
    '''

    def __init__(
        self,
        circle: ICircleDiscretizer,
        rectangle: IRectangleDiscretizer,
    ) -> None:
        '''
            Initializes adapter with scaralang shape discretizer services.

            :param circle: Injected scaralang ICircleDiscretizer instance.
            :param rectangle: Injected scaralang IRectangleDiscretizer instance.
            :exceptions: None.
        '''
        self._circle: Final[ICircleDiscretizer] = circle
        self._rectangle: Final[IRectangleDiscretizer] = rectangle

    def generate(
        self,
        preset_name: str,
        center_x: float,
        center_y: float,
        z: float,
    ) -> list[ScaraPose]:
        '''
            Generates demonstration Cartesian waypoints for a preset pattern.

            :param preset_name: Preset demonstration identifier name.
            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param z: Constant height coordinate in mm.
            :return: Ordered list of Cartesian poses for trajectory execution.
            :exceptions: None.
        '''
        match preset_name:
            case 'circle':
                geom: CircleGeometry = CircleGeometry(
                    center=Point2D(x=center_x, y=center_y),
                    radius=30.0,
                    steps=32,
                    z=z,
                    speed=40.0,
                )
                waypoints: list[Waypoint] = self._circle.discretize(
                    geometry=geom
                )
                return [
                    ScaraPose(x=wp.x, y=wp.y, z=wp.z, phi=wp.phi)
                    for wp in waypoints
                ]

            case 'square':
                p1: Point2D = Point2D(x=center_x - 25.0, y=center_y - 25.0)
                p2: Point2D = Point2D(x=center_x + 25.0, y=center_y + 25.0)
                waypoints = self._rectangle.discretize(
                    p1, p2, z=z, speed=40.0
                )
                return [
                    ScaraPose(x=wp.x, y=wp.y, z=wp.z, phi=wp.phi)
                    for wp in waypoints
                ]

            case _:
                return [ScaraPose(x=center_x, y=center_y, z=z, phi=0.0)]

    def get_version(self) -> str:
        '''
            Returns adapter component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
