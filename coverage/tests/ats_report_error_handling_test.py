# -*- coding: UTF-8 -*-

'''
Module
    ats_report_error_handling_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    ats_coverage is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    ats_coverage is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines report loading and readme update error handling test cases.
'''

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent))

from ats_coverage import load_report, update_readme
from tests.ats_base_test import ATSCoverageBaseTestCase

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSReportErrorHandlingTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSReportErrorHandlingTestCase with error handling tests.
        Tests load report and readme update handling of OSError.

        It defines:

            :attributes: None.
            :methods:
                | test_load_report_os_error - Test load report handling of OSError.
                | test_update_readme_os_error - Test update readme handling of OSError.
    '''

    def test_load_report_os_error(self) -> None:
        '''
            Test load report handling of OSError.

            :exceptions: None.
        '''
        dummy_file = Path("dummy_file.json")
        dummy_file.write_text("{}", encoding="utf-8")
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            result = load_report(str(dummy_file))
            self.assertEqual(result, {})

    def test_update_readme_os_error(self) -> None:
        '''
            Test update readme handling of OSError.

            :exceptions: None.
        '''
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            update_readme({"files": {}})


if __name__ == '__main__':
    unittest.main()
