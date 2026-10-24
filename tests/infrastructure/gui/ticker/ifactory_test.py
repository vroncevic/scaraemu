# -*- coding: UTF-8 -*-

'''
Module
    ifactory_test.py
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
    Unit tests for ISimulationTickerFactory protocol.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.ticker.dependencies import SimulationTickerDependencies
from scaraemu.infrastructure.gui.ticker.ifactory import ISimulationTickerFactory
from scaraemu.infrastructure.gui.ticker.iticker import ISimulationTicker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class _ConformingFactory:
    '''
        Mock conforming to ISimulationTickerFactory protocol.

        It defines:

            :methods:
                | create - Creates an ISimulationTicker.
                | get_version - Returns version string.
    '''

    def create(
        self,
        dependencies: SimulationTickerDependencies,
    ) -> ISimulationTicker:
        '''
            Creates an ISimulationTicker.

            :param dependencies: Parameter bundle.
            :return: Mock simulation ticker.
            :exceptions: None.
        '''
        _ = dependencies
        mock_ticker = MagicMock(spec=ISimulationTicker)
        return mock_ticker

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class _NonConformingFactory:
    '''
        Mock non-conforming to ISimulationTickerFactory protocol.

        It defines:

            :methods:
                | reset - Dummy reset method.
                | get_version - Returns version string.
    '''

    def reset(self) -> None:
        '''
            Dummy reset method.

            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.2'


class TestISimulationTickerFactory(TestCase):
    '''
        Unit tests for ISimulationTickerFactory structural protocol verification.

        It defines:

            :methods:
                | test_structural_conformance - Verifies conforming class satisfies protocol.
                | test_non_conforming_rejection - Verifies non-conforming class fails protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies conforming class satisfies protocol.

            :exceptions: None.
        '''
        factory = _ConformingFactory()
        self.assertIsInstance(factory, ISimulationTickerFactory)

    def test_non_conforming_rejection(self) -> None:
        '''
            Verifies non-conforming class fails protocol.

            :exceptions: None.
        '''
        non_conforming = _NonConformingFactory()
        self.assertNotIsInstance(non_conforming, ISimulationTickerFactory)


if __name__ == '__main__':
    unittest_main()
