# -*- coding: UTF-8 -*-

'''
Module
    ats_tree_generation_test.py
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
    Defines tree generation and project structure update test cases.
'''

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent))

from ats_updater import generate_tree_lines
from ats_coverage import update_structure
from tests.ats_base_test import ATSCoverageBaseTestCase

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '5.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSTreeGenerationTestCase(ATSCoverageBaseTestCase):
    '''
        Defines class ATSTreeGenerationTestCase with tree generation tests.
        Tests single file trees and RST structure updates.

        It defines:

            :attributes: None.
            :methods:
                | test_generate_tree_lines_single_file_success - Test tree generation with single file.
                | test_generate_tree_lines_single_file_non_dir - Test tree generation with single file when not a directory.
                | test_update_structure_rst - Test update structure with RST file format.
                | test_update_structure_rst_framework - Test update structure with RST framework structure.
                | test_update_structure_read_os_error - Test update structure read handling of OSError.
                | test_update_structure_write_os_error - Test update structure write handling of OSError.
    '''

    def test_generate_tree_lines_single_file_success(self) -> None:
        '''
            Test tree generation with single file.

            :exceptions: None.
        '''
        dummy_dir = Path("dummy_dir")
        dummy_dir.mkdir(parents=True, exist_ok=True)
        (dummy_dir / "dummy_file.py").write_text("def hello(): pass", encoding="utf-8")
        lines, dirs, files = generate_tree_lines("dummy_dir")
        self.assertEqual(lines, ["    dummy_dir/\n", "         └── dummy_file.py\n"])
        self.assertEqual(dirs, 1)
        self.assertEqual(files, 1)

    def test_generate_tree_lines_single_file_non_dir(self) -> None:
        '''
            Test tree generation with single file when not a directory.

            :exceptions: None.
        '''
        file_path = Path("dummy_file.py")
        file_path.write_text("def hello(): pass", encoding="utf-8")
        lines, dirs, files = generate_tree_lines("dummy_file")
        self.assertEqual(lines, ["    dummy_file.py\n"])
        self.assertEqual(dirs, 0)
        self.assertEqual(files, 1)

    def test_update_structure_rst(self) -> None:
        '''
            Test update structure with RST file format.

            :exceptions: None.
        '''
        rst_path = Path("index.rst")
        rst_content = (
            "Some header\n\n"
            "Tool structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n"
        )
        rst_path.write_text(rst_content, encoding="utf-8")
        update_structure("dummy_package", "index.rst")

        updated_rst = rst_path.read_text(encoding="utf-8")
        self.assertIn("dummy_package/", updated_rst)
        self.assertIn("Next Section", updated_rst)

    def test_update_structure_rst_framework(self) -> None:
        '''
            Test update structure with RST framework structure.

            :exceptions: None.
        '''
        rst_path = Path("index.rst")
        rst_content = (
            "Some header\n\n"
            "Framework structure\n"
            ".. code-block:: bash\n\n"
            "     existing structure\n\n"
            "Next Section\n"
        )
        rst_path.write_text(rst_content, encoding="utf-8")
        update_structure("dummy_package", "index.rst")

        updated_rst = rst_path.read_text(encoding="utf-8")
        self.assertIn("dummy_package/", updated_rst)
        self.assertIn("Next Section", updated_rst)

    def test_update_structure_read_os_error(self) -> None:
        '''
            Test update structure read handling of OSError.

            :exceptions: None.
        '''
        with patch("builtins.open", side_effect=OSError("Mocked read error")):
            update_structure("dummy_package")

    def test_update_structure_write_os_error(self) -> None:
        '''
            Test update structure write handling of OSError.

            :exceptions: None.
        '''
        original_open = open
        def mock_open_func(file, mode='r', *args, **kwargs):
            if 'w' in mode:
                raise OSError("Mocked write error")
            return original_open(file, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=mock_open_func):
            update_structure("dummy_package")


if __name__ == '__main__':
    unittest.main()
