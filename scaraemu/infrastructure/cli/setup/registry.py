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
    Encapsulates core CLI components for simplification of CLI bundle.
'''

from __future__ import annotations

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager

from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.command.command import CommandBundle
from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.infrastructure.cli.setup.validator import CLIBundleValidator
from scaraemu.infrastructure.cli.setup.keys import CLIBundleKeys
from scaraemu.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scaraemu.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleRegistry:
    '''
        Encapsulates core CLI components for simplification of CLI bundle.

        It defines:

            :methods:
                | create_bundle - Creates the CLI bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: CLIBundleDependencies) -> CLIBundle:
        '''
            Creates the CLI bundle.

            :param dependencies: The CLI bundle dependencies.
            :return: The CLI bundle.
            :exceptions:
                | ATSValueError: The dependencies or bundle must be provided and valid.
                | ATSTypeError: The dependencies or bundle attributes must match types.
        '''
        CLIBundleDependenciesValidator.validate(dependencies)

        service: IService | None = dependencies.get(CLIBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        parser: IOptionManager | None = dependencies.get(CLIBundleKeys.DEPENDENCY_PARSER) if dependencies else None
        commands: Sequence[CommandBundle] | None = (
            dependencies.get(CLIBundleKeys.DEPENDENCY_COMMANDS) if dependencies else None
        )

        bundle: CLIBundle = CLIBundle(service=service, parser=parser, commands=commands)
        CLIBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version string.
            :exceptions: None.
        '''
        return __version__
