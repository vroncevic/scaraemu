# -*- coding: UTF-8 -*-

'''
Module
    protocol_parser.py
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
    Parser decoding raw serial lines from SCARA microcontroller firmware.
'''

from __future__ import annotations

import re
from typing import ClassVar

from scaraemu.infrastructure.communication.protocol.firmware_response_dto import FirmwareResponseDTO

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolParser:
    '''
        Parser for serial communication protocols between SCARA host and firmware.

        It defines:

            :attributes:
                | TELEM_PATTERN - Regex pattern for positional telemetry packets.
                | ACK_PATTERN - Regex pattern for ACK response packets.
                | ERR_PATTERN - Regex pattern for ERROR response packets.
            :methods:
                | parse_line - Decodes a single raw serial text line into a structured DTO.
                | _parse_kv_telem - Decodes key-value telemetry packet.
                | _parse_resp - Decodes RESP response packet.
    '''

    TELEM_PATTERN: ClassVar[re.Pattern] = re.compile(
        r'<TELEM:([-\d.]+)#([-\d.]+)#([-\d.]+)#([-\d.]+)#([A-Za-z0-9_]+)>'
    )
    ACK_PATTERN: ClassVar[re.Pattern] = re.compile(r'<ACK:(.*)>')
    ERR_PATTERN: ClassVar[re.Pattern] = re.compile(r'<ERR:(.*)>')

    @classmethod
    def _parse_kv_telem(cls, clean_line: str) -> FirmwareResponseDTO:
        '''
            Decodes key-value telemetry packet.

            :param clean_line: Cleaned input line string.
            :return: Decoded FirmwareResponseDTO.
            :exceptions: None.
        '''
        payload: dict[str, object] = {}
        inner: str = clean_line[1:-1] if clean_line.startswith('<') and clean_line.endswith('>') else clean_line
        parts: list[str] = inner.split('#')[1:]
        for part in parts:
            if '=' in part:
                k, v = part.split('=', 1)
                k_lower: str = k.strip().lower()
                try:
                    payload[k_lower] = float(v.strip())
                except ValueError:
                    payload[k_lower] = v.strip()

        return FirmwareResponseDTO(
            raw_line=clean_line,
            response_type='TELEM',
            is_success=True,
            payload=payload
        )

    @classmethod
    def _parse_resp(cls, clean_line: str) -> FirmwareResponseDTO:
        '''
            Decodes RESP response packet.

            :param clean_line: Cleaned input line string.
            :return: Decoded FirmwareResponseDTO.
            :exceptions: None.
        '''
        inner: str = clean_line.strip('<>')
        resp_body: str = inner[5:] if inner.startswith('RESP:') else inner
        parts: list[str] = resp_body.split('#')
        primary_token: str = parts[0] if parts else ''
        secondary_token: str = parts[1] if len(parts) > 1 else ''

        match (primary_token, secondary_token):
            case ('MOVE_DONE', _):
                resp_type: str = 'MOVE_DONE'
            case ('MOVE_FAILED', _):
                resp_type = 'MOVE_FAILED'
            case ('MOVE_START', _):
                resp_type = 'MOVE_START'
            case ('HOMED_SUCCESS', _):
                resp_type = 'HOMED_SUCCESS'
            case ('HOMING_IN_PROGRESS', _):
                resp_type = 'HOMING_IN_PROGRESS'
            case ('HOMING_FAILED', _):
                resp_type = 'HOMING_FAILED'
            case ('FEED_HOLD_ACTIVE', _) | ('ACK', 'FEED_HOLD_ACTIVE'):
                resp_type = 'FEED_HOLD_ACTIVE'
            case ('MOTION_RESUMED', _) | ('ACK', 'MOTION_RESUMED'):
                resp_type = 'MOTION_RESUMED'
            case ('NACK_SINGULARITY_LIMIT', _):
                resp_type = 'NACK_SINGULARITY'
            case ('NACK_JOINT_LIMIT', _):
                resp_type = 'NACK_JOINT_LIMIT'
            case ('NACK_Z_OUT_OF_BOUNDS', _):
                resp_type = 'NACK_Z_LIMIT'
            case ('NACK_PATH_CROSSES_DEADZONE', _):
                resp_type = 'NACK_PATH_CROSSES_DEADZONE'
            case ('ELBOW', _):
                resp_type = 'ELBOW'
            case ('ACK', _) if 'ELBOW' in secondary_token:
                resp_type = 'ELBOW'
            case (tok, _) if 'BUFFER_FULL' in tok:
                resp_type = 'BUFFER_FULL'
            case (tok, _) if 'NACK' in tok:
                resp_type = 'NACK'
            case _:
                resp_type = 'ACK'

        payload: dict[str, object] = {'message': clean_line}
        for part in parts:
            if '=' in part:
                k, v = part.split('=', 1)
                k_lower: str = k.strip().lower()
                try:
                    payload[k_lower] = float(v.strip())
                except ValueError:
                    payload[k_lower] = v.strip()

        if 'queue' in payload and isinstance(payload['queue'], (int, float)):
            payload['queue_depth'] = int(payload['queue'])

        is_nack: bool = (
            'NACK' in clean_line
            or 'BUFFER_FULL' in clean_line
            or resp_type in ('HOMING_FAILED', 'MOVE_FAILED')
        )

        return FirmwareResponseDTO(
            raw_line=clean_line,
            response_type=resp_type,
            is_success=not is_nack,
            payload=payload
        )

    @classmethod
    def parse_line(cls, line: str) -> FirmwareResponseDTO:
        '''
            Decodes a single raw serial text line into a structured FirmwareResponseDTO.

            :param line: Raw serial input string.
            :return: FirmwareResponseDTO representation.
            :exceptions: None.
        '''
        clean_line: str = line.strip()

        if clean_line.startswith(('<TELEM#', '<POS#', '<STATUS#')):
            return cls._parse_kv_telem(clean_line)

        if clean_line.startswith('<RESP:'):
            return cls._parse_resp(clean_line)

        telem_match = cls.TELEM_PATTERN.search(clean_line)
        if telem_match:
            try:
                return FirmwareResponseDTO(
                    raw_line=clean_line,
                    response_type='TELEM',
                    is_success=True,
                    payload={
                        'j1_steps': round(float(telem_match.group(1))),
                        'j2_steps': round(float(telem_match.group(2))),
                        'z_steps': round(float(telem_match.group(3))),
                        'j4_steps': round(float(telem_match.group(4))),
                        'status': telem_match.group(5)
                    }
                )
            except (ValueError, IndexError):
                pass

        err_match = cls.ERR_PATTERN.search(clean_line)
        if err_match:
            return FirmwareResponseDTO(
                raw_line=clean_line,
                response_type='ERROR',
                is_success=False,
                payload={'message': err_match.group(1)}
            )

        ack_match = cls.ACK_PATTERN.search(clean_line)
        if ack_match:
            return FirmwareResponseDTO(
                raw_line=clean_line,
                response_type='ACK',
                is_success=True,
                payload={'message': ack_match.group(1)}
            )

        return FirmwareResponseDTO(
            raw_line=clean_line,
            response_type='LOG',
            is_success=True,
            payload={'message': clean_line}
        )
