# -*- coding: UTF-8 -*-

'''
Module
    linear_path_interpolator.py
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
    Cartesian linear path segment subdivider and waypoint interpolator.
'''

from __future__ import annotations

from math import ceil, sqrt

from scaraemu.core.model.kinematics.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LinearPathInterpolator:
    '''
        Interpolates Cartesian linear trajectory segments into intermediate waypoints.

        It defines:

            :methods:
                | interpolate - Divides a straight line into fine intermediate Cartesian waypoints.
    '''

    @classmethod
    def interpolate(
        cls,
        start_pose: ScaraPose,
        end_pose: ScaraPose,
        segment_len_mm: float = 0.5
    ) -> list[ScaraPose]:
        '''
            Divides a straight Cartesian line into fine intermediate waypoints.

            :param start_pose: Start position.
            :param end_pose: End position.
            :param segment_len_mm: Maximum segment resolution in mm.
            :return: Ordered list of intermediate Cartesian waypoints.
            :exceptions: None.
        '''
        dx: float = end_pose.x - start_pose.x
        dy: float = end_pose.y - start_pose.y
        dz: float = end_pose.z - start_pose.z
        dphi: float = end_pose.phi - start_pose.phi

        distance: float = sqrt(dx * dx + dy * dy + dz * dz)
        if distance < 0.001 and abs(dphi) < 0.001:
            return [end_pose]

        num_segments: int = max(1, ceil(distance / max(0.01, segment_len_mm)))
        points: list[ScaraPose] = []

        for i in range(1, num_segments + 1):
            t: float = i / num_segments
            points.append(
                ScaraPose(
                    x=start_pose.x + dx * t,
                    y=start_pose.y + dy * t,
                    z=start_pose.z + dz * t,
                    phi=start_pose.phi + dphi * t
                )
            )

        return points
