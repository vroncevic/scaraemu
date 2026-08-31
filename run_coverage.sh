#!/bin/bash
#
# @brief   scaraemu
# @version 1.0.0
# @date    Mon Aug 31 07:15:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py scaraemu
pylint scaraemu > scaraemu.report
echo "Done"
