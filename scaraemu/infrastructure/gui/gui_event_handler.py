# -*- coding: UTF-8 -*-

'''
Module
    gui_event_handler.py
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
    Encapsulates user interaction event handlers for the SCARA emulator GUI.
'''

from __future__ import annotations

from typing import Callable, Final

from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.core.service.iservice import IService
from scaraemu.core.service.demo_generator import TrajectoryDemoGenerator
from scaraemu.infrastructure.communication.protocol.command_formatter import CommandFormatter
from scaraemu.infrastructure.gui.hardware_bridge_controller import HardwareBridgeController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiEventHandler:
    '''
        Encapsulates user interaction event handling for emulator and hardware bridge.

        It defines:

            :methods:
                | handle_xy_click - Handles click on planar XY canvas.
                | handle_z_click - Handles click on vertical Z canvas.
                | handle_jog - Handles incremental jog displacement.
                | handle_home - Handles homing motion command.
                | handle_toggle_elbow - Toggles Lefty/Righty configuration.
                | handle_toggle_motors - Toggles motor power state.
                | handle_estop - Triggers emergency stop.
                | handle_demo_select - Generates and queues demo trajectory.
    '''

    _service: Final[IService]
    _bridge: Final[HardwareBridgeController]
    _log_host: Final[Callable[[str, str], None]]
    _flash_unreachable: Final[Callable[[float, float], None] | None]

    def __init__(
        self,
        service: IService,
        bridge: HardwareBridgeController,
        log_host: Callable[[str, str], None],
        flash_unreachable: Callable[[float, float], None] | None = None
    ) -> None:
        '''
            Initializes GUI event handler with domain service and bridge controller.

            :param service: Top-level service locator instance.
            :param bridge: Hardware bridge controller instance.
            :param log_host: Logging callback for host diagnostics.
            :param flash_unreachable: Canvas flash unreachable coordinate callback.
            :exceptions: None.
        '''
        self._service = service
        self._bridge = bridge
        self._log_host = log_host
        self._flash_unreachable = flash_unreachable

    def _diagnose_pose(self, pose: ScaraPose) -> tuple[bool, str]:
        '''
            Checks motor power, emergency stop, and kinematic reachability.

            :param pose: Target ScaraPose.
            :return: Tuple of (is_valid, reason_string).
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        telem = emu.get_telemetry()
        if not telem.motors_enabled:
            return (False, 'Motors disabled')
        if telem.estop_active:
            return (False, 'E-Stop active')
        is_left = telem.joints.theta2 < 0
        kin = self._service.get_kinematics()
        return kin.diagnose_reachability(pose, is_left)

    def handle_xy_click(self, x: float, y: float) -> None:
        '''
            Handles click on XY planar canvas.

            :param x: Target X in mm.
            :param y: Target Y in mm.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        new_pose = ScaraPose(x=x, y=y, z=curr.z, phi=curr.phi)
        ok, reason = self._diagnose_pose(new_pose)
        if not ok:
            curr_left = emu.get_telemetry().joints.theta2 < 0
            other_left = not curr_left
            kin = self._service.get_kinematics()
            ok_other, _ = kin.diagnose_reachability(new_pose, other_left)
            if ok_other:
                emu.set_elbow_mode(other_left)
                cmd = CommandFormatter.format_set_elbow(other_left)
                self._bridge.handle_manual_send(cmd)
                mode_str = 'Lefty' if other_left else 'Righty'
                self._log_host(f'[HOST]: Auto-switched to {mode_str} mode for target ({x:.1f}, {y:.1f})', 'info')
                ok = True

        if ok and emu.set_target_pose(new_pose, direct=False):
            self._bridge.send_hardware_move(new_pose)
        else:
            self._log_host(f'[HOST]: Target ({x:.1f}, {y:.1f}) unreachable: {reason}', 'err')
            if self._flash_unreachable is not None:
                self._flash_unreachable(x, y)

    def handle_z_click(self, z: float) -> None:
        '''
            Handles click on Z vertical canvas.

            :param z: Target Z in mm.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        new_pose = ScaraPose(x=curr.x, y=curr.y, z=z, phi=curr.phi)
        ok, reason = self._diagnose_pose(new_pose)
        if ok and emu.set_target_pose(new_pose, direct=False):
            self._bridge.send_hardware_move(new_pose)
        else:
            self._log_host(f'[HOST]: Elevation Z={z:.1f} unreachable: {reason}', 'err')

    def handle_jog(self, dx: float, dy: float, dz: float, dphi: float) -> None:
        '''
            Handles manual incremental jog displacement.

            :param dx: Delta X in mm.
            :param dy: Delta Y in mm.
            :param dz: Delta Z in mm.
            :param dphi: Delta Phi in radians.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        target = ScaraPose(
            x=curr.x + dx,
            y=curr.y + dy,
            z=curr.z + dz,
            phi=curr.phi + dphi
        )
        ok, reason = self._diagnose_pose(target)
        if ok and emu.set_target_pose(target, direct=False):
            self._bridge.send_hardware_move(target)
        else:
            self._log_host(f'[HOST]: Jog displacement unreachable: {reason}', 'err')

    def handle_home(self, axis: str) -> None:
        '''
            Handles homing motion for specified axis (planar XY or vertical Z).

            :param axis: Target axis ('xy' or 'z').
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        geom = self._service.get_kinematics().get_geometry()
        curr = emu.get_current_pose()

        if axis == 'xy':
            home_x: float = (geom.l1 + geom.l2) * 0.65
            target = ScaraPose(x=home_x, y=0.0, z=curr.z, phi=0.0)
        elif axis == 'z':
            home_z: float = geom.z_min + 20.0
            target = ScaraPose(x=curr.x, y=curr.y, z=home_z, phi=curr.phi)
        else:
            home_x = (geom.l1 + geom.l2) * 0.65
            home_z = geom.z_min + 20.0
            target = ScaraPose(x=home_x, y=0.0, z=home_z, phi=0.0)

        emu.set_target_pose(target, direct=False)
        self._bridge.send_hardware_move(target)

    def handle_toggle_elbow(self) -> None:
        '''
            Toggles between Lefty and Righty elbow configurations.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr_left = emu.get_telemetry().joints.theta2 < 0
        new_left = not curr_left
        emu.set_elbow_mode(new_left)
        cmd = CommandFormatter.format_set_elbow(new_left)
        self._bridge.handle_manual_send(cmd)
        mode_str = 'Lefty' if new_left else 'Righty'
        self._log_host(f'[HOST]: Switched to {mode_str} configuration', 'info')

    def handle_toggle_motors(self) -> None:
        '''
            Toggles motor driver power enable.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr_state = emu.get_telemetry().motors_enabled
        emu.set_motors_enabled(not curr_state)
        cmd = CommandFormatter.format_enable_motors() if not curr_state else CommandFormatter.format_disable_motors()
        self._bridge.handle_manual_send(cmd)

    def handle_estop(self) -> None:
        '''
            Executes emergency stop.

            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        emu.set_estop(True)
        self._bridge.clear_queue()
        self._bridge.handle_manual_send(CommandFormatter.format_estop())

    def handle_demo_select(self, demo_name: str) -> None:
        '''
            Generates and queues demo trajectory waypoints.

            :param demo_name: Demo trajectory identifier.
            :exceptions: None.
        '''
        emu = self._service.get_emulator()
        curr = emu.get_current_pose()
        poses = TrajectoryDemoGenerator.generate(demo_name, center_x=curr.x, center_y=curr.y, z=curr.z)

        if poses:
            emu.enqueue_trajectory(poses)
            self._bridge.enqueue_hardware_trajectory(poses)
