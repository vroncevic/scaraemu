# -*- coding: UTF-8 -*-

'''
Module
    scara_script_loader.py
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
    Implementation of IScaraScriptLoader converting .scara DSL and JSON plans into ScaraPose trajectories.
'''

from __future__ import annotations

from json import loads
from math import atan2, cos, hypot, pi, sin
from re import compile as re_compile, Pattern
from typing import ClassVar

from scaraemu.core.model.scara_pose import ScaraPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraScriptLoader:
    '''
        Service translating .scara scripts and plan JSON files into ScaraPose waypoints.

        It defines:

            :methods:
                | load_from_file - Reads and parses script or plan from filesystem.
                | parse_script - Parses raw script text content into sequence of poses.
                | _extract_params - Extracts key-value parameters from command line tokens.
                | _generate_arc_points - Generates interpolated arc intermediate poses.
    '''

    _PARAM_PATTERN: ClassVar[Pattern[str]] = re_compile(
        r'([A-Za-z_]+)\s*=\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)'
    )

    def load_from_file(self, *, filepath: str) -> list[ScaraPose]:
        '''
            Reads and parses a script or plan file from the filesystem.

            :param filepath: Path to .scara or .json trajectory plan file.
            :return: List of ScaraPose waypoints.
            :exceptions: OSError, ValueError.
        '''
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if filepath.lower().endswith('.json'):
            data = loads(content)
            poses: list[ScaraPose] = []
            waypoints = data.get('waypoints', [])
            for pt in waypoints:
                if isinstance(pt, dict) and 'x' in pt and 'y' in pt:
                    poses.append(
                        ScaraPose(
                            x=float(pt['x']),
                            y=float(pt['y']),
                            z=float(pt.get('z', 20.0)),
                            phi=float(pt.get('phi', 0.0)),
                        )
                    )
            return poses

        return self.parse_script(source=content)

    def parse_script(self, *, source: str) -> list[ScaraPose]:
        '''
            Parses raw script text content into sequence of ScaraPose waypoints.

            :param source: SCARA DSL source text.
            :return: List of ScaraPose waypoints.
            :exceptions: ValueError.
        '''
        poses: list[ScaraPose] = []
        curr_x: float = 180.0
        curr_y: float = 0.0
        curr_z: float = 20.0
        curr_phi: float = 0.0

        for raw_line in source.splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue
            if '#' in line:
                line = line.split('#', 1)[0].strip()

            tokens = line.split()
            if not tokens:
                continue

            cmd = tokens[0].upper()
            params = self._extract_params(line=line)

            match cmd:
                case 'HOME':
                    curr_x, curr_y, curr_z, curr_phi = 180.0, 0.0, 20.0, 0.0
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=curr_z, phi=curr_phi))

                case 'MOVE_L' | 'MOVE_J':
                    curr_x = params.get('X', curr_x)
                    curr_y = params.get('Y', curr_y)
                    curr_z = params.get('Z', curr_z)
                    curr_phi = params.get('PHI', curr_phi)
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=curr_z, phi=curr_phi))

                case 'JUMP':
                    target_x = params.get('X', curr_x)
                    target_y = params.get('Y', curr_y)
                    target_z = params.get('Z', curr_z)
                    arch = params.get('ARCH', 25.0)
                    apex_z = max(curr_z, target_z) + arch
                    mid_x = (curr_x + target_x) * 0.5
                    mid_y = (curr_y + target_y) * 0.5
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=apex_z, phi=curr_phi))
                    poses.append(ScaraPose(x=mid_x, y=mid_y, z=apex_z, phi=curr_phi))
                    curr_x, curr_y, curr_z = target_x, target_y, target_z
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=curr_z, phi=curr_phi))

                case 'APPROACH':
                    dist = params.get('DIST', 10.0)
                    curr_z = max(0.0, curr_z - dist)
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=curr_z, phi=curr_phi))

                case 'RETRACT':
                    dist = params.get('DIST', 10.0)
                    curr_z = curr_z + dist
                    poses.append(ScaraPose(x=curr_x, y=curr_y, z=curr_z, phi=curr_phi))

                case 'ARC_CW' | 'ARC_CCW':
                    target_x = params.get('X', curr_x)
                    target_y = params.get('Y', curr_y)
                    target_z = params.get('Z', curr_z)
                    offset_i = params.get('I', 0.0)
                    offset_j = params.get('J', 0.0)
                    arc_pts = self._generate_arc_points(
                        start_x=curr_x,
                        start_y=curr_y,
                        target_x=target_x,
                        target_y=target_y,
                        offset_i=offset_i,
                        offset_j=offset_j,
                        is_cw=(cmd == 'ARC_CW'),
                        z=target_z,
                        phi=curr_phi,
                    )
                    poses.extend(arc_pts)
                    curr_x, curr_y, curr_z = target_x, target_y, target_z

                case _:
                    pass

        return poses

    def _extract_params(self, *, line: str) -> dict[str, float]:
        '''
            Extracts key-value numerical parameters from a command line string.

            :param line: Raw command line string.
            :return: Dictionary of uppercase parameter names to numerical values.
        '''
        params: dict[str, float] = {}
        for match in self._PARAM_PATTERN.finditer(line):
            key = match.group(1).upper()
            val = float(match.group(2))
            params[key] = val
        return params

    def _generate_arc_points(
        self,
        *,
        start_x: float,
        start_y: float,
        target_x: float,
        target_y: float,
        offset_i: float,
        offset_j: float,
        is_cw: bool,
        z: float,
        phi: float,
        steps: int = 12,
    ) -> list[ScaraPose]:
        '''
            Generates interpolated arc intermediate poses.

            :param start_x: Starting X coordinate in mm.
            :param start_y: Starting Y coordinate in mm.
            :param target_x: Ending X coordinate in mm.
            :param target_y: Ending Y coordinate in mm.
            :param offset_i: Center X offset relative to start.
            :param offset_j: Center Y offset relative to start.
            :param is_cw: True for clockwise, False for counter-clockwise.
            :param z: Z elevation in mm.
            :param phi: End-effector orientation angle in degrees.
            :param steps: Number of interpolation subdivision segments.
            :return: List of interpolated ScaraPose waypoints.
        '''
        center_x = start_x + offset_i
        center_y = start_y + offset_j
        radius = hypot(offset_i, offset_j)
        if radius < 1e-4:
            return [ScaraPose(x=target_x, y=target_y, z=z, phi=phi)]

        start_angle = atan2(start_y - center_y, start_x - center_x)
        end_angle = atan2(target_y - center_y, target_x - center_x)

        if is_cw:
            if end_angle >= start_angle:
                end_angle -= 2.0 * pi
        else:
            if end_angle <= start_angle:
                end_angle += 2.0 * pi

        delta_angle = end_angle - start_angle
        pts: list[ScaraPose] = []
        for i in range(1, steps + 1):
            theta = start_angle + (delta_angle * i / steps)
            px = center_x + radius * cos(theta)
            py = center_y + radius * sin(theta)
            pts.append(ScaraPose(x=px, y=py, z=z, phi=phi))
        return pts
