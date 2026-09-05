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
         │       ├── iscara_script_loader.py
         │       ├── iservice.py
         │       ├── kinematics_service.py
         │       └── scara_script_loader.py
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
         │   │   │   ├── config_command_formatter.py
         │   │   │   ├── firmware_response_dto.py
         │   │   │   ├── __init__.py
         │   │   │   ├── motion_command_formatter.py
         │   │   │   └── protocol_parser.py
         │   │   ├── serial_device_preferences.py
         │   │   ├── serial_port_scanner.py
         │   │   └── transport/
         │   │       ├── __init__.py
         │   │       ├── itransport.py
         │   │       ├── ivirtual_robot_server.py
         │   │       ├── serial_transport.py
         │   │       ├── tcp_transport.py
         │   │       └── virtual_robot_server.py
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
         │       ├── gui_event_handler.py
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

     15 directories, 87 files
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
│     CanvasXY     │      │     CanvasZ     │      │TrajectoryDemoPanel│      │ SerialConsolePan.│
│  (Top-Down 2D)   │      │  (Z Elevation)  │      │(Autonomous Motion)│      │  (Raw Telemetry) │
└────────┬─────────┘      └────────┬────────┘      └─────────┬─────────┘      └─────────┬────────┘
         │                         │                         │                          │
         └────────────┬────────────┴─────────────────────────┘                          │
                      │ Dispatches Events to GUIEventHandler                            │
                      ▼                                                                 ▼
         ┌──────────────────────────┐                                      ┌─────────────────────────┐
         │     GUIEventHandler      │                                      │ HardwareBridgeController│
         └────────────┬─────────────┘                                      └────────────┬────────────┘
                      │ Controls Simulation                                             │ Translates ASCII
                      ▼                                                                 ▼ Packets
         ┌──────────────────────────┐                                      ┌─────────────────────────┐
         │     EmulatorService      │ (Kinematic Simulation Engine)        │     ProtocolParser      │
         └────────────┬─────────────┘                                      └────────────┬────────────┘
                      │                                                                 │
         ┌────────────┴────────────┬────────────────────────┐                           │ Uses
         ▼                         ▼                        ▼                           ▼
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐     ┌─────────────────────────┐
│KinematicsService │      │TrajectoryDemoGen.│     │ CommandTemplates│     │  FirmwareResponseDTO    │
│(Forward / Inverse│      │ (Pick&Place/JUMP)│     │(Syntax Alignment│     └─────────────────────────┘
└──────────────────┘      └──────────────────┘     └─────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Strict limit of $\le 15$ methods per class enforced by automated CI quality gate (`srp_checker.py`).
  * Presentation logic is cleanly partitioned between `ScaraEmuGUI` (layout assembly), `GUIEventHandler` (user interactions), `HardwareBridgeController` (serial bridging), and modular UI panels (`CanvasXY`, `CanvasZ`, `JogPanel`, `TrajectoryDemoPanel`).
* **O — Open/Closed Principle (OCP)**:
  * `TrajectoryDemoGenerator` uses a registry pattern to register new autonomous demonstration routines (e.g. `generate_pick_and_place`) without altering caller or dispatcher logic.
* **L — Liskov Substitution Principle (LSP)**:
  * Strict avoidance of concrete class inheritance hierarchies; all contracts use Python `@runtime_checkable Protocol` structural typing (`IKinematicsService`, `IEmulatorService`, `ICanvasXY`, `ICanvasZ`).
* **I — Interface Segregation Principle (ISP)**:
  * Role-specific interfaces ensure components only bind to methods they consume. Validated by `isp_checker.py`.
* **D — Dependency Inversion Principle (DIP)**:
  * Presentation and bridge controllers depend exclusively on abstractions (`IKinematicsService`, `IEmulatorService`) and immutable domain DTOs (`ScaraPose`, `ScaraJoints`, `TelemetryDTO`).

##### Automated Quality Gates (`run_quality_gates.sh`)

All PRs and builds are checked against 4 automated architectural gates:
1. **Structural Protocols Gate**: Confirms 100% adherence to pure `@runtime_checkable Protocol` definitions.
2. **Interface Segregation Gate (ISP)**: Confirms that interfaces are finely segregated with no bloated dependencies.
3. **Module Limits Gate**: Enforces file length limits and line lengths $\le 100$ characters.
4. **Single Responsibility Gate (SRP)**: Enforces strict adherence to $\le 15$ methods per class.

#### ✨ Features

* **2D Planar Dual-Link Visualizer**: Real-time rendering of primary ($L_1$) and secondary ($L_2$) arm links, active joint angles, target crosshair, and animated motion path trail.
* **Side Elevation Z-Tower View**: Multi-rod lead screw carriage elevation, active tool height, and radial extension profile visualization.
* **Interactive Targeting & Jogging**: Direct mouse click position targeting on both XY and Z canvases, Cartesian delta jogging ($X, Y, Z, \Phi$), Lefty/Righty elbow toggling, and Emergency Stop.
* **Autonomous Trajectory Demos**: Pre-programmed autonomous demonstration trajectories (Circle, Square, 5-Point Star, 3D Helical Coil, and Pick & Place 3D JUMP Arch).
* **Sliding Window Hardware Streaming**: Multi-threaded USB serial (`/dev/ttyACM0`) and TCP socket streaming with dynamic ACK tracking, auto-pause on buffer full, and progress monitoring.
* **Hardware Serial Bridge & Protocol Parser**: Bidirectional streaming over USB Serial (RP2040 micro-commands) with raw terminal telemetry log, live feedrate override, hardware dwell delays, pneumatic tool toggles, and manual command console.
* **Configurable Kinematics & Dimensions**: Dynamic robot link lengths ($L_1, L_2$), stroke limits ($Z_{min}, Z_{max}$), and speed bounds configurable via CLI options and JSON schema.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, high test coverage, and 10.00 / 10.00 Pylint score.

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
| `scaraemu/core/model/kinematics_config_dto.py` | 18 | 0 | 100%|
| `scaraemu/core/model/scara_geometry.py` | 37 | 0 | 100%|
| `scaraemu/core/model/scara_joints.py` | 17 | 0 | 100%|
| `scaraemu/core/model/scara_pose.py` | 16 | 0 | 100%|
| `scaraemu/core/model/scara_step_coords.py` | 16 | 0 | 100%|
| `scaraemu/core/model/simulation_state_dto.py` | 17 | 0 | 100%|
| `scaraemu/core/model/telemetry_dto.py` | 22 | 0 | 100%|
| `scaraemu/core/service/__init__.py` | 9 | 0 | 100%|
| `scaraemu/core/service/demo_generator.py` | 58 | 0 | 100%|
| `scaraemu/core/service/emulator_service.py` | 123 | 15 | 88%|
| `scaraemu/core/service/engine.py` | 24 | 0 | 100%|
| `scaraemu/core/service/iemulator_service.py` | 31 | 0 | 100%|
| `scaraemu/core/service/ikinematics_service.py` | 24 | 0 | 100%|
| `scaraemu/core/service/iscara_script_loader.py` | 15 | 15 | 0%|
| `scaraemu/core/service/iservice.py` | 17 | 0 | 100%|
| `scaraemu/core/service/kinematics_service.py` | 126 | 31 | 75%|
| `scaraemu/core/service/scara_script_loader.py` | 114 | 5 | 96%|
| `scaraemu/engine.py` | 64 | 64 | 0%|
| `scaraemu/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/cli/engine.py` | 40 | 7 | 82%|
| `scaraemu/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/bundle.py` | 22 | 1 | 95%|
| `scaraemu/infrastructure/cli/setup/dep_validator.py` | 36 | 1 | 97%|
| `scaraemu/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/factory.py` | 37 | 1 | 97%|
| `scaraemu/infrastructure/cli/setup/keys.py` | 28 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/opt_validator.py` | 35 | 1 | 97%|
| `scaraemu/infrastructure/cli/setup/options.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/cli/setup/registry.py` | 31 | 1 | 97%|
| `scaraemu/infrastructure/cli/setup/validator.py` | 43 | 5 | 88%|
| `scaraemu/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/command/command.py` | 16 | 0 | 100%|
| `scaraemu/infrastructure/command/emulator_command_definition.py` | 24 | 1 | 96%|
| `scaraemu/infrastructure/command/emulator_command_executor.py` | 35 | 6 | 83%|
| `scaraemu/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `scaraemu/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/communication/protocol/command_formatter.py` | 12 | 0 | 100%|
| `scaraemu/infrastructure/communication/protocol/command_templates.py` | 38 | 0 | 100%|
| `scaraemu/infrastructure/communication/protocol/config_command_formatter.py` | 37 | 8 | 78%|
| `scaraemu/infrastructure/communication/protocol/firmware_response_dto.py` | 17 | 0 | 100%|
| `scaraemu/infrastructure/communication/protocol/motion_command_formatter.py` | 51 | 3 | 94%|
| `scaraemu/infrastructure/communication/protocol/protocol_parser.py` | 116 | 16 | 86%|
| `scaraemu/infrastructure/communication/serial_device_preferences.py` | 40 | 20 | 50%|
| `scaraemu/infrastructure/communication/serial_port_scanner.py` | 43 | 5 | 88%|
| `scaraemu/infrastructure/communication/transport/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/communication/transport/itransport.py` | 22 | 5 | 77%|
| `scaraemu/infrastructure/communication/transport/serial_transport.py` | 102 | 59 | 42%|
| `scaraemu/infrastructure/communication/transport/tcp_transport.py` | 96 | 55 | 43%|
| `scaraemu/infrastructure/communication/transport/virtual_robot_server.py` | 201 | 47 | 77%|
| `scaraemu/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/canvas_xy.py` | 157 | 122 | 22%|
| `scaraemu/infrastructure/gui/canvas_z.py` | 74 | 46 | 38%|
| `scaraemu/infrastructure/gui/components/__init__.py` | 9 | 0 | 100%|
| `scaraemu/infrastructure/gui/components/jog_panel.py` | 83 | 52 | 37%|
| `scaraemu/infrastructure/gui/components/serial_bar.py` | 98 | 69 | 30%|
| `scaraemu/infrastructure/gui/components/serial_console_panel.py` | 75 | 52 | 31%|
| `scaraemu/infrastructure/gui/components/telemetry_panel.py` | 64 | 36 | 44%|
| `scaraemu/infrastructure/gui/components/trajectory_demo_panel.py` | 91 | 61 | 33%|
| `scaraemu/infrastructure/gui/engine.py` | 167 | 103 | 38%|
| `scaraemu/infrastructure/gui/gui_event_handler.py` | 125 | 93 | 26%|
| `scaraemu/infrastructure/gui/hardware_bridge_controller.py` | 117 | 30 | 74%|
| `scaraemu/infrastructure/gui/icanvas_xy.py` | 19 | 2 | 89%|
| `scaraemu/infrastructure/gui/icanvas_z.py` | 17 | 2 | 88%|
| `scaraemu/infrastructure/gui/igui.py` | 15 | 0 | 100%|
| `scaraemu/infrastructure/gui/theme.py` | 28 | 0 | 100%|
| `scaraemu/setup/__init__.py` | 9 | 0 | 100%|
| `scaraemu/setup/bundle.py` | 25 | 1 | 96%|
| `scaraemu/setup/dep_validator.py` | 36 | 1 | 97%|
| `scaraemu/setup/dependencies.py` | 21 | 0 | 100%|
| `scaraemu/setup/factory.py` | 88 | 3 | 97%|
| `scaraemu/setup/keys.py` | 39 | 0 | 100%|
| `scaraemu/setup/opt_validator.py` | 36 | 2 | 94%|
| `scaraemu/setup/options.py` | 22 | 0 | 100%|
| `scaraemu/setup/registry.py` | 34 | 1 | 97%|
| `scaraemu/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 3540 | 1053 | 70% |

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
4. **Hardware Bridge & Telemetry Streaming**:
   * Connect to physical SCARA microcontroller via `/dev/ttyACM0` or TCP socket.
   * Telemetry updates synchronize live hardware position with the visualizer.
5. **Serial Command Console**:
   * Inspect incoming raw protocol packets (`<TELEM...>`, `<RESP:...>`) and send custom commands.

##### 🤖 Digital Twin Integration with SCARAjectory

**scaraemu** acts as a virtual hardware target, SITL digital twin, and kinematic simulator for **[scarajectory](https://github.com/vroncevic/scarajectory)**.

###### Method 1: Virtual Robot Server (TCP 127.0.0.1:8888)
1. In **scaraemu**, click the **🌐 Virtual Server: OFF** toggle button on the top status bar.
2. The button illuminates green and displays **🌐 Virtual Server: 8888**, listening for incoming TCP client connections on `127.0.0.1:8888`.
3. In **scarajectory**, navigate to the **Hardware Streamer** tab and select **`127.0.0.1:8888 (Digital Twin)`** from the Port dropdown.
4. Click **Connect** in **scarajectory**.
5. Stream any trajectory plan or jog joints interactively:
   * **scaraemu** parses incoming motion packets (`<pt#X#Y#Z#PHI#SPEED#end>`).
   * Forward kinematics computes joint angles ($\theta_1, \theta_2, Z, \phi$) and renders real-time motion on the 2D and 3D canvases.
   * Bidirectional handshake messages (`<RESP:ACK#QUEUE=1>`, `<RESP:MOVE_DONE#...>`) flow back to **scarajectory** for closed-loop motion synchronization.

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
