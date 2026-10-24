# -*- coding: UTF-8 -*-

'''
Module
    iview_test.py
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
    Unit tests for ITelemetryView structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.core.model.simulation.telemetry import Telemetry
from scaraemu.infrastructure.gui.telemetry.iview import ITelemetryView


class _DummyTelemetryView:
    '''
        Dummy class conforming to ITelemetryView structurally.

        It defines:

            :methods:
                | update_telemetry - Updates displayed telemetry values.
                | get_version - Returns view interface version.
    '''

    def update_telemetry(self, telem: Telemetry) -> None:
        '''
            Updates displayed telemetry values.

            :param telem: Input telem.
            :exceptions: None.
        '''
        _ = telem

    def get_version(self) -> str:
        '''
            Returns view interface version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _InvalidTelemetryView:
    '''
        Dummy class missing required protocol methods.

        It defines:

            :methods:
                | reset - Resets telemetry view.
                | get_version - Returns view version.
    '''

    def reset(self) -> None:
        '''
            Resets telemetry view.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns view version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestITelemetryView(TestCase):
    '''
        Test cases verifying ITelemetryView structural protocol subtyping.

        It defines:

            :methods:
                | test_conforming_instance - Verifies dummy conforming class satisfies ITelemetryView structurally.
                | test_non_conforming_instance - Verifies non-conforming class does not satisfy ITelemetryView.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies dummy conforming class satisfies ITelemetryView structurally.

            :exceptions: None.
        '''
        view = _DummyTelemetryView()
        self.assertIsInstance(view, ITelemetryView)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming class does not satisfy ITelemetryView.

            :exceptions: None.
        '''
        invalid = _InvalidTelemetryView()
        self.assertNotIsInstance(invalid, ITelemetryView)


if __name__ == '__main__':
    unittest_main()
