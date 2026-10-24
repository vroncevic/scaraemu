# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating TrajectoryDemoAdapter instances.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.discretization.factory import DiscretizationFactory
from scaralang.core.service.trajectory.discretization.provides import DiscretizationProvides

from scaraemu.infrastructure.scaralang.demo.adapter import TrajectoryDemoAdapter
from scaraemu.infrastructure.scaralang.demo.iadapter import ITrajectoryDemoAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryDemoAdapterFactory:
    '''
        Factory providing configured ITrajectoryDemoAdapter instances.

        It defines:

            :methods:
                | create - Builds adapter with default scaralang discretizers.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(cls) -> ITrajectoryDemoAdapter:
        '''
            Builds and returns an ITrajectoryDemoAdapter instance.

            :return: ITrajectoryDemoAdapter instance.
            :exceptions: None.
        '''
        provides: DiscretizationProvides = DiscretizationFactory.create()
        return TrajectoryDemoAdapter(provides.circle, provides.rectangle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
