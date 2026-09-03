# -*- coding: UTF-8 -*-

'''
Module
    test_protocol.py
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
    Unit tests for protocol parser and command formatter.
'''

from __future__ import annotations

import unittest
from scaraemu.core.model.scara_pose import ScaraPose
from scaraemu.infrastructure.communication.protocol.command_formatter import CommandFormatter
from scaraemu.infrastructure.communication.protocol.protocol_parser import ProtocolParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProtocol(unittest.TestCase):
    '''Unit test cases for protocol encoding and decoding.'''

    def test_command_formatting(self) -> None:
        '''Tests packet encoding for moves and control commands.'''
        pose = ScaraPose(x=150.25, y=-50.75, z=20.0, phi=0.5)
        pkt = CommandFormatter.format_move_pose(pose, speed=45.0)
        self.assertEqual(pkt, '<pt#150.25#-50.75#20.00#0.50#45.0#end>')

        self.assertEqual(CommandFormatter.format_enable_motors(), '<CMD:ENABLE>')
        self.assertEqual(CommandFormatter.format_disable_motors(), '<CMD:DISABLE>')
        self.assertEqual(CommandFormatter.format_estop(), '<CMD:ESTOP>')
        self.assertEqual(CommandFormatter.format_home(), '<CMD:HOME>')
        self.assertEqual(CommandFormatter.format_get_telemetry(), '<CMD:GET_TELEM>')
        self.assertEqual(CommandFormatter.format_get_position(), '<CMD:GETPOS>')
        self.assertEqual(CommandFormatter.format_get_status(), '<CMD:STATUS>')
        self.assertEqual(CommandFormatter.format_hold(), '<CMD:HOLD>')
        self.assertEqual(CommandFormatter.format_resume(), '<CMD:RESUME>')

    def test_telemetry_packet_parsing(self) -> None:
        '''Tests decoding incoming positional telemetry packet.'''
        raw = '<TELEM:1600#-800#400#200#IDLE>'
        resp = ProtocolParser.parse_line(raw)
        self.assertEqual(resp.response_type, 'TELEM')
        self.assertTrue(resp.is_success)
        self.assertIsNotNone(resp.payload)
        self.assertEqual(resp.payload['j1_steps'], 1600)
        self.assertEqual(resp.payload['j2_steps'], -800)
        self.assertEqual(resp.payload['z_steps'], 400)
        self.assertEqual(resp.payload['j4_steps'], 200)
        self.assertEqual(resp.payload['status'], 'IDLE')

    def test_kv_telemetry_packet_parsing(self) -> None:
        '''Tests decoding key-value hardware telemetry stream.'''
        raw = '<TELEM#X=269.03#Y=0.05#Z=0.22#PHI=0.00#J1=-154#J2=348#Z_STEP=86#J4=-48>'
        resp = ProtocolParser.parse_line(raw)
        self.assertEqual(resp.response_type, 'TELEM')
        self.assertTrue(resp.is_success)
        self.assertIsNotNone(resp.payload)
        self.assertAlmostEqual(float(resp.payload['x']), 269.03)
        self.assertAlmostEqual(float(resp.payload['y']), 0.05)
        self.assertAlmostEqual(float(resp.payload['z']), 0.22)
        self.assertAlmostEqual(float(resp.payload['phi']), 0.00)
        self.assertEqual(int(resp.payload['j1']), -154)

    def test_pos_and_status_packet_parsing(self) -> None:
        '''Tests decoding POS and STATUS query responses.'''
        pos_raw = '<POS#X=270.00#Y=0.00#Z=0.00#PHI=0.00#J1=0#J2=0#Z_STEP=0#J4=0>'
        resp = ProtocolParser.parse_line(pos_raw)
        self.assertEqual(resp.response_type, 'TELEM')
        self.assertTrue(resp.is_success)
        self.assertAlmostEqual(float(resp.payload['x']), 270.00)

        status_raw = '<STATUS#STATE=IDLE#BUSY=0#Q=0#X=270.00#Y=0.00#Z=0.00#PHI=0.00>'
        s_resp = ProtocolParser.parse_line(status_raw)
        self.assertEqual(s_resp.response_type, 'TELEM')
        self.assertTrue(s_resp.is_success)

    def test_resp_packet_parsing(self) -> None:
        '''Tests decoding structured firmware RESP packets.'''
        ack_resp = ProtocolParser.parse_line('<RESP:ACK#QUEUE=1>')
        self.assertEqual(ack_resp.response_type, 'ACK')
        self.assertTrue(ack_resp.is_success)

        done_resp = ProtocolParser.parse_line('<RESP:MOVE_DONE#X=180.00#Y=5.00#Z=20.00#PHI=0.00>')
        self.assertEqual(done_resp.response_type, 'MOVE_DONE')
        self.assertTrue(done_resp.is_success)
        self.assertAlmostEqual(float(done_resp.payload['x']), 180.0)
        self.assertAlmostEqual(float(done_resp.payload['y']), 5.0)

        homed_resp = ProtocolParser.parse_line('<RESP:HOMED_SUCCESS#X=175.50#Y=0.00#Z=20.00#PHI=0.00>')
        self.assertEqual(homed_resp.response_type, 'HOMED_SUCCESS')
        self.assertTrue(homed_resp.is_success)
        self.assertAlmostEqual(float(homed_resp.payload['x']), 175.5)

        hold_resp = ProtocolParser.parse_line('<RESP:ACK#FEED_HOLD_ACTIVE>')
        self.assertEqual(hold_resp.response_type, 'FEED_HOLD_ACTIVE')

        sing_resp = ProtocolParser.parse_line('<RESP:NACK_SINGULARITY_LIMIT>')
        self.assertEqual(sing_resp.response_type, 'NACK_SINGULARITY')
        self.assertFalse(sing_resp.is_success)

        nack_resp = ProtocolParser.parse_line('<RESP:NACK_BUFFER_FULL>')
        self.assertEqual(nack_resp.response_type, 'BUFFER_FULL')
        self.assertFalse(nack_resp.is_success)

    def test_ack_err_log_parsing(self) -> None:
        '''Tests decoding ACK, ERR, and general log lines.'''
        ack_resp = ProtocolParser.parse_line('<ACK:MOVE_STARTED>')
        self.assertEqual(ack_resp.response_type, 'ACK')
        self.assertTrue(ack_resp.is_success)

        err_resp = ProtocolParser.parse_line('<ERR:OUT_OF_BOUNDS>')
        self.assertEqual(err_resp.response_type, 'ERROR')
        self.assertFalse(err_resp.is_success)

        log_resp = ProtocolParser.parse_line('System initialized.')
        self.assertEqual(log_resp.response_type, 'LOG')
        self.assertTrue(log_resp.is_success)


if __name__ == '__main__':
    unittest.main()
