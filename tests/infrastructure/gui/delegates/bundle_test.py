# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for GuiDelegatesBundle value object.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock

from scaraemu.infrastructure.gui.delegates.bundle import GuiDelegatesBundle
from scaraemu.infrastructure.gui.jog.action.idelegate import IJogActionDelegate
from scaraemu.infrastructure.gui.machine.configuration.idelegate import IConfigurationDelegate
from scaraemu.infrastructure.gui.machine.safety.idelegate import ISafetyDelegate
from scaraemu.infrastructure.gui.toolbar.action.idelegate import IActionDelegate as IToolbarActionDelegate
from scaraemu.infrastructure.gui.trajectory.preset.idelegate import ITrajectoryPresetDelegate
from scaraemu.infrastructure.gui.trajectory.queue.idelegate import IQueueActionDelegate
from scaraemu.infrastructure.gui.trajectory.script.idelegate import IScriptLoaderDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaraemu'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaraemu/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiDelegatesBundleTestCase(TestCase):
    '''
        Unit tests for GuiDelegatesBundle.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle attribute assignment.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle attribute assignment.

            :exceptions: None.
        '''
        jog = MagicMock(spec=IJogActionDelegate)
        config = MagicMock(spec=IConfigurationDelegate)
        safety = MagicMock(spec=ISafetyDelegate)
        preset = MagicMock(spec=ITrajectoryPresetDelegate)
        script = MagicMock(spec=IScriptLoaderDelegate)
        serial_bar = MagicMock(spec=IToolbarActionDelegate)
        queue = MagicMock(spec=IQueueActionDelegate)

        bundle = GuiDelegatesBundle(
            jog=jog,
            config=config,
            safety=safety,
            preset=preset,
            script=script,
            serial_bar=serial_bar,
            queue=queue,
        )

        self.assertIs(bundle.jog, jog)
        self.assertIs(bundle.config, config)
        self.assertIs(bundle.safety, safety)
        self.assertIs(bundle.preset, preset)
        self.assertIs(bundle.script, script)
        self.assertIs(bundle.serial_bar, serial_bar)
        self.assertIs(bundle.queue, queue)


if __name__ == '__main__':
    unittest_main()
