# -*- coding: UTF-8 -*-

'''
Module
    ats_coverage_execution_test.py
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
    Defines coverage execution and test runner collection test cases.
'''

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent))

from ats_coverage import run_coverage, _run_tests_and_collect
from tests.ats_base_test import ATSCoverageBaseTestCase

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSCoverageExecutionTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSCoverageExecutionTestCase with coverage execution tests.
        Tests run_coverage and _run_tests_and_collect helper functions.

        It defines:

            :attributes: None.
            :methods:
                | test_run_tests_and_collect - Test _run_tests_and_collect helper function.
                | test_run_coverage_mocked - Test run_coverage with mocked Coverage class.
    '''

    def test_run_tests_and_collect(self) -> None:
        '''
            Test _run_tests_and_collect helper function.

            :exceptions: None.
        '''
        _run_tests_and_collect("dummy_package")

    def test_run_coverage_mocked(self) -> None:
        '''
            Test run_coverage with mocked Coverage class.

            :exceptions: None.
        '''
        import ats_coverage

        with patch("ats_coverage.check_exists") as mock_check, \
             patch("ats_coverage.Coverage") as mock_cov, \
             patch("ats_coverage._run_tests_and_collect") as mock_run:
            
            mock_instance = MagicMock()
            mock_cov.return_value = mock_instance

            ats_coverage.run_coverage("dummy_package")

            mock_check.assert_called_once()
            mock_cov.assert_called_once_with(
                source=["dummy_package"],
                config_file=".coveragerc",
                data_file=".coverage.dummy_package"
            )
            mock_instance.start.assert_called_once()
            mock_run.assert_called_once_with("dummy_package")
            mock_instance.stop.assert_called_once()
            mock_instance.save.assert_called_once()
            mock_instance.report.assert_called_once()
            mock_instance.json_report.assert_called_once_with(outfile="dummy_package.json")
            mock_instance.xml_report.assert_called_once_with(outfile="dummy_package.xml")
            mock_instance.html_report.assert_called_once_with(directory="htmlcov")


if __name__ == '__main__':
    unittest.main()
