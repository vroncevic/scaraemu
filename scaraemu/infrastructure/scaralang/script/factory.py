# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating ScriptLoaderAdapter instances.
'''

from __future__ import annotations

from scaralang.core.service.linter.factory import LinterFactory
from scaralang.infrastructure.parser.factory import DefaultParserFactory
from scaralang.core.service.compiler.plan.dependencies import PlanDependencies
from scaralang.core.service.compiler.plan.factory import PlanFactory
from scaralang.core.service.compiler.plan.provides import PlanProvides
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory

from scaraemu.infrastructure.scaralang.script.adapter import ScriptLoaderAdapter
from scaraemu.infrastructure.scaralang.script.iadapter import IScriptLoaderAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptLoaderAdapterFactory:
    '''
        Factory providing ScriptLoaderAdapter instances.

        It defines:

            :methods:
                | create - Builds an adapter wired with default scaralang compiler.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScriptLoaderAdapter:
        '''
            Builds and returns an adapter wired with default scaralang plan compiler.

            :return: Default IScriptLoaderAdapter instance.
            :exceptions: None.
        '''
        validator = DefaultValidationFactory.create().plan
        parser = DefaultParserFactory.create().parser
        linter = LinterFactory.create().linter
        plan_subsystem: PlanProvides = PlanFactory.create(
            dependencies=PlanDependencies(
                validator=validator,
                parser=parser,
                linter=linter,
            )
        )
        return ScriptLoaderAdapter(compiler=plan_subsystem.script_compiler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the component version string.

            :return: Semantic version string.
        '''
        return __version__
