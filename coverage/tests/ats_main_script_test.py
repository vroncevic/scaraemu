# -*- coding: UTF-8 -*-

'''
Module
    ats_main_script_test.py
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
    Defines main script entry point run tests.
'''

from __future__ import annotations

import sys
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch
from runpy import run_path

sys.path.append(str(Path(__file__).parent.parent))

from tests.ats_base_test import ATSCoverageBaseTestCase

SCRIPT_PATH = str(Path(__file__).parent.parent / "ats_coverage.py")

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSMainScriptTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSMainScriptTestCase with main script runner tests.
        Tests running the main script under success and failure scenarios.

        It defines:

            :attributes: None.
            :methods:
                | test_main_script_success - Test executing ats_coverage.py as __main__ with success.
                | test_main_script_failure_load_report - Test executing ats_coverage.py as __main__ with load report failure.
                | test_main_script_failure_run_coverage - Test executing ats_coverage.py as __main__ with run coverage raising TypeError.
                | test_main_script_success_run_path - Test executing ats_coverage.py as __main__ successfully via run_path.
    '''

    def test_main_script_success(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with success.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            ".. Tool structure\n"
            ".. details:: Structure\n"
            "existing rst line\n"
            ".. end details\n",
            encoding="utf-8"
        )
        res = subprocess.run(["python3", SCRIPT_PATH, "dummy_package"])
        self.assertEqual(res.returncode, 0)

    def test_main_script_failure_load_report(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with load report failure.

            :exceptions: None.
        '''
        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            ".. Tool structure\n"
            ".. details:: Structure\n"
            "existing rst line\n"
            ".. end details\n",
            encoding="utf-8"
        )
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with patch("ats_updater.load_report", return_value={}):
                with self.assertRaises(SystemExit) as cm:
                    run_path(SCRIPT_PATH, run_name="__main__")
                self.assertEqual(cm.exception.code, 129)

    def test_main_script_failure_run_coverage(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with run coverage raising TypeError.

            :exceptions: None.
        '''
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with patch("ats_coverage.run_coverage", side_effect=TypeError("Mocked error")):
                with self.assertRaises(SystemExit) as cm:
                    run_path(SCRIPT_PATH, run_name="__main__")
                self.assertEqual(cm.exception.code, 128)

    def test_main_script_success_run_path(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ successfully.

            :exceptions: None.
        '''
        readme_path = Path("README.md")
        readme_path.write_text(self.readme_content, encoding="utf-8")

        docs_dir = Path("docs/source")
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "index.rst").write_text(
            "Some header\n\n"
            "Tool structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n",
            encoding="utf-8"
        )
        with patch("sys.argv", ["ats_coverage.py", "dummy_package"]):
            with self.assertRaises(SystemExit) as cm:
                run_path(SCRIPT_PATH, run_name="__main__")
            self.assertEqual(cm.exception.code, 0)

    def test_main_script_failure_no_arguments(self) -> None:
        '''
            Test executing ats_coverage.py as __main__ with no arguments.

            :exceptions: None.
        '''
        with patch("sys.argv", ["ats_coverage.py"]):
            with self.assertRaises(SystemExit) as cm:
                run_path(SCRIPT_PATH, run_name="__main__")
            self.assertEqual(cm.exception.code, 128)


if __name__ == '__main__':
    unittest.main()

