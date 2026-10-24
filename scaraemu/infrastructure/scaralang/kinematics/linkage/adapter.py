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
    Concrete adapter providing arm forward kinematics calculation via scaralang.
'''

from __future__ import annotations

from typing import Final
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LinkageAdapter:
    '''
        Adapter computing arm linkage poses via scaralang kinematics service.

        It defines:

            :attributes:
                | _planar - Injected scaralang planar kinematics solver.
            :methods:
                | __init__ - Initializes adapter with scaralang planar solver collaborator.
                | solve_fk_pose - Computes Cartesian coordinates of elbow and wrist joints.
                | solve_fk - Computes Cartesian end-effector coordinates from joint angles.
                | get_version - Returns adapter version string.
    '''

    _planar: IPlanarKinematicsSolver

    def __init__(self, planar: IPlanarKinematicsSolver) -> None:
        '''
            Initializes manipulator linkage adapter with scaralang planar solver.

            :param planar: Injected IPlanarKinematicsSolver collaborator.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = planar

    def solve_fk_pose(
        self,
        theta1_rad: float,
        theta2_rad: float,
    ) -> tuple[Point2D, Point2D]:
        '''
            Computes Cartesian positions of both elbow and wrist joints via scaralang.

            :param theta1_rad: J1 base joint angle in radians.
            :param theta2_rad: J2 elbow joint angle in radians.
            :return: Tuple of (elbow_point, wrist_point) Cartesian coordinates.
            :exceptions: None.
        '''
        return self._planar.solve_fk_pose_2d(theta1_rad, theta2_rad)

    def solve_fk(
        self,
        theta1_rad: float,
        theta2_rad: float,
    ) -> Point2D:
        '''
            Computes Cartesian end-effector position from joint angles via scaralang.

            :param theta1_rad: J1 base joint angle in radians.
            :param theta2_rad: J2 elbow joint angle in radians.
            :return: Cartesian coordinate point.
            :exceptions: None.
        '''
        return self._planar.solve_fk_2d(theta1_rad, theta2_rad)

    def get_version(self) -> str:
        '''
            Returns adapter version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
