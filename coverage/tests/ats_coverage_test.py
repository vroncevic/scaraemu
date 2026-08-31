# -*- coding: UTF-8 -*-

'''
Module
    ats_coverage_test.py
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
    Defines test cases for ats_coverage.py.
Execute
    python3 -m unittest discover -s tests -p '*_test.py'
'''

import os
import sys
import tempfile
import subprocess
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from ats_updater import find_root_package, generate_tree_lines
from ats_coverage import (
    run_coverage,
    load_report,
    update_readme,
    update_structure,
    check_exists,
)

SCRIPT_PATH = str(Path(__file__).parent.parent / "ats_coverage.py")


class ATSCoverageBaseTestCase(unittest.TestCase):
    '''
        Defines class ATSCoverageBaseTestCase with setUp and tearDown.
        Base test case class providing temporary package structure setup.

        It defines:

            :attributes: None.
            :methods:
                | setUp - Set up temporary project structure before each test case.
                | tearDown - Clean up temporary project structure after each test case.
    '''

    def setUp(self) -> None:
        '''
            Set up temporary project structure before each test case.

            :exceptions: None.
        '''
        self.old_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

        sys.path.insert(0, self.temp_dir.name)

        for name, module in list(sys.modules.items()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        self.pkg_dir = Path("dummy_package")
        self.pkg_dir.mkdir()
        (self.pkg_dir / "__init__.py").write_text("def hello() -> str:\n    return 'world'\n", encoding="utf-8")
        (self.pkg_dir / "submodule.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")
        
        self.pkg_subdir = self.pkg_dir / "subdir"
        self.pkg_subdir.mkdir()
        (self.pkg_subdir / "file.py").write_text("def sub() -> None:\n    pass\n", encoding="utf-8")

        self.test_dir = Path("tests")
        self.test_dir.mkdir()
        (self.test_dir / "__init__.py").write_text("", encoding="utf-8")
        (self.test_dir / "dummy_test.py").write_text(
            "import unittest\n"
            "from dummy_package import hello\n"
            "from dummy_package.submodule import add\n\n"
            "class DummyTest(unittest.TestCase):\n"
            "    def test_hello(self):\n"
            "        self.assertEqual(hello(), 'world')\n"
            "    def test_add(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n",
            encoding="utf-8"
        )

        self.readme_content = (
            "# Dummy Project\n\n"
            "### Tool structure\n"
            "<details>\n"
            "<summary>Structure</summary>\n"
            "existing structure line 1\n"
            "existing structure line 2\n"
            "</details>\n\n"
            "### Code coverage\n"
            "<details>\n"
            "<summary>Coverage</summary>\n"
            "existing coverage line 1\n"
            "existing coverage line 2\n"
            "</details>\n\n"
            "### Docs\n"
        )
        self.readme_path = Path("README.md")
        self.readme_path.write_text(self.readme_content, encoding="utf-8")

    def tearDown(self) -> None:
        '''
            Clean up temporary project structure after each test case.

            :exceptions: None.
        '''
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

        for name, module in list(sys.modules.items()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        if self.temp_dir.name in sys.path:
            sys.path.remove(self.temp_dir.name)


class ATSCoverageCoreTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSCoverageCoreTestCase with core functional test cases.
        Tests base package discovery, loading, and directory tree generation.

        It defines:

            :attributes: None.
            :methods:
                | test_find_root_package - Test that find_root_package resolves the root package folder.
                | test_run_and_load_coverage - Test running coverage and loading the generated report.
                | test_generate_tree_lines_single_file - Test that generate_tree_lines handles non-directory paths by raising ValueError.
    '''

    def test_find_root_package(self) -> None:
        '''
            Test that find_root_package resolves the root package folder.

            :exceptions: None.
        '''
        submodule_path = str((self.pkg_dir / "submodule.py").resolve())
        root_package = find_root_package(submodule_path)
        self.assertIsNotNone(root_package)
        self.assertEqual(root_package.name, "dummy_package")

    def test_run_and_load_coverage(self) -> None:
        '''
            Test running coverage and loading the generated report.

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
        subprocess.run(["python3", SCRIPT_PATH, "dummy_package"], check=True)
        report_file = "dummy_package.json"
        self.assertTrue(Path(report_file).exists())

        report_data = load_report(report_file)
        self.assertIn("files", report_data)
        self.assertIn("totals", report_data)

    def test_generate_tree_lines_single_file(self) -> None:
        '''
            Test that generate_tree_lines handles non-directory paths by raising ValueError.

            :exceptions: None.
        '''
        file_path = "dummy_package/__init__.py"
        with self.assertRaises(ValueError):
            generate_tree_lines(file_path)


class ATSCoverageReadmeTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSCoverageReadmeTestCase with README updating test cases.
        Tests README.md and index.rst coverage table/structure updates.

        It defines:

            :attributes: None.
            :methods:
                | test_update_readme_and_structure - Test that README.md is updated correctly with coverage and structure.
                | test_update_readme_and_framework_structure - Test that README.md with Framework structure is updated correctly.
                | test_missing_readme_markers - Test that update functions skip gently if markers are missing.
                | test_update_readme_missing_file - Test that update_readme raises ValueError when README.md is missing.
                | test_update_structure_missing_file - Test that update_structure raises ValueError when README.md is missing.
                | test_update_readme_missing_tags - Test that update_readme skips when summary/details tags are missing.
                | test_update_structure_missing_tags - Test that update_structure skips when summary/details tags are missing.
    '''

    def test_update_readme_and_structure(self) -> None:
        '''
            Test that README.md is updated correctly with coverage and structure.

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
        subprocess.run(["python3", SCRIPT_PATH, "dummy_package"], check=True)
        report_file = "dummy_package.json"
        report_data = load_report(report_file)

        report_data["files"]["/some/other/file.py"] = {
            "summary": {
                "num_statements": 10,
                "missing_lines": 0,
                "percent_covered_display": "100"
            }
        }

        update_readme(report_data)
        update_structure("dummy_package")

        updated_readme = self.readme_path.read_text(encoding="utf-8")
        self.assertIn("| Name | Stmts | Miss | Cover |", updated_readme)
        self.assertIn("dummy_package/__init__.py", updated_readme)
        self.assertIn("file.py", updated_readme)
        self.assertIn("dummy_package/", updated_readme)
        self.assertIn("submodule.py", updated_readme)
        self.assertIn("subdir/", updated_readme)

    def test_update_readme_and_framework_structure(self) -> None:
        '''
            Test that README.md with Framework structure is updated correctly.

            :exceptions: None.
        '''
        framework_readme = (
            "# Dummy Framework Project\n\n"
            "### Framework structure\n"
            "<details>\n"
            "<summary>Structure</summary>\n"
            "</details>\n\n"
            "### Code coverage\n"
        )
        self.readme_path.write_text(framework_readme, encoding="utf-8")
        update_structure("dummy_package")

        updated_readme = self.readme_path.read_text(encoding="utf-8")
        self.assertIn("dummy_package/", updated_readme)
        self.assertIn("submodule.py", updated_readme)

    def test_missing_readme_markers(self) -> None:
        '''
            Test that update functions skip gently if markers are missing.

            :exceptions: None.
        '''
        self.readme_path.write_text("# Just a Title\n", encoding="utf-8")

        run_coverage("dummy_package")
        report_file = "dummy_package.json"
        report_data = load_report(report_file)

        update_readme(report_data)
        update_structure("dummy_package")

        updated_readme = self.readme_path.read_text(encoding="utf-8")
        self.assertEqual(updated_readme, "# Just a Title\n")

    def test_update_readme_missing_file(self) -> None:
        '''
            Test that update_readme raises ValueError when README.md is missing.

            :exceptions: None.
        '''
        self.readme_path.unlink()
        with self.assertRaises(ValueError):
            update_readme({"files": {}})

    def test_update_structure_missing_file(self) -> None:
        '''
            Test that update_structure raises ValueError when README.md is missing.

            :exceptions: None.
        '''
        self.readme_path.unlink()
        with self.assertRaises(ValueError):
            update_structure("dummy_package")

    def test_update_readme_missing_tags(self) -> None:
        '''
            Test that update_readme skips when summary/details tags are missing.

            :exceptions: None.
        '''
        self.readme_path.write_text("### Code coverage\n", encoding="utf-8")
        update_readme({"files": {}})

    def test_update_structure_missing_tags(self) -> None:
        '''
            Test that update_structure skips when summary/details tags are missing.

            :exceptions: None.
        '''
        self.readme_path.write_text("### Tool structure\n", encoding="utf-8")
        update_structure("dummy_package")


class ATSCoverageValidationTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSCoverageValidationTestCase with validation test cases.
        Tests type and value validation errors raised by ats_coverage.py functions.

        It defines:

            :attributes: None.
            :methods:
                | test_run_coverage_invalid_type - Test that run_coverage raises TypeError on invalid type.
                | test_run_coverage_missing_package - Test that run_coverage raises ValueError on missing package.
                | test_load_report_invalid_type - Test that load_report raises TypeError on invalid type.
                | test_load_report_missing_file - Test that load_report raises ValueError on missing file.
                | test_find_root_package_invalid_type - Test that find_root_package raises TypeError on invalid type.
                | test_update_readme_invalid_type - Test that update_readme raises TypeError on invalid type.
                | test_update_structure_invalid_type - Test that update_structure raises TypeError on invalid type.
                | test_generate_tree_lines_missing - Test that generate_tree_lines raises ValueError on missing file/folder.
                | test_check_exists_invalid_type - Test that check_exists raises TypeError on invalid type.
                | test_check_exists_empty_path - Test that check_exists raises ValueError on empty path.
                | test_check_exists_missing_dir - Test that check_exists raises ValueError on missing directory.
    '''

    def test_run_coverage_invalid_type(self) -> None:
        '''
            Test that run_coverage raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            run_coverage(123)

    def test_run_coverage_missing_package(self) -> None:
        '''
            Test that run_coverage raises ValueError on missing package.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            run_coverage("nonexistent_package")

    def test_load_report_invalid_type(self) -> None:
        '''
            Test that load_report raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            load_report(123)

    def test_load_report_missing_file(self) -> None:
        '''
            Test that load_report raises ValueError on missing file.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            load_report("nonexistent_file.json")

    def test_find_root_package_invalid_type(self) -> None:
        '''
            Test that find_root_package raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            find_root_package(123)

    def test_update_readme_invalid_type(self) -> None:
        '''
            Test that update_readme raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            update_readme(123)

    def test_update_structure_invalid_type(self) -> None:
        '''
            Test that update_structure raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            update_structure(123)

    def test_generate_tree_lines_missing(self) -> None:
        '''
            Test that generate_tree_lines raises ValueError on missing file/folder.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            generate_tree_lines("nonexistent_path")

    def test_check_exists_invalid_type(self) -> None:
        '''
            Test that check_exists raises TypeError on invalid type.

            :exceptions: None.
        '''
        with self.assertRaises(TypeError):
            check_exists(123)

    def test_check_exists_empty_path(self) -> None:
        '''
            Test that check_exists raises ValueError on empty path.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            check_exists("")

    def test_check_exists_missing_dir(self) -> None:
        '''
            Test that check_exists raises ValueError on missing directory.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            check_exists("nonexistent_dir", is_dir=True)


if __name__ == '__main__':
    unittest.main()
