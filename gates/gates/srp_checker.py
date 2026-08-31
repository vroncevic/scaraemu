# -*- coding: UTF-8 -*-

'''
Module
    srp_checker.py
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
    Defines attribute(s) and function(s) for QG - SRP check.
'''

from __future__ import annotations

from argparse import ArgumentParser
from ast import AsyncFunctionDef, ClassDef, Constant, Expr, FunctionDef, parse, walk
from logging import Logger, basicConfig, getLogger, StreamHandler, INFO
from os import walk as os_walk
from os.path import isdir, join
from sys import stdout, exit

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/quality-gates-py'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/quality-gates-py/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Development'


# Maximum methods allowed per class.
MAX_METHODS_PER_CLASS = 15

# Maximum logical lines allowed per method.
MAX_LOGICAL_LINES_PER_METHOD = 180


def count_logical_lines(method_node: FunctionDef | AsyncFunctionDef) -> int:
    '''
        Counts the actual logical lines of code in a method.
        Ignores docstrings, blank lines, and comments.

        :param method_node: The method node to count lines for.
        :return: The number of logical lines in the method.
        :exceptions: None.
    '''
    body = method_node.body

    if not body:
        return 0

    if isinstance(body[0], Expr) and isinstance(body[0].value, Constant):
        if isinstance(body[0].value.value, str):
            body = body[1:]

    if not body:
        return 0

    logical_lines = set()

    for stmt in body:
        for node in walk(stmt):
            if node is not stmt and isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef)):
                continue

            if hasattr(node, 'lineno'):
                logical_lines.add(node.lineno)

    return len(logical_lines)


def check_srp(package_dir: str, verbose: bool, logger: Logger) -> None:
    '''
        Check Single Responsibility Principle constraints.

        :param package_dir: Path to the python source code package (directory).
        :param verbose: Enable verbose output.
        :param logger: Logger instance.
        :exceptions: None.
    '''
    if not isdir(package_dir):
        logger.error(f"❌ Directory '{package_dir}' does not exist.")
        exit(1)

    errors: list[str] = []

    for root, _, files in os_walk(package_dir):
        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue
            
            path = join(root, file)

            if verbose:
                logger.info(f"Parsing SRP checks in: {path}")

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    tree = parse(f.read(), filename=path)

                for node in walk(tree):
                    if isinstance(node, ClassDef):
                        methods = [
                            n for n in node.body 
                            if isinstance(n, (FunctionDef, AsyncFunctionDef))
                        ]
                        
                        if len(methods) > MAX_METHODS_PER_CLASS:
                            errors.append(
                                f"❌ SRP Violation: Class '{node.name}' in '{path}' has {len(methods)} methods "
                                f"(Max allowed is {MAX_METHODS_PER_CLASS}). Split the class!"
                            )

                        for method in methods:
                            lines = count_logical_lines(method)
                            
                            if verbose:
                                logger.info(
                                    f"Method '{method.name}' in class '{node.name}' ('{path}') "
                                    f"has {lines} logical lines"
                                )
                                
                            if lines > MAX_LOGICAL_LINES_PER_METHOD:
                                errors.append(
                                    f"❌ SRP Violation: Method '{method.name}' in class '{node.name}' ('{path}') "
                                    f"is too long ({lines} logical lines, Max allowed is {MAX_LOGICAL_LINES_PER_METHOD})."
                                )
            except (OSError, SyntaxError) as e:
                errors.append(f"❌ Error parsing {path}: {e}")

    if errors:
        for err in errors:
            logger.error(err)

        logger.error("-" * 100)
        logger.error("Quality Gate Failed! Code violates SRP bounds.")
        exit(1)

    logger.info("-" * 100)
    logger.info("✅ Quality Gate Pass: SRP constraints are respected.")
    exit(0)


def main() -> None:
    '''
        Parse CLI arguments and trigger SRP verification.
    '''
    parser: ArgumentParser = ArgumentParser(
        description='Quality Gate: Verify Single Responsibility Principle constraints.',
        prog='quality-gate-py-srp-checker'
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

    check_srp(args.package_dir, args.verbose, logger)


if __name__ == '__main__':
    main()