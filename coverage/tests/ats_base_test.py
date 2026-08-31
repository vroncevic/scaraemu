# -*- coding: UTF-8 -*-

'''
Module
    ats_base_test.py
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
    Defines base test case class for ats_coverage test suite.
'''

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


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

        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        self.pkg_dir = Path("dummy_package")
        self.pkg_dir.mkdir(parents=True, exist_ok=True)
        (self.pkg_dir / "__init__.py").write_text("def hello() -> str:\n    return 'world'\n", encoding="utf-8")
        (self.pkg_dir / "submodule.py").write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")
        
        self.pkg_subdir = self.pkg_dir / "subdir"
        self.pkg_subdir.mkdir(parents=True, exist_ok=True)
        (self.pkg_subdir / "file.py").write_text("def sub() -> None:\n    pass\n", encoding="utf-8")

        self.test_dir = Path("tests")
        self.test_dir.mkdir(parents=True, exist_ok=True)
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

        for name in list(sys.modules.keys()):
            if name.startswith("dummy_package") or "dummy_test" in name or name.startswith("ats_coverage"):
                sys.modules.pop(name, None)
            elif name == "tests" or name.startswith("tests."):
                sys.modules.pop(name, None)

        if self.temp_dir.name in sys.path:
            sys.path.remove(self.temp_dir.name)
