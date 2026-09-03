# -*- coding: UTF-8 -*-

'''
Module
    opt_validator.py
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
    Validator for CLI bundle options.
'''

from __future__ import annotations

from collections.abc import Mapping
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from scaraemu.infrastructure.cli.setup.options import CLIBundleOptions
from scaraemu.infrastructure.cli.setup.keys import CLIBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleOptionsValidator:
    '''
        Validator for CLI bundle options.

        It defines:

            :methods:
                | validate - Validates the CLI bundle options.
                | is_valid - Checks if the CLI bundle options are valid.
    '''

    @classmethod
    def validate(cls, options: CLIBundleOptions) -> None:
        '''
            Validates the CLI bundle options.

            :param options: The CLI bundle options to be validated.
            :exceptions:
                | ATSValueError: The CLI bundle options must be provided.
                | ATSTypeError: The CLI bundle options must be a Mapping.
        '''
        ctx: str = 'cli_bundle_options_validator::validate(...)'
        msg_options_none: str = 'the CLI bundle options must be provided'
        msg_options_istype: str = 'the CLI bundle options must be a Mapping'

        not_none(options, ctx, msg_options_none)
        istype(options, Mapping, ctx, msg_options_istype)

        for attr_name, expected_type in CLIBundleKeys.get_option_to_type().items():
            if attr_name in options:
                msg_attr_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'
                attribute = options.get(attr_name)
                istype(attribute, expected_type, ctx, msg_attr_istype)

    @classmethod
    def is_valid(cls, options: CLIBundleOptions) -> bool:
        '''
            Checks if the CLI bundle options are valid.

            :param options: The CLI bundle options to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(options)
            return True
        except (ATSValueError, ATSTypeError):
            return False
