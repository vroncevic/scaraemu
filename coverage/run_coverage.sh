#!/bin/bash
#
# @brief   ats_coverage
# @version 5.0.0
# @date    Fri Aug 14 18:07:30 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 ats_coverage.py ats_coverage
pylint ats_coverage.py > ats_coverage.report
echo "Done"
