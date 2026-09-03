# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    CLIBundleDependencies TypedDict definition.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import TypedDict

from ats_utilities.option.imanager import IOptionManager

from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.command.command import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleDependencies(TypedDict, total=False):
    '''
        CLI bundle dependencies specification.

        It defines:

            :attributes:
                | service - The service interface instance.
                | parser - The option parser interface instance.
                | commands - Sequence of registered command bundles.
    '''

    service: IService
    parser: IOptionManager
    commands: Sequence[CommandBundle]
