# -*- coding: UTF-8 -*-

'''
Module
    iprovider_test.py
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
    Unit tests for IJogStepProvider protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main

from scaraemu.infrastructure.gui.jog.step.iprovider import IJogStepProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _DummyJogStepProvider:
    '''
        Dummy provider for protocol conformance verification.
    '''

    def __init__(self, step: float = 5.0) -> None:
        '''
            Initializes dummy step provider.

            :param step: Step displacement in mm.
            :exceptions: None.
        '''
        self._step = step

    def get_step(self) -> float:
        '''
            Returns active step distance in mm.

            :return: Step size in mm.
            :exceptions: None.
        '''
        return self._step

    def get_version(self) -> str:
        '''
            Returns provider version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestJogStepProvider(TestCase):
    '''
        Test cases verifying IJogStepProvider protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy provider satisfies IJogStepProvider protocol.
                | test_step_query - Verifies step querying and version inquiry.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies dummy provider satisfies IJogStepProvider protocol.

            :exceptions: None.
        '''
        provider = _DummyJogStepProvider()
        self.assertIsInstance(provider, IJogStepProvider)

    def test_step_query(self) -> None:
        '''
            Verifies step querying and version inquiry.

            :exceptions: None.
        '''
        provider = _DummyJogStepProvider(step=10.0)
        self.assertEqual(provider.get_step(), 10.0)
        self.assertEqual(provider.get_version(), '1.0.2')


if __name__ == '__main__':
    unittest_main()
