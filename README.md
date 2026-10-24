# SCARA Robot Python Emulator & 2D/3D Kinematic Visualizer

<img align="right" src="https://raw.githubusercontent.com/vroncevic/scaraemu/dev/docs/scaraemu_logo.png" width="25%">

**scaraemu** is a standalone kinematic emulator, real-time 2D/3D visualizer, and hardware communication bridge for 4-DOF SCARA robotic manipulators.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![scaraemu python checker](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python_checker.yml) [![scaraemu python package](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package_checker.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_package.yml) [![scaraemu interface checker](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_interface_checker.yml) [![scaraemu isp checker](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_isp_checker.yml) [![scaraemu srp checker](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/scaraemu.svg)](https://github.com/vroncevic/scaraemu/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/scaraemu.svg)](https://github.com/vroncevic/scaraemu/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
    - [🌐 SCARA Ecosystem Role & Physical Hardware Simulation](#-scara-ecosystem-role--physical-hardware-simulation)
  - [✨ Features](#-features)
  - [📐 SCARA Kinematic & Geometric Configuration](#-scara-kinematic--geometric-configuration)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Command Options](#cli-command-options)
    - [Interactive Emulation & Control Workflow](#interactive-emulation--control-workflow)
    - [🤖 Digital Twin Integration with SCARAjectory](#-digital-twin-integration-with-scarajectory)
      - [Method 1: Virtual Robot Server (TCP 127.0.0.1:8888)](#method-1-virtual-robot-server-tcp-1270018888)
      - [Method 2: Launch via CLI with Initial File](#method-2-launch-via-cli-with-initial-file)
      - [Method 3: Load `.scara` DSL Programs from UI](#method-3-load-scara-dsl-programs-from-ui)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/scaraemu/dev/docs/debtux.png)

[![scaraemu python3 build](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml/badge.svg)](https://github.com/vroncevic/scaraemu/actions/workflows/scaraemu_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**scaraemu** is located at **[pypi.org](https://pypi.org/project/scaraemu/)**.

You can install by using pip

```bash
# python3
pip3 install scaraemu
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/scaraemu/releases/)** download and extract release archive.

To install **scaraemu** type the following

```bash
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
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/scaraemu/releases)** download and extract release archive.

To install **scaraemu** locate and run setup.py with arguments

```bash
tar xvzf scaraemu-x.y.z.tar.gz
cd scaraemu-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**scaraemu** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
* [pyserial - Python Serial Port Extension](https://pypi.org/project/pyserial/) [![License: BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### 📁 Tool structure

**scaraemu** is based on OOP and Hexagonal Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    scaraemu/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── joints.py
         │   │   │   ├── pose.py
         │   │   │   └── step_coords.py
         │   │   └── simulation/
         │   │       ├── __init__.py
         │   │       ├── state.py
         │   │       └── telemetry.py
         │   └── service/
         │       ├── emulation/
         │       │   ├── controller/
         │       │   │   ├── controller.py
         │       │   │   ├── flags.py
         │       │   │   ├── icontroller.py
         │       │   │   └── __init__.py
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── iservice.py
         │       │   ├── motion/
         │       │   │   ├── __init__.py
         │       │   │   └── stepper.py
         │       │   ├── notification/
         │       │   │   ├── ilistener.py
         │       │   │   ├── __init__.py
         │       │   │   ├── inotifier.py
         │       │   │   └── notifier.py
         │       │   ├── provides.py
         │       │   ├── queue/
         │       │   │   ├── __init__.py
         │       │   │   ├── iqueue.py
         │       │   │   ├── queue.py
         │       │   │   └── snapshot.py
         │       │   └── service.py
         │       ├── __init__.py
         │       └── kinematics/
         │           ├── imanipulator.py
         │           └── __init__.py
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
         │   │   ├── bundle.py
         │   │   ├── definition.py
         │   │   ├── executor.py
         │   │   ├── idefinition.py
         │   │   ├── iexecutor.py
         │   │   └── __init__.py
         │   ├── config/
         │   │   ├── scara_geometry.json
         │   │   ├── scara_geometry_scheme.json
         │   │   ├── scaraemu.cfg
         │   │   └── scaraemu.logo
         │   ├── connection/
         │   │   ├── command/
         │   │   │   ├── dependencies.py
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── idispatcher.py
         │   │   │   └── __init__.py
         │   │   ├── coordinator/
         │   │   │   ├── coordinator.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── icoordinator.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── handler/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── handler.py
         │   │   │   ├── ihandler.py
         │   │   │   └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── listener/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── listener.py
         │   │   └── provides.py
         │   ├── dependencies.py
         │   ├── factory.py
         │   ├── gui/
         │   │   ├── bridge/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── log/
         │   │   │   │   ├── adapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── provides.py
         │   │   │   ├── server/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── log_adapter.py
         │   │   │   │   └── state_adapter.py
         │   │   │   ├── status/
         │   │   │   │   ├── adapter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── sync/
         │   │   │       ├── __init__.py
         │   │   │       ├── isynchronizer.py
         │   │   │       └── synchronizer.py
         │   │   ├── canvas/
         │   │   │   ├── canvas_xy.py
         │   │   │   ├── canvas_z.py
         │   │   │   ├── config.py
         │   │   │   ├── icanvas_xy.py
         │   │   │   ├── icanvas_z.py
         │   │   │   ├── __init__.py
         │   │   │   ├── renderer/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── j1_boundary_renderer.py
         │   │   │   │   ├── manipulator_arm_renderer.py
         │   │   │   │   ├── manipulator_render_context.py
         │   │   │   │   ├── trail_renderer.py
         │   │   │   │   ├── trajectory_path_renderer.py
         │   │   │   │   ├── workspace_boundary_renderer.py
         │   │   │   │   ├── z_render_context.py
         │   │   │   │   └── z_renderer.py
         │   │   │   ├── target/
         │   │   │   │   ├── elbow_auto_switch_coordinator.py
         │   │   │   │   ├── elbow_dependencies.py
         │   │   │   │   ├── ielbow_auto_switch_coordinator.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── itarget_click_listener.py
         │   │   │   │   ├── itarget_motion_dispatcher.py
         │   │   │   │   ├── target_action_coordinator.py
         │   │   │   │   ├── target_dependencies.py
         │   │   │   │   └── target_motion_dispatcher.py
         │   │   │   └── viewport/
         │   │   │       ├── coordinate_transformer.py
         │   │   │       ├── icoordinate_transformer.py
         │   │   │       ├── __init__.py
         │   │   │       ├── iviewport.py
         │   │   │       ├── viewport.py
         │   │   │       └── z_coordinate_mapper.py
         │   │   ├── console/
         │   │   │   ├── buffer_actions.py
         │   │   │   ├── ilog_listener.py
         │   │   │   ├── __init__.py
         │   │   │   └── panel.py
         │   │   ├── delegates/
         │   │   │   ├── assembly.py
         │   │   │   ├── bundle.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── engine.py
         │   │   ├── factory.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── jog/
         │   │   │   ├── action/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── dpad/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   └── step/
         │   │   │       ├── __init__.py
         │   │   │       ├── iprovider.py
         │   │   │       └── section.py
         │   │   ├── layout/
         │   │   │   ├── builder/
         │   │   │   │   ├── builder.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── ibuilder.py
         │   │   │   │   └── __init__.py
         │   │   │   └── __init__.py
         │   │   ├── lifecycle/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── irunner.py
         │   │   │   └── runner.py
         │   │   ├── machine/
         │   │   │   ├── configuration/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   └── safety/
         │   │   │       ├── coordinator.py
         │   │   │       ├── idelegate.py
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── provides.py
         │   │   ├── services.py
         │   │   ├── splash/
         │   │   │   ├── factory.py
         │   │   │   ├── ifactory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iscreen.py
         │   │   │   └── screen.py
         │   │   ├── telemetry/
         │   │   │   ├── cartesian/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iview.py
         │   │   │   ├── joint/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── panel.py
         │   │   │   └── step/
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── theme/
         │   │   │   ├── __init__.py
         │   │   │   ├── style.py
         │   │   │   └── theme.py
         │   │   ├── ticker/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── ifactory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iticker.py
         │   │   │   ├── observer/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iobserver.py
         │   │   │   │   └── observer.py
         │   │   │   ├── scheduler/
         │   │   │   │   ├── ilistener.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── ischeduler.py
         │   │   │   │   └── scheduler.py
         │   │   │   └── ticker.py
         │   │   ├── toolbar/
         │   │   │   ├── action/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── connection/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── istatus_view.py
         │   │   │   │   └── section.py
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   ├── port/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iprovider.py
         │   │   │   │   └── section.py
         │   │   │   └── server/
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   ├── trajectory/
         │   │   │   ├── __init__.py
         │   │   │   ├── panel.py
         │   │   │   ├── preset/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── section.py
         │   │   │   ├── queue/
         │   │   │   │   ├── coordinator.py
         │   │   │   │   ├── idelegate.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── iview.py
         │   │   │   │   └── section.py
         │   │   │   └── script/
         │   │   │       ├── coordinator.py
         │   │   │       ├── idelegate.py
         │   │   │       ├── __init__.py
         │   │   │       └── section.py
         │   │   └── window/
         │   │       ├── configurator.py
         │   │       ├── factory.py
         │   │       ├── iconfigurator.py
         │   │       └── __init__.py
         │   ├── __init__.py
         │   ├── preferences/
         │   │   ├── dependencies.py
         │   │   ├── exceptions/
         │   │   │   ├── __init__.py
         │   │   │   └── preference_not_found_error.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   ├── serial/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── repository.py
         │   │   └── server/
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── irepository.py
         │   │       ├── preference.py
         │   │       └── repository.py
         │   ├── provides.py
         │   ├── scaralang/
         │   │   ├── bypass/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── demo/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── __init__.py
         │   │   │   ├── linkage/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── solver/
         │   │   │       ├── adapter.py
         │   │   │       ├── factory.py
         │   │   │       ├── iadapter.py
         │   │   │       └── __init__.py
         │   │   ├── protocol/
         │   │   │   ├── builder/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── codec/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── payload/
         │   │   │   │   ├── adapter.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iadapter.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── provides.py
         │   │   │   └── response/
         │   │   │       ├── adapter.py
         │   │   │       ├── factory.py
         │   │   │       ├── iadapter.py
         │   │   │       └── __init__.py
         │   │   ├── provides.py
         │   │   ├── reach/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   ├── safety/
         │   │   │   ├── adapter.py
         │   │   │   ├── factory.py
         │   │   │   ├── iadapter.py
         │   │   │   └── __init__.py
         │   │   └── script/
         │   │       ├── adapter.py
         │   │       ├── discovery.py
         │   │       ├── factory.py
         │   │       ├── iadapter.py
         │   │       └── __init__.py
         │   ├── server/
         │   │   ├── accept/
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iworker.py
         │   │   │   └── worker.py
         │   │   ├── dependencies.py
         │   │   ├── dispatcher/
         │   │   │   ├── dispatcher.py
         │   │   │   ├── factory.py
         │   │   │   ├── idispatcher.py
         │   │   │   └── __init__.py
         │   │   ├── factory.py
         │   │   ├── handler/
         │   │   │   ├── ihandler.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── motion/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── system/
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   └── __init__.py
         │   │   │   └── tool/
         │   │   │       ├── dependencies.py
         │   │   │       ├── factory.py
         │   │   │       ├── handler.py
         │   │   │       └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── iserver.py
         │   │   ├── logger/
         │   │   │   ├── factory.py
         │   │   │   ├── holder.py
         │   │   │   ├── iholder.py
         │   │   │   ├── ilistener.py
         │   │   │   └── __init__.py
         │   │   ├── manager/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── ilistener.py
         │   │   │   ├── imanager.py
         │   │   │   ├── __init__.py
         │   │   │   └── manager.py
         │   │   ├── motion_completion_listener.py
         │   │   ├── pose/
         │   │   │   ├── factory.py
         │   │   │   ├── holder.py
         │   │   │   ├── iholder.py
         │   │   │   └── __init__.py
         │   │   ├── processor/
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iprocessor.py
         │   │   │   └── processor.py
         │   │   ├── provides.py
         │   │   ├── server.py
         │   │   └── session/
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── ioutbound_queue.py
         │   │       ├── iworker.py
         │   │       ├── outbound_queue.py
         │   │       └── worker.py
         │   ├── settings/
         │   │   ├── dependencies.py
         │   │   ├── factory.py
         │   │   ├── geometry/
         │   │   │   ├── factory.py
         │   │   │   ├── iloader.py
         │   │   │   ├── __init__.py
         │   │   │   └── loader.py
         │   │   ├── __init__.py
         │   │   ├── provides.py
         │   │   └── transmission/
         │   │       ├── factory.py
         │   │       ├── iloader.py
         │   │       ├── __init__.py
         │   │       └── loader.py
         │   └── streaming/
         │       ├── dependencies.py
         │       ├── factory.py
         │       ├── __init__.py
         │       ├── motion/
         │       │   ├── coordinator.py
         │       │   ├── factory.py
         │       │   ├── icoordinator.py
         │       │   └── __init__.py
         │       ├── provides.py
         │       ├── pumper/
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── ipumper.py
         │       │   └── pumper.py
         │       └── streamer/
         │           ├── dependencies.py
         │           ├── factory.py
         │           ├── __init__.py
         │           ├── istreamer.py
         │           └── streamer.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── kinematics/
             │   ├── dependencies.py
             │   ├── factory.py
             │   ├── __init__.py
             │   └── provides.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     103 directories, 408 files
```
</details>

#### 🏗 Architecture & SOLID Principles

**scaraemu** follows a clean, decoupled **Layered Digital Twin Architecture** separating real-time kinematic simulation, physical canvas rendering, autonomous trajectory generation, and hardware serial bridging:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                       ScaraEmuGUI                       │ (Presenter / Main Window)
                  └────────────────────────────┬────────────────────────────┘
                                               │ Orchestrates UI Components via DTOs
         ┌─────────────────────────┬───────────┴─────────────┬──────────────────────────┐
         ▼                         ▼                         ▼                          ▼
┌──────────────────┐      ┌─────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│     CanvasXY     │      │     CanvasZ     │      │TrajectoryDemoPanel│      │   ConsolePanel   │
│  (Top-Down 2D)   │      │  (Z Elevation)  │      │(Autonomous Motion)│      │ (Logs/Telemetry) │
└────────┬─────────┘      └────────┬────────┘      └─────────┬─────────┘      └─────────┬────────┘
         │                         │                         │                          │
         └────────────┬────────────┴─────────────────────────┘                          │
                      │ Dispatches Events to Coordinators                               │
                      ▼                                                                 ▼
         ┌──────────────────────────┐                                      ┌─────────────────────────┐
         │   Action Coordinators    │                                      │     Bridge Adapters     │
         └────────────┬─────────────┘                                      └────────────┬────────────┘
                      │ Controls Simulation                                             │ Decodes Binary
                      ▼                                                                 ▼ Frames
         ┌──────────────────────────┐                                      ┌─────────────────────────┐
         │     EmulationService     │ (Kinematic Simulation Engine)        │       BinaryCodec       │
         └────────────┬─────────────┘                                      └────────────┬────────────┘
                      │                                                                 │
         ┌────────────┴────────────┬────────────────────────┐                           │ Uses
         ▼                         ▼                        ▼                           ▼
┌───────────────────┐      ┌──────────────────┐     ┌──────────────────┐    ┌─────────────────────────┐
│ManipulatorKinemat.│      │TrajectoryPreset  │     │  VirtualServer   │    │       BinaryFrame       │
│(Forward / Inverse)│      │(Autonomous Path) │     │ (TCP 127.0.0.1)  │    └─────────────────────────┘
└───────────────────┘      └──────────────────┘     └──────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Strict limit of $\le 15$ methods per class enforced by automated CI quality gate (`srp_checker.py`), with fine-grained components strictly targeting 2 to 4 methods (max 6 methods).
  * Presentation logic is cleanly partitioned between `ScaraEmuGUI` (layout assembly), focused action coordinators (`TargetActionCoordinator`, `JogActionCoordinator`, `QueueActionCoordinator`, `ScriptLoaderCoordinator`), modular bridge adapters (`ServerAdapter`, `StatusAdapter`, `LogAdapter`, `BridgeSynchronizer`), and modular UI panels (`CanvasXY`, `CanvasZ`, `JogPanel`, `TrajectoryDemoPanel`, `ConsolePanel`, `MachinePanel`, `TelemetryPanel`).
* **O — Open/Closed Principle (OCP)**:
  * Autonomous motion routines and trajectory actions use pluggable coordinators without modifying core emulation or rendering dispatchers.
* **L — Liskov Substitution Principle (LSP)**:
  * Strict avoidance of concrete class inheritance hierarchies; all contracts use Python `@runtime_checkable Protocol` structural typing (`IManipulatorKinematics`, `IEmulationService`, `ICanvasXY`, `ICanvasZ`).
* **I — Interface Segregation Principle (ISP)**:
  * Role-specific interfaces ensure components only bind to methods they consume. Validated by `isp_checker.py`.
* **D — Dependency Inversion Principle (DIP)**:
  * Presentation, server handlers, and bridge controllers depend exclusively on structural abstractions (`IManipulatorKinematics`, `IEmulationService`, `IEmulationQueue`) and immutable domain models (`ScaraPose`, `ScaraJoints`, `JointSteps`).

##### Automated Quality Gates (`run_quality_gates.sh`)

All PRs and builds are checked against 4 automated architectural gates:
1. **Structural Protocols Gate**: Confirms 100% adherence to pure `@runtime_checkable Protocol` definitions.
2. **Interface Segregation Gate (ISP)**: Confirms that interfaces are finely segregated with no bloated dependencies.
3. **Module Limits Gate**: Enforces file length limits and line lengths $\le 100$ characters.
4. **Single Responsibility Gate (SRP)**: Enforces strict adherence to $\le 15$ methods per class.

##### 🌐 SCARA Ecosystem Role & Physical Hardware Simulation

**scaraemu** serves as the visual Digital Twin within the unified 4-tier SCARA robotics architecture:
* **[scaralang](https://github.com/vroncevic/scaralang) Integration:** Simulates bytecode execution and binary wire frames (`0xAA 0x55`) compiled by `scaralang`.
* **[scarajectory](https://github.com/vroncevic/scarajectory) Loopback:** Receives real-time streaming trajectories over loopback TCP (port 8888) or PTY serial channels, returning closed-loop flow control and ACK/NACK responses.
* **[scara_base](https://github.com/dof2bot/scara) Hardware Simulation:** Accurately visualizes physical dual-link kinematics, Z-elevation, and end-effector actions corresponding to the real robot driven by Raspberry Pi Pico (RP2040) controlling NEMA steppers in **Open-Loop (TMC2209)** or **Closed-Loop (MKS SERVO42D via CAN bus)**.

#### ✨ Features

* **2D Planar Dual-Link Visualizer**: Real-time rendering of primary ($L_1$) and secondary ($L_2$) arm links, active joint angles, target crosshair, and animated motion path trail.
* **Side Elevation Z-Tower View**: Multi-rod lead screw carriage elevation, active tool height, and radial extension profile visualization.
* **Interactive Targeting & Jogging**: Direct mouse click position targeting on both XY and Z canvases, Cartesian delta jogging ($X, Y, Z, \Phi$), Lefty/Righty elbow toggling, and Emergency Stop.
* **Autonomous Trajectory Demos**: Pre-programmed autonomous demonstration trajectories (Circle, Square, 5-Point Star, 3D Helical Coil, and Pick & Place 3D JUMP Arch).
* **Sliding Window Stream Processing**: Multi-threaded TCP socket and queue processing with dynamic ACK tracking, auto-pause on buffer full, and progress monitoring.
* **Virtual Server Bridge & Binary Protocol Codec**: Bidirectional streaming over TCP socket (port 8888) with `scaralang` binary wire frames (`0xAA 0x55`), real-time status telemetry queries, dynamic queue management, and digital twin synchronization.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, 100% code coverage (8,947/8,947 lines), and 9.99 / 10.00 Pylint score.

#### 📐 SCARA Kinematic & Geometric Configuration

The robot dimensions and physical boundaries can be customized in [`scara_geometry.json`](scaraemu/infrastructure/config/scara_geometry.json) or injected programmatically:

| Parameter | Default Value | Description |
|---|:---:|---|
| **`l1`** | `150.0 mm` | Primary arm link length (shoulder to elbow). |
| **`l2`** | `120.0 mm` | Secondary arm link length (elbow to wrist). |
| **`r_min`** | `30.0 mm` | Inner singular deadzone radius ($|L_1 - L_2|$). |
| **`r_max`** | `270.0 mm` | Maximum horizontal reach boundary ($L_1 + L_2$). |
| **`z_min`** | `0.0 mm` | Minimum vertical height limit (bed level). |
| **`z_max`** | `100.0 mm` | Maximum vertical stroke limit. |
| **`min_speed`** | `1.0 mm/s` | Minimum allowable feedrate speed. |
| **`max_speed`** | `100.0 mm/s` | Maximum allowable safe feedrate speed. |

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `scaraemu/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/model/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/model/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/model/kinematics/joints.py` | 17 | 0 | 100%|
| `scaraemu/core/model/kinematics/pose.py` | 16 | 0 | 100%|
| `scaraemu/core/model/kinematics/step_coords.py` | 16 | 0 | 100%|
| `scaraemu/core/model/simulation/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/model/simulation/state.py` | 19 | 0 | 100%|
| `scaraemu/core/model/simulation/telemetry.py` | 23 | 0 | 100%|
| `scaraemu/core/service/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/controller/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/controller/controller.py` | 32 | 0 | 100%|
| `scaraemu/core/service/emulation/controller/flags.py` | 16 | 0 | 100%|
| `scaraemu/core/service/emulation/controller/icontroller.py` | 18 | 0 | 100%|
| `scaraemu/core/service/emulation/dependencies.py` | 17 | 0 | 100%|
| `scaraemu/core/service/emulation/factory.py` | 30 | 0 | 100%|
| `scaraemu/core/service/emulation/iservice.py` | 17 | 0 | 100%|
| `scaraemu/core/service/emulation/motion/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/motion/stepper.py` | 30 | 0 | 100%|
| `scaraemu/core/service/emulation/notification/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/notification/ilistener.py` | 14 | 0 | 100%|
| `scaraemu/core/service/emulation/notification/inotifier.py` | 15 | 0 | 100%|
| `scaraemu/core/service/emulation/notification/notifier.py` | 21 | 0 | 100%|
| `scaraemu/core/service/emulation/provides.py` | 20 | 0 | 100%|
| `scaraemu/core/service/emulation/queue/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/emulation/queue/iqueue.py` | 17 | 0 | 100%|
| `scaraemu/core/service/emulation/queue/queue.py` | 47 | 0 | 100%|
| `scaraemu/core/service/emulation/queue/snapshot.py` | 17 | 0 | 100%|
| `scaraemu/core/service/emulation/service.py` | 57 | 0 | 100%|
| `scaraemu/core/service/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/kinematics/imanipulator.py` | 19 | 0 | 100%|
| `scaraemu/engine.py` | 59 | 0 | 100%|
| `scaraemu/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/cli/engine.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/bundle.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/dep_validator.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/dependencies.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/factory.py` | 35 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/keys.py` | 25 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/opt_validator.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/options.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/registry.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/validator.py` | 38 | 0 | 100%|
| `scaraemu/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/command/bundle.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/command/definition.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/command/executor.py` | 34 | 0 | 100%|
| `scaraemu/infrastructure/command/idefinition.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/command/iexecutor.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/connection/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/connection/command/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/connection/command/dependencies.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/connection/command/dispatcher.py` | 39 | 0 | 100%|
| `scaraemu/infrastructure/connection/command/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/connection/command/idispatcher.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/connection/coordinator/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/connection/coordinator/coordinator.py` | 38 | 0 | 100%|
| `scaraemu/infrastructure/connection/coordinator/dependencies.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/connection/coordinator/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/connection/coordinator/icoordinator.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/connection/dependencies.py` | 26 | 0 | 100%|
| `scaraemu/infrastructure/connection/factory.py` | 38 | 0 | 100%|
| `scaraemu/infrastructure/connection/handler/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/connection/handler/dependencies.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/connection/handler/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/connection/handler/handler.py` | 63 | 0 | 100%|
| `scaraemu/infrastructure/connection/handler/ihandler.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/connection/listener/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/connection/listener/dependencies.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/connection/listener/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/connection/listener/listener.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/connection/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/dependencies.py` | 31 | 0 | 100%|
| `scaraemu/infrastructure/factory.py` | 55 | 0 | 100%|
| `scaraemu/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/factory.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/log/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/log/adapter.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/provides.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/server/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/server/log_adapter.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/server/state_adapter.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/status/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/status/adapter.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/sync/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/sync/isynchronizer.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/bridge/sync/synchronizer.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/canvas_xy.py` | 73 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/canvas_z.py` | 51 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/config.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/icanvas_xy.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/icanvas_z.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/j1_boundary_renderer.py` | 43 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/manipulator_arm_renderer.py` | 38 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/manipulator_render_context.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/trail_renderer.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/trajectory_path_renderer.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/workspace_boundary_renderer.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/z_render_context.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/renderer/z_renderer.py` | 48 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/elbow_auto_switch_coordinator.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/elbow_dependencies.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/ielbow_auto_switch_coordinator.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/itarget_click_listener.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/itarget_motion_dispatcher.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/target_action_coordinator.py` | 63 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/target_dependencies.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/target/target_motion_dispatcher.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/coordinate_transformer.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/icoordinate_transformer.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/iviewport.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/viewport.py` | 34 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas/viewport/z_coordinate_mapper.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/gui/console/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/console/buffer_actions.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/gui/console/ilog_listener.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/console/panel.py` | 49 | 0 | 100%|
| `scaraemu/infrastructure/gui/delegates/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/delegates/assembly.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/delegates/bundle.py` | 26 | 0 | 100%|
| `scaraemu/infrastructure/gui/delegates/dependencies.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/gui/delegates/factory.py` | 53 | 0 | 100%|
| `scaraemu/infrastructure/gui/dependencies.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/gui/engine.py` | 42 | 0 | 100%|
| `scaraemu/infrastructure/gui/factory.py` | 50 | 0 | 100%|
| `scaraemu/infrastructure/gui/igui.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/action/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/action/coordinator.py` | 59 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/action/dependencies.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/action/idelegate.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/dpad/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/dpad/section.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/panel.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/step/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/step/iprovider.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/jog/step/section.py` | 26 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/builder/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/builder/builder.py` | 93 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/builder/dependencies.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/builder/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/layout/builder/ibuilder.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/lifecycle/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/lifecycle/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/gui/lifecycle/irunner.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/lifecycle/runner.py` | 53 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/configuration/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/configuration/coordinator.py` | 39 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/configuration/idelegate.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/configuration/section.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/panel.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/safety/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/safety/coordinator.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/safety/idelegate.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/machine/safety/section.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/gui/provides.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/services.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/gui/splash/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/splash/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/gui/splash/ifactory.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/splash/iscreen.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/splash/screen.py` | 60 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/cartesian/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/cartesian/section.py` | 48 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/iview.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/joint/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/joint/section.py` | 42 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/panel.py` | 44 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/step/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/telemetry/step/section.py` | 47 | 0 | 100%|
| `scaraemu/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/theme/style.py` | 23 | 0 | 100%|
| `scaraemu/infrastructure/gui/theme/theme.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/dependencies.py` | 27 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/factory.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/ifactory.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/iticker.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/observer/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/observer/iobserver.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/observer/observer.py` | 33 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/scheduler/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/scheduler/ilistener.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/scheduler/ischeduler.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/scheduler/scheduler.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/gui/ticker/ticker.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/action/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/action/coordinator.py` | 40 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/action/idelegate.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/connection/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/connection/istatus_view.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/connection/section.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/panel.py` | 39 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/port/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/port/iprovider.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/port/section.py` | 71 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/server/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/toolbar/server/section.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/panel.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/preset/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/preset/coordinator.py` | 34 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/preset/idelegate.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/preset/section.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/queue/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/queue/coordinator.py` | 23 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/queue/idelegate.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/queue/iview.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/queue/section.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/script/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/script/coordinator.py` | 35 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/script/idelegate.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/gui/trajectory/script/section.py` | 48 | 0 | 100%|
| `scaraemu/infrastructure/gui/window/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/window/configurator.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/gui/window/factory.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/gui/window/iconfigurator.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/preferences/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/preferences/dependencies.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/preferences/exceptions/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/preferences/exceptions/preference_not_found_error.py` | 10 | 0 | 100%|
| `scaraemu/infrastructure/preferences/factory.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/preferences/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/preferences/serial/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/preferences/serial/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/preferences/serial/repository.py` | 65 | 0 | 100%|
| `scaraemu/infrastructure/preferences/server/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/preferences/server/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/preferences/server/irepository.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/preferences/server/preference.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/preferences/server/repository.py` | 65 | 0 | 100%|
| `scaraemu/infrastructure/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/bypass/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/bypass/adapter.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/bypass/factory.py` | 13 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/bypass/iadapter.py` | 11 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/demo/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/demo/adapter.py` | 35 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/demo/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/demo/iadapter.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/dependencies.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/factory.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/linkage/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/linkage/adapter.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/linkage/factory.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/linkage/iadapter.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/solver/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/solver/adapter.py` | 41 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/solver/factory.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/kinematics/solver/iadapter.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/builder/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/builder/adapter.py` | 34 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/builder/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/builder/iadapter.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/codec/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/codec/adapter.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/codec/factory.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/codec/iadapter.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/payload/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/payload/adapter.py` | 31 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/payload/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/payload/iadapter.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/provides.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/response/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/response/adapter.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/response/factory.py` | 21 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/protocol/response/iadapter.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/provides.py` | 42 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/reach/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/reach/adapter.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/reach/factory.py` | 27 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/reach/iadapter.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/safety/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/safety/adapter.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/safety/factory.py` | 29 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/safety/iadapter.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/script/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/script/adapter.py` | 34 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/script/discovery.py` | 31 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/script/factory.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/scaralang/script/iadapter.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/accept/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/accept/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/server/accept/iworker.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/accept/worker.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/dependencies.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/dispatcher/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/dispatcher/dispatcher.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/dispatcher/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/server/dispatcher/idispatcher.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/server/factory.py` | 44 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/ihandler.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/jog/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/jog/dependencies.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/jog/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/jog/handler.py` | 72 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/motion/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/motion/dependencies.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/motion/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/motion/handler.py` | 75 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/system/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/system/dependencies.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/system/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/system/handler.py` | 57 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/tool/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/tool/dependencies.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/tool/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/handler/tool/handler.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/iserver.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/logger/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/logger/factory.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/server/logger/holder.py` | 23 | 0 | 100%|
| `scaraemu/infrastructure/server/logger/iholder.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/logger/ilistener.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/dependencies.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/ilistener.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/imanager.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/manager/manager.py` | 41 | 0 | 100%|
| `scaraemu/infrastructure/server/motion_completion_listener.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/pose/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/pose/factory.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/server/pose/holder.py` | 27 | 0 | 100%|
| `scaraemu/infrastructure/server/pose/iholder.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/server/processor/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/processor/dependencies.py` | 30 | 0 | 100%|
| `scaraemu/infrastructure/server/processor/factory.py` | 37 | 0 | 100%|
| `scaraemu/infrastructure/server/processor/iprocessor.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/processor/processor.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/server/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/server.py` | 74 | 0 | 100%|
| `scaraemu/infrastructure/server/session/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/server/session/dependencies.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/session/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/server/session/ioutbound_queue.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/server/session/iworker.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/server/session/outbound_queue.py` | 32 | 0 | 100%|
| `scaraemu/infrastructure/server/session/worker.py` | 50 | 1 | 98%|
| `scaraemu/infrastructure/settings/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/settings/dependencies.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/settings/factory.py` | 24 | 0 | 100%|
| `scaraemu/infrastructure/settings/geometry/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/settings/geometry/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/settings/geometry/iloader.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/settings/geometry/loader.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/settings/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/settings/transmission/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/settings/transmission/factory.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/settings/transmission/iloader.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/settings/transmission/loader.py` | 36 | 0 | 100%|
| `scaraemu/infrastructure/streaming/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/streaming/dependencies.py` | 20 | 0 | 100%|
| `scaraemu/infrastructure/streaming/factory.py` | 31 | 0 | 100%|
| `scaraemu/infrastructure/streaming/motion/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/streaming/motion/coordinator.py` | 23 | 0 | 100%|
| `scaraemu/infrastructure/streaming/motion/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/streaming/motion/icoordinator.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/streaming/provides.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/streaming/pumper/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/streaming/pumper/dependencies.py` | 22 | 0 | 100%|
| `scaraemu/infrastructure/streaming/pumper/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/streaming/pumper/ipumper.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/streaming/pumper/pumper.py` | 55 | 0 | 100%|
| `scaraemu/infrastructure/streaming/streamer/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/streaming/streamer/dependencies.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/streaming/streamer/factory.py` | 19 | 0 | 100%|
| `scaraemu/infrastructure/streaming/streamer/istreamer.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/streaming/streamer/streamer.py` | 40 | 0 | 100%|
| `scaraemu/setup/__init__.py` | 9 | 0 | 100%|
| `scaraemu/setup/bundle.py` | 24 | 0 | 100%|
| `scaraemu/setup/dep_validator.py` | 36 | 0 | 100%|
| `scaraemu/setup/dependencies.py` | 23 | 0 | 100%|
| `scaraemu/setup/factory.py` | 54 | 0 | 100%|
| `scaraemu/setup/keys.py` | 41 | 0 | 100%|
| `scaraemu/setup/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaraemu/setup/kinematics/dependencies.py` | 18 | 0 | 100%|
| `scaraemu/setup/kinematics/factory.py` | 47 | 0 | 100%|
| `scaraemu/setup/kinematics/provides.py` | 18 | 0 | 100%|
| `scaraemu/setup/opt_validator.py` | 36 | 0 | 100%|
| `scaraemu/setup/options.py` | 22 | 0 | 100%|
| `scaraemu/setup/registry.py` | 24 | 0 | 100%|
| `scaraemu/setup/validator.py` | 32 | 0 | 100%|
| **Total** | 8938 | 1 | 99% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install scaraemu
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/scaraemu/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/scaraemu/main/main.py
```

##### CLI Command Options

Launch the graphical emulator with default configuration:

```bash
python3 main.py emulator
```

Launch with custom geometry overrides:

```bash
python3 main.py emulator --l1 160.0 --l2 110.0 --verbose
```

| Option | Type | Choices | Description |
|---|:---:|:---:|---|
| **`--l1`** | `float` | *Length in mm* | Override primary arm length L1 in millimeters. |
| **`--l2`** | `float` | *Length in mm* | Override secondary arm length L2 in millimeters. |
| **`--z-min`** | `float` | *Limit in mm* | Minimum vertical Z boundary in millimeters. |
| **`--z-max`** | `float` | *Limit in mm* | Maximum vertical Z boundary in millimeters. |
| **`--robot-config`** | `str` | *File path* | Path to custom robot geometry JSON file. |
| **`--verbose`** | `bool` | *Flag* | Enable verbose ATS operational logging. |

##### Interactive Emulation & Control Workflow

1. **2D/3D Kinematic Visualizer**:
   * Inspect top-down planar canvas (XY) and side elevation carriage (Z).
   * Directly click anywhere inside reachable annular workspace to command moves.
2. **Manual Jogging & Axis Control**:
   * Step along $X, Y, Z, \Phi$ with configurable step sizes under **Monitor & Jog**.
   * Toggle between Lefty and Righty elbow configurations or toggle motor power.
3. **Autonomous Demo Trajectories**:
   * Under the **Trajectories** tab, select **Circle**, **Square**, **5-Star**, or **3D Helix**.
   * Watch the real-time simulation interpolator render toolhead paths.
4. **Virtual Server & Telemetry Streaming**:
   * Run embedded Virtual Robot Server listening on TCP socket `127.0.0.1:8888`.
   * Telemetry updates synchronize simulated robot position with the visualizer.
5. **Console & Telemetry Logging**:
   * Inspect live binary protocol logs, server communication events, and real-time telemetry updates.

##### 🤖 Digital Twin Integration with SCARAjectory

**scaraemu** acts as a virtual hardware target, SITL digital twin, and kinematic simulator for **[scarajectory](https://github.com/vroncevic/scarajectory)**.

###### Method 1: Virtual Robot Server (TCP 127.0.0.1:8888)
1. In **scaraemu**, click the **🌐 Virtual Server: OFF** toggle button on the top status bar.
2. The button illuminates green and displays **🌐 Virtual Server: 8888**, listening for incoming TCP client connections on `127.0.0.1:8888`.
3. In **scarajectory**, navigate to the **Hardware Streamer** tab and select **`127.0.0.1:8888 (Digital Twin)`** from the Port dropdown.
4. Click **Connect** in **scarajectory**.
5. Stream any trajectory plan or jog joints interactively:
   * **scaraemu** decodes incoming `scaralang` binary motion frames (`CMD_MOVE_JOINT_STEPS`).
   * Forward kinematics computes joint angles ($\theta_1, \theta_2, Z, \phi$) and renders real-time motion on the 2D and 3D canvases.
   * Bidirectional handshake frames (`RESP_ACK`, `RESP_MOVE_DONE`) flow back to **scarajectory** for closed-loop motion synchronization.

###### Method 2: Launch via CLI with Initial File
Launch **scaraemu** with an initial `.scara` script or `plan.json`:
```bash
python3 main.py emulator --file /path/to/trajectory.scara
```
The emulator automatically loads the file, executes forward and inverse kinematics, and displays the toolhead path.

###### Method 3: Load `.scara` DSL Programs from UI
1. Navigate to the **Trajectories** tab in **scaraemu**.
2. Select any program from the **SCARA DSL Script** dropdown (12 industrial demo programs included).
3. Or click **📂 Load** to browse and open any custom `.scara` or JSON trajectory plan.

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/scaraemu/badge/?version=latest)](https://scaraemu.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [scaraemu.readthedocs.io](https://scaraemu.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to scaraemu](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/scaraemu](https://vroncevic.github.io/scaraemu)

**scaraemu** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/scarajectory/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
