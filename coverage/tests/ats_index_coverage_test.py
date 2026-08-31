# -*- coding: UTF-8 -*-

'''
Module
    ats_index_coverage_test.py
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
    Defines index coverage CSV update test cases.
'''

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ats_coverage import run_coverage, load_report, update_index_coverage
from tests.ats_base_test import ATSCoverageBaseTestCase

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSIndexCoverageTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSIndexCoverageTestCase with index coverage tests.
        Tests index coverage CSV updating and its error handling.

        It defines:

            :attributes: None.
            :methods:
                | test_update_index_coverage - Test index coverage CSV updating.
                | test_update_index_coverage_os_error - Test index coverage handling of OSError.
    '''

    def test_update_index_coverage(self) -> None:
        '''
            Test index coverage CSV updating.

            :exceptions: None.
        '''
        run_coverage("dummy_package")
        report_file = "dummy_package.json"
        report_data = load_report(report_file)

        report_data["files"]["/some/other/file.py"] = {
            "summary": {
                "num_statements": 10,
                "missing_lines": 0,
                "percent_covered_display": "100"
            }
        }

        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        csv_path = "docs/source/coverage_table.csv"

        update_index_coverage(report_data, csv_path=csv_path)
        self.assertTrue(Path(csv_path).exists())

        csv_content = Path(csv_path).read_text(encoding="utf-8")
        self.assertIn('"Name", "Stmts", "Miss", "Cover"', csv_content)
        self.assertIn('"dummy_package/__init__.py"', csv_content)
        self.assertIn('""', csv_content)

    def test_update_index_coverage_os_error(self) -> None:
        '''
            Test index coverage handling of OSError.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        update_index_coverage(
            {"files": {}, "totals": {"num_statements": "0", "missing_lines": "0", "percent_covered_display": "0"}},
            csv_path=str(docs_dir)
        )


if __name__ == '__main__':
    unittest.main()
