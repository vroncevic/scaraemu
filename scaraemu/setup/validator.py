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
    Validator for the scaraemu bundle instance.
'''

from __future__ import annotations

from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.setup.keys import SCARAEmuBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAEmuBundleValidator:
    '''
        Validator for the scaraemu bundle instance.

        It defines:

            :methods:
                | validate - Validates the scaraemu bundle instance.
                | is_valid - Checks if the scaraemu bundle instance is valid.
    '''

    @classmethod
    def validate(cls, bundle: SCARAEmuBundle) -> None:
        '''
            Validates the scaraemu bundle instance.

            :param bundle: The scaraemu bundle to be validated.
            :exceptions:
                | ATSValueError: The scaraemu bundle must be provided and have non-None attributes.
                | ATSTypeError: The scaraemu bundle attributes must match required interfaces.
        '''
        ctx: str = 'scaraemu_bundle_validator::validate(...)'
        not_none(bundle, ctx, 'the scaraemu bundle must be provided')
        istype(bundle, SCARAEmuBundle, ctx, 'the scaraemu bundle must be an instance of SCARAEmuBundle')

        for attr_name, expected_type in SCARAEmuBundleKeys.get_dependency_to_type().items():
            attribute = getattr(bundle, attr_name, None)
            display_name: str = attr_name.replace('_', ' ')
            not_none(attribute, ctx, f'the {display_name} must be provided')
            istype(attribute, expected_type, ctx, f'the {display_name} must be an instance of {expected_type.__name__}')

    @classmethod
    def is_valid(cls, bundle: SCARAEmuBundle) -> bool:
        '''
            Checks if the scaraemu bundle is valid.

            :param bundle: The scaraemu bundle to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True

        except (ATSValueError, ATSTypeError):
            return False
