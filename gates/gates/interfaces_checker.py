# -*- coding: UTF-8 -*-

'''
Module
    interfaces_checker.py
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
    Defines attribute(s) and function(s) for QG - Protocol interface check.
'''

from __future__ import annotations

from argparse import ArgumentParser
from ast import (
    AST, AsyncFunctionDef, Attribute, Call, ClassDef,
    FunctionDef, Name, Subscript, parse, walk
)
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


def get_base_name(node: AST) -> str | None:
    '''
        Extracts the base class name regardless of generics (Subscript) or attributes.

        :param node: The AST node to check.
        :return: The base name of the class if found, otherwise None.
        :exceptions: None.
    '''
    if isinstance(node, Subscript):
        return get_base_name(node.value)
    if isinstance(node, Name):
        return node.id
    elif isinstance(node, Attribute):
        return node.attr

    return None


def is_dataclass(class_node: ClassDef) -> bool:
    '''
        Checks if the class is decorated with @dataclass.

        :param class_node: The class AST node to check.
        :return: True if the class is a dataclass, otherwise False.
        :exceptions: None.
    '''
    for decorator in class_node.decorator_list:
        if isinstance(decorator, Name) and decorator.id == 'dataclass':
            return True
        elif isinstance(decorator, Call) and isinstance(decorator.func, Name) and decorator.func.id == 'dataclass':
            return True

    return False


def inherits_from(class_node: ClassDef, exception_names: set[str]) -> bool:
    '''
        Checks if the class inherits from any of the base classes from the allowed/ignored list.

        :param class_node: The class AST node to check.
        :param exception_names: Set of base class names to ignore.
        :return: True if the class inherits from any ignored base, otherwise False.
        :exceptions: None.
    '''
    for base in class_node.bases:
        name = get_base_name(base)

        if name in exception_names:
            return True

    return False


def extract_methods_and_properties(class_node: ClassDef) -> set[str]:
    '''
        Extracts names of all methods and properties defined within the class.

        :param class_node: The class AST node.
        :return: Set of method and property names.
        :exceptions: None.
    '''
    members = set()
    for item in class_node.body:
        if isinstance(item, (FunctionDef, AsyncFunctionDef)):
            members.add(item.name)
    return members


def check_interfaces(package_dir: str, verbose: bool, logger: Logger) -> None:
    '''
        Check that concrete classes correctly implement structural protocols.

        :param package_dir: Path to the python source code package (directory).
        :param verbose: Enable verbose output.
        :param logger: Logger instance.
        :exceptions: None.
    '''
    if not isdir(package_dir):
        logger.error(f"❌ Directory '{package_dir}' does not exist.")
        exit(1)

    errors: list[str] = []
    defined_protocols: dict[str, set[str]] = {}

    ignored_bases: set[str] = {
        'Exception', 'BaseException', 'ValueError', 'TypeError', 'KeyError', 
        'AttributeError', 'LookupError', 'RuntimeError', 'int', 'str', 'dict', 
        'list', 'set', 'tuple', 'bytes', 'object', 

        'TypedDict', 'Protocol', 'Generic', 'NamedTuple', 'ABC', 'ABCMeta',

        'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag', 
        'ArgumentParser', 'Action', 'Formatter',

        'Thread', 'Process', 'Task', 'Future',
    }

    # 1. Discover all defined protocols/interfaces starting with 'I'
    for root, _, files in os_walk(package_dir):
        if 'exceptions' in root:
            continue

        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue

            path = join(root, file)

            if verbose:
                logger.info(f"Parsing protocol definitions in: {path}")

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    tree = parse(f.read(), filename=path)

                for node in walk(tree):
                    if isinstance(node, ClassDef):
                        if node.name.startswith('I') and len(node.name) > 1 and node.name[1].isupper():
                            methods = extract_methods_and_properties(node)
                            defined_protocols[node.name] = methods

                            if verbose:
                                logger.info(f"Discovered protocol {node.name} with methods: {methods}")

            except (OSError, SyntaxError) as e:
                errors.append(f"❌ Error parsing {path}: {e}")

    # 2. Verify concrete classes satisfy protocols
    for root, _, files in os_walk(package_dir):
        if 'exceptions' in root:
            continue

        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue

            path = join(root, file)

            if file.startswith('i') and len(file) > 1 and file[1].isupper():
                continue

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    tree = parse(f.read(), filename=path)

                for node in walk(tree):
                    if not isinstance(node, ClassDef):
                        continue

                    if node.name.startswith('I') and len(node.name) > 1 and node.name[1].isupper():
                        continue

                    if is_dataclass(node) or inherits_from(node, ignored_bases):
                        continue

                    class_methods = extract_methods_and_properties(node)
                    expected_protocol_name = f"I{node.name}"

                    if expected_protocol_name in defined_protocols:
                        required_methods = defined_protocols[expected_protocol_name]
                        missing_methods = required_methods - class_methods

                        if verbose:
                            logger.info(f"Checking class '{node.name}' against protocol '{expected_protocol_name}'")

                        if missing_methods:
                            errors.append(
                                f"❌ Class '{node.name}' in '{path}' does not satisfy Protocol '{expected_protocol_name}'. "
                                f"Missing methods/properties: {missing_methods}"
                            )
                    else:
                        pass

            except (OSError, SyntaxError) as e:
                errors.append(f"❌ Error parsing {path}: {e}")

    if errors:
        for err in errors:
            logger.error(err)

        logger.error("-" * 100)
        logger.error("Quality Gate Failed! Concrete class does not satisfy Protocol requirements.")
        exit(1)

    logger.info("-" * 100)
    logger.info("✅ Quality Gate Pass: All structural protocols are correctly implemented by concrete classes.")
    exit(0)


def main() -> None:
    '''
        Parse CLI arguments and trigger interface verification.
    '''
    parser: ArgumentParser = ArgumentParser(
        description='Quality Gate: Verify that concrete classes satisfy protocol requirements.',
        prog='quality-gate-py-interfaces-checker'
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

    check_interfaces(args.package_dir, args.verbose, logger)


if __name__ == '__main__':
    main()
