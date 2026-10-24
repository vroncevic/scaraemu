# -*- coding: UTF-8 -*-

'''
Module
    services.py
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
    Parameter bundle dataclass encapsulating backend and infrastructure services for GUI assembly.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaracom.transport.itransport import ITransport
from scaracom.transport.scanner.iport_scanner import IPortScanner

from scaraemu.core.service.emulation.controller.icontroller import IEmulationController
from scaraemu.core.service.emulation.queue.iqueue import IEmulationQueue
from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.preferences.provides import PreferencesProvides
from scaraemu.infrastructure.scaralang.provides import ScaralangProvides
from scaraemu.infrastructure.server.provides import ServerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class GuiServicesBundle:
    '''
        Immutable parameter bundle encapsulating backend and infrastructure services for GUI assembly.

        It defines:

            :attributes:
                | transport - Hardware communication transport.
                | kinematics - Forward and inverse kinematics calculation service.
                | emulation_service - Manipulator digital twin emulation and integration service.
                | emulation_controller - Manipulator mode and safety controller port.
                | emulation_queue - Motion trajectory waypoint queue port.
                | server - Virtual manipulator server provides container.
                | preferences - Preferences repository provides container.
                | scaralang - ScaraLang compiler, geometry, and protocol adapters provides container.
                | port_scanner - Hardware serial port discovery scanner.
    '''

    transport: ITransport
    kinematics: IManipulatorKinematics
    emulation_service: IEmulationService
    emulation_controller: IEmulationController
    emulation_queue: IEmulationQueue
    server: ServerProvides
    preferences: PreferencesProvides
    scaralang: ScaralangProvides
    port_scanner: IPortScanner
