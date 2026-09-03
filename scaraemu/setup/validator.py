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

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from scaraemu.setup.bundle import SCARAEmuBundle
from scaraemu.core.service.iservice import IService
from scaraemu.infrastructure.communication.transport.itransport import ITransport
from scaraemu.infrastructure.gui.igui import IGUI
from scaraemu.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
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
        msg_bundle_none: str = 'the scaraemu bundle must be provided'
        msg_bundle_istype: str = 'the scaraemu bundle must be an instance of SCARAEmuBundle'
        msg_base_none: str = 'the base bundle must be provided'
        msg_service_none: str = 'the service must be provided'
        msg_gui_none: str = 'the gui must be provided'
        msg_transport_none: str = 'the transport must be provided'
        msg_cli_none: str = 'the cli must be provided'
        msg_base_istype: str = 'the base bundle must be an instance of BaseBundle'
        msg_service_istype: str = 'the service must be an instance of IService'
        msg_gui_istype: str = 'the gui must be an instance of IGUI'
        msg_transport_istype: str = 'the transport must be an instance of ITransport'
        msg_cli_istype: str = 'the cli must be an instance of ICLI'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, SCARAEmuBundle, ctx, msg_bundle_istype)

        not_none(bundle.base, ctx, msg_base_none)
        not_none(bundle.service, ctx, msg_service_none)
        not_none(bundle.gui, ctx, msg_gui_none)
        not_none(bundle.transport, ctx, msg_transport_none)
        not_none(bundle.cli, ctx, msg_cli_none)

        istype(bundle.base, BaseBundle, ctx, msg_base_istype)
        istype(bundle.service, IService, ctx, msg_service_istype)
        istype(bundle.gui, IGUI, ctx, msg_gui_istype)
        istype(bundle.transport, ITransport, ctx, msg_transport_istype)
        istype(bundle.cli, ICLI, ctx, msg_cli_istype)

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
