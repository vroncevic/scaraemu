# -*- coding: UTF-8 -*-

'''
Module
    motion_completion_listener_test.py
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
    Unit tests for ServerMotionCompletionListener.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.core.service.emulation.notification.ilistener import IMotionCompletionListener
from scaraemu.infrastructure.scaralang.protocol.builder.iadapter import IBinaryResponseBuilderAdapter
from scaraemu.infrastructure.scaralang.protocol.codec.iadapter import IBinaryFrameCodecAdapter
from scaraemu.infrastructure.server.logger.ilistener import IServerLogListener
from scaraemu.infrastructure.server.motion_completion_listener import ServerMotionCompletionListener
from scaraemu.infrastructure.server.session.ioutbound_queue import IOutboundFrameQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServerMotionCompletionListener(TestCase):
    '''
        Test cases verifying ServerMotionCompletionListener behaviour.

        It defines:

            :methods:
                | test_interface_compliance - Verifies protocol adherence.
                | test_on_waypoint_completed_valid_seq - Verifies event building and push.
                | test_on_waypoint_completed_zero_seq - Verifies skipping when seq is 0.
                | test_get_version - Verifies version string.
    '''

    def test_interface_compliance(self) -> None:
        '''
            Verifies protocol adherence.

            :exceptions: None.
        '''
        listener = ServerMotionCompletionListener(
            outbound_queue=MagicMock(spec=IOutboundFrameQueue),
            response_builder=MagicMock(spec=IBinaryResponseBuilderAdapter),
            codec=MagicMock(spec=IBinaryFrameCodecAdapter),
            log_listener=MagicMock(spec=IServerLogListener),
        )
        self.assertIsInstance(listener, IMotionCompletionListener)

    def test_on_waypoint_completed_valid_seq(self) -> None:
        '''
            Verifies event building and queue push for valid seq_num.

            :exceptions: None.
        '''
        mock_queue = MagicMock(spec=IOutboundFrameQueue)
        mock_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        mock_log = MagicMock(spec=IServerLogListener)

        fake_frame = MagicMock()
        mock_builder.build_move_event.return_value = fake_frame
        mock_codec.pack_frame.return_value = b'packed_event'

        listener = ServerMotionCompletionListener(
            outbound_queue=mock_queue,
            response_builder=mock_builder,
            codec=mock_codec,
            log_listener=mock_log,
        )

        listener.on_waypoint_completed(5)

        mock_builder.build_move_event.assert_called_once_with(seq_num=5, event_type=2)
        mock_codec.pack_frame.assert_called_once_with(fake_frame)
        mock_queue.push.assert_called_once_with(b'packed_event')
        mock_log.on_server_log.assert_called_once_with(
            '🏁 [DT-SERVER]: Waypoint reached (seq=5)'
        )

    def test_on_waypoint_completed_zero_seq(self) -> None:
        '''
            Verifies skipping when seq_num is 0.

            :exceptions: None.
        '''
        mock_queue = MagicMock(spec=IOutboundFrameQueue)
        mock_builder = MagicMock(spec=IBinaryResponseBuilderAdapter)
        mock_codec = MagicMock(spec=IBinaryFrameCodecAdapter)
        mock_log = MagicMock(spec=IServerLogListener)

        listener = ServerMotionCompletionListener(
            outbound_queue=mock_queue,
            response_builder=mock_builder,
            codec=mock_codec,
            log_listener=mock_log,
        )

        listener.on_waypoint_completed(0)

        mock_builder.build_move_event.assert_not_called()
        mock_codec.pack_frame.assert_not_called()
        mock_queue.push.assert_not_called()
        mock_log.on_server_log.assert_not_called()

    def test_get_version(self) -> None:
        '''
            Verifies version string.

            :exceptions: None.
        '''
        listener = ServerMotionCompletionListener(
            outbound_queue=MagicMock(spec=IOutboundFrameQueue),
            response_builder=MagicMock(spec=IBinaryResponseBuilderAdapter),
            codec=MagicMock(spec=IBinaryFrameCodecAdapter),
            log_listener=MagicMock(spec=IServerLogListener),
        )
        self.assertEqual(listener.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
