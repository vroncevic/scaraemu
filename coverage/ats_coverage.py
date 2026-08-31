# -*- coding: UTF-8 -*-

'''
Module
    ats_coverage.py
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
    Defines attribute(s) and function(s) for coverage support.
'''

from __future__ import annotations

from sys import stdout, stderr, modules, argv, gettrace, settrace, exit as sys_exit
from pathlib import Path
from unittest import TestLoader, TestSuite, TextTestRunner

from coverage import Coverage

from ats_updater import (
    check_exists,
    load_report,
    update_readme,
    update_structure,
    update_index_coverage,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/ats_coverage'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__ = '5.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def _run_tests_and_collect(pro_name: str) -> None:
    '''
        Discovers and runs tests for the project.

        :param pro_name: Project name.
        :exceptions: None.
    '''
    modules.pop(pro_name, None)
    tests: TestSuite = TestLoader().discover('tests', pattern='*_test.py', top_level_dir='.')

    test_runner = TextTestRunner(verbosity=2)
    stdout.write('\n--- Test Report ---\n')
    test_runner.run(tests)


def run_coverage(pro_name: str) -> None:
    '''
        Runs coverage for project and generates reports in JSON and XML formats.

        :param pro_name: Project name (is equal to directory name).
        :exceptions:
            | TypeError:  The parameter pro_name type validation failed.
            | ValueError: The parameter pro_name format validation failed.
            | ValueError: The directory with name does not exist.
    '''
    is_dir = isinstance(pro_name, str) and Path(pro_name).is_dir()
    path_to_check = (
        pro_name if is_dir else f'{pro_name}.py'
        if isinstance(pro_name, str) else pro_name
    )
    check_exists(path_to_check, is_dir=is_dir)
    cov = Coverage(source=[pro_name], config_file='.coveragerc', data_file=f'.coverage.{pro_name}')

    old_trace = gettrace()

    stdout.write('\n--- Starting coverage ---\n')
    cov.start()

    _run_tests_and_collect(pro_name)

    cov.stop()
    cov.save()

    settrace(old_trace)

    stdout.write('\n--- Coverage Report ---\n')
    cov.report()
    stdout.write('\n--- JSON Report ---\n')
    cov.json_report(outfile=f'{pro_name}.json')
    stdout.write(f'\n--- JSON Report saved to {pro_name}.json ---\n')
    stdout.write('\n--- XML Report ---\n')
    cov.xml_report(outfile=f'{pro_name}.xml')
    stdout.write(f'\n--- XML Report saved to {pro_name}.xml ---\n')
    stdout.write('\n--- HTML Report ---\n')
    cov.html_report(directory='htmlcov')
    stdout.write('\n--- HTML Report saved to htmlcov ---\n')


def main() -> None:
    '''
        Main execution flow.

        :exceptions: None.
    '''
    try:
        if len(argv) < 2:
            stderr.write('Usage: ats_coverage <project_name>\n')
            sys_exit(128)

        project_name: str = argv[1]
        run_coverage(project_name)
        report_data: dict[str, object] = load_report(f'{project_name}.json')

        if report_data:
            update_readme(report_data)
            update_structure(project_name, 'README.md')
            update_index_coverage(report_data)
            update_structure(project_name, 'docs/source/index.rst')
            sys_exit(0)

        stderr.write('ats_coverage: failed to generate coverage report\n')
        sys_exit(129)

    except (ValueError, TypeError) as err:
        stderr.write(f'ats_coverage: {err}\n')
        sys_exit(128)


if __name__ == "__main__":
    main()
