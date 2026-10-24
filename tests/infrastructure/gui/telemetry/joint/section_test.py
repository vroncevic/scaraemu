# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for JointSection subcomponent.
'''

from __future__ import annotations

from math import radians
from tkinter import TclError, Tk
from unittest import TestCase, main as unittest_main

from scaraemu.core.model.kinematics.joints import ScaraJoints
from scaraemu.infrastructure.gui.telemetry.joint.section import JointSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointSection(TestCase):
    '''
        Unit tests for JointSection.

        It defines:

            :methods:
                | setUp - Sets up root window for Tkinter widgets.
                | tearDown - Cleans up Tk root window.
                | test_section_and_update - Tests section creation, joints update, and version inquiry.
    '''

    def setUp(self) -> None:
        '''
            Sets up root window for Tkinter widgets.

            :exceptions: None.
        '''
        try:
            self._root = Tk()
        except TclError:
            self._root = None

    def tearDown(self) -> None:
        '''
            Cleans up Tk root window.

            :exceptions: None.
        '''
        if self._root is not None:
            self._root.destroy()

    def test_section_and_update(self) -> None:
        '''
            Tests section creation, joints update, and version inquiry.

            :exceptions: None.
        '''
        if self._root is None:
            self.skipTest('Tkinter display not available')

        section = JointSection(self._root)
        section.pack()

        self.assertEqual(section.get_version(), '1.0.2')

        joints = ScaraJoints(
            theta1=radians(30.0),
            theta2=radians(60.0),
            z=0.0,
            theta4=0.0,
            reachable=True,
        )
        section.update_joints(joints)

        readouts = section.get_readouts()
        self.assertEqual(readouts[0], '30.00°')
        self.assertEqual(readouts[1], '60.00°')
        self.assertEqual(readouts[2], '0.00°')


if __name__ == '__main__':
    unittest_main()
