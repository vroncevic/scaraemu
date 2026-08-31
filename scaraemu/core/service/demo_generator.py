# -*- coding: UTF-8 -*-

'''
Module
    demo_generator.py
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
    Autonomous demonstration trajectory generators for SCARA robot.
'''

from __future__ import annotations

import math
from typing import Callable, Final
from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoGenerator:
    '''
        Generator of synthetic demonstration trajectories (Circle, Square, Star, Helix).

        It defines:

            :attributes:
                | AVAILABLE_DEMOS - Tuple of supported demo type identifiers.
                | _REGISTRY - Internal dictionary mapping demo names to generator functions.
            :methods:
                | generate - Dispatches trajectory generation for specified demo name.
                | generate_circle - Generates circular planar trajectory.
                | generate_square - Generates rectangular planar trajectory.
                | generate_star - Generates 5-pointed star planar trajectory.
                | generate_helix - Generates 3D helical trajectory.
    '''

    AVAILABLE_DEMOS: Final[tuple[str, ...]] = ('circle', 'square', 'star', 'helix')

    @classmethod
    def generate(
        cls,
        demo_name: str,
        center_x: float = 160.0,
        center_y: float = 0.0,
        z: float = 20.0
    ) -> list[ScaraPose]:
        '''
            Dispatches trajectory generation for specified demo name.

            :param demo_name: Identifier of demo trajectory.
            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param z: Reference Z elevation in mm.
            :return: List of ScaraPose waypoints.
            :exceptions: None.
        '''
        generators: dict[str, Callable[[], list[ScaraPose]]] = {
            'circle': lambda: cls.generate_circle(center_x, center_y, radius=35.0, z=z),
            'square': lambda: cls.generate_square(center_x, center_y, side=60.0, z=z),
            'star': lambda: cls.generate_star(center_x, center_y, r_outer=45.0, r_inner=20.0, z=z),
            'helix': lambda: cls.generate_helix(center_x, center_y, radius=30.0, z_start=10.0, z_end=70.0)
        }
        gen = generators.get(demo_name.lower())
        return gen() if gen is not None else []

    @classmethod
    def generate_circle(
        cls,
        center_x: float = 160.0,
        center_y: float = 0.0,
        radius: float = 45.0,
        z: float = 20.0,
        num_points: int = 60
    ) -> list[ScaraPose]:
        '''
            Generates circular planar trajectory.

            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param radius: Circle radius in mm.
            :param z: Z elevation in mm.
            :param num_points: Discretization point count.
            :return: List of ScaraPose waypoints.
            :exceptions: None.
        '''
        poses: list[ScaraPose] = []
        for i in range(num_points + 1):
            angle: float = 2.0 * math.pi * (i / num_points)
            px: float = center_x + radius * math.cos(angle)
            py: float = center_y + radius * math.sin(angle)
            poses.append(ScaraPose(x=px, y=py, z=z, phi=0.0))
        return poses

    @classmethod
    def generate_square(
        cls,
        center_x: float = 160.0,
        center_y: float = 0.0,
        side: float = 70.0,
        z: float = 20.0
    ) -> list[ScaraPose]:
        '''
            Generates rectangular planar trajectory.

            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param side: Side length in mm.
            :param z: Z elevation in mm.
            :return: List of ScaraPose waypoints.
            :exceptions: None.
        '''
        half: float = side / 2.0
        corners: list[tuple[float, float]] = [
            (center_x - half, center_y - half),
            (center_x + half, center_y - half),
            (center_x + half, center_y + half),
            (center_x - half, center_y + half),
            (center_x - half, center_y - half)
        ]
        return [ScaraPose(x=cx, y=cy, z=z, phi=0.0) for cx, cy in corners]

    @classmethod
    def generate_star(
        cls,
        center_x: float = 160.0,
        center_y: float = 0.0,
        r_outer: float = 55.0,
        r_inner: float = 25.0,
        z: float = 20.0
    ) -> list[ScaraPose]:
        '''
            Generates 5-pointed star planar trajectory.

            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param r_outer: Outer tip radius in mm.
            :param r_inner: Inner vertex radius in mm.
            :param z: Z elevation in mm.
            :return: List of ScaraPose waypoints.
            :exceptions: None.
        '''
        poses: list[ScaraPose] = []
        for i in range(11):
            angle: float = math.pi / 2.0 + (i * math.pi / 5.0)
            rad: float = r_outer if i % 2 == 0 else r_inner
            px: float = center_x + rad * math.cos(angle)
            py: float = center_y + rad * math.sin(angle)
            poses.append(ScaraPose(x=px, y=py, z=z, phi=0.0))
        return poses

    @classmethod
    def generate_helix(
        cls,
        center_x: float = 160.0,
        center_y: float = 0.0,
        radius: float = 40.0,
        z_start: float = 10.0,
        z_end: float = 70.0,
        turns: int = 2,
        num_points: int = 100
    ) -> list[ScaraPose]:
        '''
            Generates 3D helical trajectory.

            :param center_x: Center X coordinate in mm.
            :param center_y: Center Y coordinate in mm.
            :param radius: Helix horizontal radius in mm.
            :param z_start: Starting Z elevation in mm.
            :param z_end: Ending Z elevation in mm.
            :param turns: Number of full revolutions.
            :param num_points: Discretization point count.
            :return: List of ScaraPose waypoints.
            :exceptions: None.
        '''
        poses: list[ScaraPose] = []
        z_range: float = z_end - z_start
        for i in range(num_points + 1):
            t: float = i / num_points
            angle: float = 2.0 * math.pi * turns * t
            px: float = center_x + radius * math.cos(angle)
            py: float = center_y + radius * math.sin(angle)
            pz: float = z_start + z_range * t
            poses.append(ScaraPose(x=px, y=py, z=pz, phi=0.0))
        return poses
