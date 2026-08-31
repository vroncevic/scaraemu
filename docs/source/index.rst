SCARA Robot Python Emulator & 2D/3D Kinematic Visualizer
---------------------------------------------------------

**scaraemu** is a standalone kinematic emulator, real-time 2D/3D visualizer, and hardware communication bridge for 4-DOF SCARA robotic manipulators.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|scaraemu python checker| |scaraemu python package| |scaraemu interface checker| |scaraemu isp checker| |scaraemu srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |scaraemu python checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml

.. |scaraemu python package| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package.yml

.. |scaraemu interface checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml

.. |scaraemu isp checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml

.. |scaraemu srp checker| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/scaraemu.svg
   :target: https://github.com/vroncevic/scaraemu/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/scaraemu.svg
   :target: https://github.com/vroncevic/scaraemu/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/scaraemu/badge/?version=latest
   :target: https://scaraemu.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|scaraemu python3 build|

.. |scaraemu python3 build| image:: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/scaraemu/releases

To install **scaraemu** type the following

.. code-block:: bash

    tar xvzf scaraemu-x.y.z.tar.gz
    cd scaraemu-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/scaraemu-*-py3-none-any.whl
    rm -f get-pip.py
    chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/scaraemu_run.py
    ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/scaraemu_run.py /usr/local/bin/scaraemu_run.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install scaraemu

📦 Dependencies
---------------

**scaraemu** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**scaraemu** is based on OOP and Hexagonal Architecture.

Tool structure

.. code-block:: bash

    scaraemu/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   ├── kinematics_config_dto.py
         │   │   ├── scara_geometry.py
         │   │   ├── scara_joints.py
         │   │   ├── scara_pose.py
         │   │   ├── scara_step_coords.py
         │   │   ├── simulation_state_dto.py
         │   │   └── telemetry_dto.py
         │   └── service/
         │       ├── demo_generator.py
         │       ├── emulator_service.py
         │       ├── engine.py
         │       ├── iemulator_service.py
         │       ├── ikinematics_service.py
         │       ├── __init__.py
         │       ├── iservice.py
         │       └── kinematics_service.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── emulator_command_definition.py
         │   │   ├── emulator_command_executor.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   └── __init__.py
         │   ├── communication/
         │   │   ├── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── command_formatter.py
         │   │   │   ├── command_templates.py
         │   │   │   ├── firmware_response_dto.py
         │   │   │   ├── __init__.py
         │   │   │   └── protocol_parser.py
         │   │   ├── serial_port_scanner.py
         │   │   └── transport/
         │   │       ├── __init__.py
         │   │       ├── itransport.py
         │   │       ├── serial_transport.py
         │   │       └── tcp_transport.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scaraemu.cfg
         │   │   ├── scaraemu.logo
         │   │   └── scheme.json
         │   └── gui/
         │       ├── canvas_xy.py
         │       ├── canvas_z.py
         │       ├── components/
         │       │   ├── __init__.py
         │       │   ├── jog_panel.py
         │       │   ├── serial_bar.py
         │       │   ├── serial_console_panel.py
         │       │   ├── telemetry_panel.py
         │       │   └── trajectory_demo_panel.py
         │       ├── engine.py
         │       ├── hardware_bridge_controller.py
         │       ├── icanvas_xy.py
         │       ├── icanvas_z.py
         │       ├── igui.py
         │       ├── __init__.py
         │       └── theme.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     15 directories, 79 files

✨ Features
-----------

* **2D Planar Dual-Link Visualizer**: Real-time rendering of primary ($L_1$) and secondary ($L_2$) arm links, active joint angles, target crosshair, and animated motion path trail.
* **Side Elevation Z-Tower View**: Multi-rod lead screw carriage elevation, active tool height, and radial extension profile visualization.
* **Interactive Targeting & Jogging**: Direct mouse click position targeting on both XY and Z canvases, Cartesian delta jogging ($X, Y, Z, \Phi$), Lefty/Righty elbow toggling, and Emergency Stop.
* **Autonomous Trajectory Demos**: Pre-programmed autonomous demonstration trajectories (Circle, Square, 5-Point Star, 3D Helical Coil).
* **Hardware Serial Bridge & Protocol Parser**: Bidirectional streaming over USB Serial (RP2040 micro-commands) with raw terminal telemetry log and manual command console.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, high test coverage, and 10.00 / 10.00 Pylint score.

📐 SCARA Kinematic & Geometric Configuration
--------------------------------------------

The robot dimensions and physical boundaries can be customized in ``scara_geometry.json`` or injected programmatically:

.. list-table:: Kinematic Limits
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Default Value
     - Description
   * - **l1**
     - ``150.0 mm``
     - Primary arm link length (shoulder to elbow).
   * - **l2**
     - ``120.0 mm``
     - Secondary arm link length (elbow to wrist).
   * - **r_min**
     - ``30.0 mm``
     - Inner singular deadzone radius (:math:`|L_1 - L_2|`).
   * - **r_max**
     - ``270.0 mm``
     - Maximum horizontal reach boundary (:math:`L_1 + L_2`).
   * - **z_min**
     - ``0.0 mm``
     - Minimum vertical height limit (bed level).
   * - **z_max**
     - ``100.0 mm``
     - Maximum vertical stroke limit.
   * - **min_speed**
     - ``1.0 mm/s``
     - Minimum allowable feedrate speed.
   * - **max_speed**
     - ``100.0 mm/s``
     - Maximum allowable safe feedrate speed.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install scaraemu

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/scaraemu/main/main.py

CLI Command Options
^^^^^^^^^^^^^^^^^^^

Launch the graphical emulator with default configuration:

.. code-block:: bash

    python3 main.py emulator

Launch with custom geometry overrides:

.. code-block:: bash

    python3 main.py emulator --l1 160.0 --l2 110.0 --verbose

.. list-table:: Emulator CLI Options
   :widths: 20 15 25 40
   :header-rows: 1

   * - Option
     - Type
     - Choices
     - Description
   * - **--l1**
     - ``float``
     - *Length in mm*
     - Override primary arm length L1 in millimeters.
   * - **--l2**
     - ``float``
     - *Length in mm*
     - Override secondary arm length L2 in millimeters.
   * - **--z-min**
     - ``float``
     - *Limit in mm*
     - Minimum vertical Z boundary in millimeters.
   * - **--z-max**
     - ``float``
     - *Limit in mm*
     - Maximum vertical Z boundary in millimeters.
   * - **--robot-config**
     - ``str``
     - *File path*
     - Path to custom robot geometry JSON file.
   * - **--verbose**
     - ``bool``
     - *Flag*
     - Enable verbose ATS operational logging.

Interactive Emulation & Control Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **2D/3D Kinematic Visualizer**:
   * Inspect top-down planar canvas (XY) and side elevation carriage (Z).
   * Directly click anywhere inside reachable annular workspace to command moves.
2. **Manual Jogging & Axis Control**:
   * Step along :math:`X, Y, Z, \Phi` with configurable step sizes under **Monitor & Jog**.
   * Toggle between Lefty and Righty elbow configurations or toggle motor power.
3. **Autonomous Demo Trajectories**:
   * Under the **Trajectories** tab, select **Circle**, **Square**, **5-Star**, or **3D Helix**.
   * Watch the real-time simulation interpolator render toolhead paths.
4. **Hardware Bridge & Telemetry Streaming**:
   * Connect to physical SCARA microcontroller via ``/dev/ttyACM0`` or TCP socket.
   * Telemetry updates synchronize live hardware position with the visualizer.
5. **Serial Command Console**:
   * Inspect incoming raw protocol packets (``<TELEM...>``, ``<RESP:...>``) and send custom commands.

📚 Docs
-------

More documentation and info at

* `scaraemu.readthedocs.io <https://scaraemu.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to scaraemu <https://github.com/vroncevic/scaraemu/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/scaraemu <https://vroncevic.github.io/scaraemu>`_

**scaraemu** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/
