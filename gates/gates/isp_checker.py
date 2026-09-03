# -*- coding: UTF-8 -*-

'''
Module
    isp_checker.py
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
    Defines attribute(s) and function(s) for QG - ISP check.
'''

from __future__ import annotations

from argparse import ArgumentParser
from ast import AsyncFunctionDef, Attribute, ClassDef, FunctionDef, Name, parse, walk
from logging import Logger, basicConfig, getLogger, StreamHandler, INFO
from os import walk as os_walk
from os.path import isdir, join
from sys import stdout, exit

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/quality-gates-py'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/quality-gates-py/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Development'


# Maximum abstract methods allowed for a single interface.
MAX_ABSTRACT_METHODS = 9


def count_abstract_methods(class_node: ClassDef) -> int:
    '''
        Count methods within a class that have the abstractmethod decorator.

        :param class_node: The class AST node to check.
        :return: The count of abstract methods.
        :exceptions: None.
    '''
    count = 0

    for node in class_node.body:
        if isinstance(node, (FunctionDef, AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, Name) and decorator.id == 'abstractmethod':
                    count += 1
                elif isinstance(decorator, Attribute) and decorator.attr == 'abstractmethod':
                    count += 1

    return count


def check_isp(package_dir: str, verbose: bool, logger: Logger) -> None:
    '''
        Check Interface Segregation Principle constraints.

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
        if 'exceptions' in root:
            continue

        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue

            path = join(root, file)

            if verbose:
                logger.info(f"Parsing ISP checks in: {path}")

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    tree = parse(f.read(), filename=path)

                for node in walk(tree):
                    if isinstance(node, ClassDef):
                        is_interface_class = (
                            (node.name.startswith('I') and len(node.name) > 1 and node.name[1].isupper()) or
                            (file.startswith('i') and len(file) > 1 and file[1].isupper())
                        )

                        if is_interface_class:
                            method_count = count_abstract_methods(node)

                            if verbose:
                                logger.info(
                                    f"Interface '{node.name}' has {method_count} abstract methods "
                                    f"(Max allowed is {MAX_ABSTRACT_METHODS})"
                                )

                            if method_count > MAX_ABSTRACT_METHODS:
                                errors.append(
                                    f"❌ ISP Violation: Interface '{node.name}' in '{path}' "
                                    f"defines {method_count} abstract methods (Max allowed is {MAX_ABSTRACT_METHODS}). "
                                    f"Segregate this interface!"
                                )

            except (OSError, SyntaxError) as e:
                errors.append(f"❌ Error parsing {path}: {e}")

    if errors:
        for err in errors:
            logger.error(err)

        logger.error("-" * 100)
        logger.error("Quality Gate Failed! Fat interfaces detected based on abstract method count.")
        exit(1)

    logger.info("-" * 100)
    logger.info("✅ Quality Gate Pass: Interface Segregation Principle constraints are respected.")
    exit(0)


def main() -> None:
    '''
        Parse CLI arguments and trigger ISP verification.
    '''
    parser: ArgumentParser = ArgumentParser(
        description='Quality Gate: Verify Interface Segregation Principle constraints.',
        prog='quality-gate-py-isp-checker'
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

    check_isp(args.package_dir, args.verbose, logger)


if __name__ == '__main__':
    main()
