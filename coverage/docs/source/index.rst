Generate code coverage and update README.md
---------------------------------------------

**ats_coverage** is toolset for generation of code coverage and update README.md.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|ats_coverage python checker| |ats_coverage python package| |github issues| |documentation status| |github contributors|

.. |ats_coverage python checker| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python_checker.yml

.. |ats_coverage python package| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_package.yml

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/ats_coverage.svg
   :target: https://github.com/vroncevic/ats_coverage/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/ats_coverage.svg
   :target: https://github.com/vroncevic/ats_coverage/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/ats_coverage/badge/?version=latest
   :target: https://ats-coverage.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
-----------------

|ats_coverage python3 build|

.. |ats_coverage python3 build| image:: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/ats_coverage/actions/workflows/ats_coverage_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/ats_coverage/releases

To install **ats_coverage** type the following

.. code-block:: bash

    tar xvzf ats_coverage-x.y.z.tar.gz
    cd ats_coverage-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/ats_coverage-*-py3-none-any.whl
    rm -f get-pip.py
    chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/ats_coverage_run.py
    ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/ats_coverage_run.py /usr/local/bin/ats_coverage_run.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # pyton3
    pip3 install ats_coverage

📦 Dependencies
-----------------

**ats_coverage** requires next modules and libraries

* `coverage - Code coverage measurement for Python <https://pypi.org/project/coverage/>`_
* `pathlib - Object-oriented filesystem paths <https://pypi.org/project/pathlib/>`_


📁 Tool structure
-------------------

**ats_coverage** is based on OOP.

Tool structure

.. code-block:: bash

    ats_coverage.py

     0 directories, 1 files

Copyright and licence
-----------------------

|license: gpl v3| |license: apache 2.0|

.. |license: gpl v3| image:: https://img.shields.io/badge/license-gplv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |license: apache 2.0| image:: https://img.shields.io/badge/license-apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2.0

Copyright (C) 2024 - 2026 by `vroncevic.github.io/ats_coverage <https://vroncevic.github.io/ats_coverage>`_

**ats_coverage** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/ats_coverage/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_us/i/btn/btn_donatecc_lg.gif
   :target: https://www.python.org/psf/donations/

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
