# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core scaraemu components for simplification of scaraemu bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.cli.icli import ICLI
from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.validator import SCARAEmuBundleValidator
from scaraemu.setup.keys import SCARAEmuBundleKeys
from scaraemu.setup.dependencies import SCARAEmuBundleDependencies
from scaraemu.setup.dep_validator import SCARAEmuBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAEmuBundleRegistry:
    '''
        Encapsulates core scaraemu components for simplification of scaraemu bundle.

        It defines:

            :methods:
                | create_bundle - Creates the scaraemu bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: SCARAEmuBundleDependencies) -> SCARAEmuBundle:
        '''
            Creates the scaraemu bundle.

            :param dependencies: The scaraemu bundle dependencies.
            :return: The scaraemu bundle.
            :exceptions:
                | ATSValueError: The dependencies or bundle must be provided and valid.
                | ATSTypeError: The dependencies or bundle attributes must match types.
        '''
        SCARAEmuBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle | None = dependencies.get(SCARAEmuBundleKeys.DEPENDENCY_BASE) if dependencies else None
        service: IService | None = dependencies.get(SCARAEmuBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        gui: IGUI | None = dependencies.get(SCARAEmuBundleKeys.DEPENDENCY_GUI) if dependencies else None
        transport: ITransport | None = dependencies.get(SCARAEmuBundleKeys.DEPENDENCY_TRANSPORT) if dependencies else None
        cli: ICLI | None = dependencies.get(SCARAEmuBundleKeys.DEPENDENCY_CLI) if dependencies else None

        bundle: SCARAEmuBundle = SCARAEmuBundle(
            base=base, service=service, gui=gui, transport=transport, cli=cli
        )
        SCARAEmuBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version string.
            :exceptions: None.
        '''
        return __version__
