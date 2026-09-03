# -*- coding: UTF-8 -*-

'''
Module
    main.py
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
    Main entry point for SCARA Python Emulator and 2D/3D Kinematic Visualizer.
'''

from __future__ import annotations

from sys import exit as sys_exit

from scaraemu.engine import SCARAEmu
from scaraemu.setup.factory import SCARAEmuBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def main() -> bool:
    '''
        Bootstraps and runs SCARAEmu with required adapters and configuration.

        :return: True if successful, False otherwise.
        :exceptions: None.
    '''
    scaraemu: SCARAEmu = SCARAEmu(SCARAEmuBundleFactory.create_bundle())

    return scaraemu.process()


if __name__ == '__main__':
    '''
        Entry point for SCARAEmu execution.

        :exit code: 0 if successful, 1 otherwise.
        :exceptions: None.
    '''
    sys_exit(0 if main() else 1)
