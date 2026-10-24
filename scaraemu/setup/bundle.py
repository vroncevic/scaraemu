# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines SCARAEmuBundle container holding application components.
'''

from __future__ import annotations

from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scaraemu.core.service.emulation.iservice import IEmulationService
from scaraemu.core.service.kinematics.imanipulator import IManipulatorKinematics
from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class SCARAEmuBundle:
    '''
        Container holding all primary application components for SCARAEmu.

        It defines:

            :attributes:
                | base - Base ATS bundle with logger, options, and info managers.
                | bounds - ScaraBounds kinematics boundary model.
                | kinematics - IManipulatorKinematics kinematics solver.
                | emulation_service - IEmulationService digital twin emulation service.
                | gui - GUI presentation adapter.
                | cli - Command-line interface adapter.
    '''

    base: BaseBundle
    bounds: ScaraBounds
    kinematics: IManipulatorKinematics
    emulation_service: IEmulationService
    gui: IGUI
    cli: ICLI
