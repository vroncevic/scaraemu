#!/bin/bash
#
# @brief   scaraemu
# @version 1.0.0
# @date    Mon Aug 31 07:15:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py scaraemu
python3 gates/gates/isp_checker.py scaraemu
python3 gates/gates/limits_checker.py scaraemu
python3 gates/gates/srp_checker.py scaraemu

echo "Done"
