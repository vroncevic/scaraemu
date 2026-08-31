# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validator for CLI bundle instance.
'''

from __future__ import annotations

from collections.abc import Sequence
from ats_utilities.option.imanager import IOptionManager
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from scaraemu.infrastructure.cli.setup.bundle import CLIBundle
from scaraemu.core.service.iservice import IService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleValidator:
    '''
        Validator for the CLI bundle instance.

        It defines:

            :methods:
                | validate - Validates the CLI bundle instance.
                | is_valid - Checks if the CLI bundle instance is valid.
    '''

    @classmethod
    def validate(cls, bundle: CLIBundle) -> None:
        '''
            Validates the CLI bundle instance.

            :param bundle: The CLI bundle to be validated.
            :exceptions:
                | ATSValueError: The CLI bundle must be provided and have non-None attributes.
                | ATSTypeError: The CLI bundle attributes must match required interfaces.
        '''
        ctx: str = 'cli_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the CLI bundle must be provided'
        msg_bundle_istype: str = 'the CLI bundle must be an instance of CLIBundle'
        msg_service_none: str = 'the service must be provided'
        msg_parser_none: str = 'the parser must be provided'
        msg_commands_none: str = 'the commands must be provided'
        msg_service_istype: str = 'the service must be an instance of IService'
        msg_parser_istype: str = 'the parser must be an instance of IOptionManager'
        msg_commands_istype: str = 'the commands must be an instance of Sequence'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, CLIBundle, ctx, msg_bundle_istype)

        not_none(bundle.service, ctx, msg_service_none)
        not_none(bundle.parser, ctx, msg_parser_none)
        not_none(bundle.commands, ctx, msg_commands_none)

        istype(bundle.service, IService, ctx, msg_service_istype)
        istype(bundle.parser, IOptionManager, ctx, msg_parser_istype)
        istype(bundle.commands, Sequence, ctx, msg_commands_istype)

    @classmethod
    def is_valid(cls, bundle: CLIBundle) -> bool:
        '''
            Checks if the CLI bundle is valid.

            :param bundle: The CLI bundle to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True
        except (ATSValueError, ATSTypeError):
            return False
