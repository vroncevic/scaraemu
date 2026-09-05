# -*- coding: UTF-8 -*-

'''
Module
    limits_checker.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    quality-gates-py is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    quality-gates-py is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines attribute(s) and function(s) for QG - module limits check.
'''

from __future__ import annotations

from argparse import ArgumentParser
from logging import Logger, basicConfig, getLogger, StreamHandler, INFO
from os import walk
from os.path import isdir, join
from sys import stdout, exit

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/quality-gates-py'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/quality-gates-py/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Development'


# Maximum line length allowed for a single line in a module.
MAX_LINE_LENGTH = 150

# Maximum number of lines allowed for a single module.
MAX_MODULE_LINES = 500


def check_limits(package_dir: str, verbose: bool, logger: Logger) -> None:
    '''
        Check limits for modules in the python source code package.

        :param package_dir: Path to the python source code package (directory).
        :param verbose: Enable verbose output.
        :param logger: Logger instance.
        :exceptions: None.
    '''

    if not isdir(package_dir):
        logger.error(f"❌ Directory '{package_dir}' does not exist.")
        exit(1)

    errors: list[str] = []

    for root, _, file_names in walk(package_dir):
        for file_name in file_names:
            if not file_name.endswith('.py'):
                continue

            module_path: str = join(root, file_name)

            if verbose:
                logger.info(f"Checking module: {module_path}")

            try:
                with open(module_path, 'r', encoding='utf-8') as file:
                    module_lines: list[str] = file.readlines()

                module_line_count: int = len(module_lines)

                if verbose:
                    logger.info(f"Module line count: {module_line_count}")

                if module_line_count > MAX_MODULE_LINES:
                    errors.append(
                        f"❌ Module Line Count Violation: '{module_path}' has {module_line_count} lines "
                        f"(Max allowed is {MAX_MODULE_LINES})."
                    )

                for line_number, line_content in enumerate(module_lines, 1):
                    line_content_clean: str = line_content.rstrip('\r\n')

                    if len(line_content_clean) > MAX_LINE_LENGTH:
                        errors.append(
                            f"❌ Line Length Violation in '{module_path}' at line {line_number}: "
                            f"Length is {len(line_content_clean)} chars (Max allowed is {MAX_LINE_LENGTH})."
                        )

                        if verbose:
                            logger.info(f"Line {line_number} length: {len(line_content_clean)}")

            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"❌ Error reading file '{module_path}': {exc}")

    if errors:
        for err in errors:
            logger.error(err)

        logger.error("-" * 100)
        logger.error("Quality Gate Failed! Module size/line limits exceeded.")
        exit(1)

    logger.info("-" * 100)
    logger.info("✅ Quality Gate Pass: Module limits (lines & line lengths) are respected.")
    exit(0)


def main() -> None:
    '''
        Parse CLI arguments and trigger module limits verification.
    '''
    parser: ArgumentParser = ArgumentParser(
        description='Quality Gate: Verify line count and line length limits for Python modules.',
        prog='quality-gate-py-limits-checker'
    )

    parser.add_argument(
        'package_dir',
        type=str,
        help='Path to the target Python package directory'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    basicConfig(
        level=INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[StreamHandler(stdout)]
    )

    args = parser.parse_args()
    logger: Logger = getLogger(__name__)

    check_limits(args.package_dir, args.verbose, logger)


if __name__ == '__main__':
    main()
