# Infrastructure & Adapters Architecture Audit (`infrastructure_issues.md`)

## 1. Architectural Scope & Layer Boundaries

The **Infrastructure / Adapters layer** (`scaraemu/infrastructure/`) implements communication servers, serial transports, protocol parsers/formatters, command-line interfaces, and Tkinter visualization canvases.

Per Clean Architecture and Dependency Inversion Principle (DIP):
* **Dependency Direction:** Infrastructure points inward toward Application Services and Domain Models.
* **Separation of Wire Formats:** Low-level TCP/Serial transports transfer raw bytes, while protocol parsers and frame builders decode and encode wire frames.
* **Granular Imports:** Strictly granular imports.

---

## 2. Infrastructure Layer Audit Matrix

| Identifier | Subsystem / File | Category | Status | Problem Description / Violation Rationale | Proposed Decoupled Architecture | Actionable Checklist Steps |
|---|---|---|---|---|---|---|
| `INF-01` | `communication/server/virtual_robot_server.py` | Protocol Server / Binary Protocol | 🟢 RESOLVED | Digital twin server only parsed ASCII command strings (`<CMD:...>`, `<pt#...>`), while RP2040 firmware and `scarajectory` have migrated to the CRC16 binary protocol. | Integrate `scaralang` `BinaryFrameParser` and `BinaryFrameBuilder` alongside `VirtualBinaryFrameProcessor`. Support native binary frames (`CMD_MOVE_JOINT_STEPS`, `CMD_HOME`, `CMD_ENABLE`, `CMD_STATUS`, `RESP_ACK`, `RESP_MOVE_EVENT`) while preserving ASCII fallback. | - [x] Implement `VirtualBinaryFrameProcessor` to handle binary frames.<br>- [x] Add binary frame routing and response packing to `VirtualRobotServer`.<br>- [x] Validate with automated unit tests for binary and ASCII streams. |
| `INF-02` | `communication/server/virtual_command_processor.py` | ASCII Command Parser | 🟢 RESOLVED | Legacy ASCII command processor dispatching `<CMD:...>` and `<pt#...>` commands. | Maintain dedicated ASCII command parsing for backward compatibility and manual console commands. | - [x] Maintain ASCII command processing and status classification. |
| `INF-03` | `communication/transport/serial_transport.py` | Hardware Transport | 🟢 RESOLVED | Serial communication bridge connecting emulator to physical RP2040 hardware. | Granular serial port management with configurable baudrate and timeout. | - [x] Maintain serial transport abstraction. |
| `INF-04` | `communication/transport/tcp_transport.py` | Network Transport | 🟢 RESOLVED | TCP streaming transport connecting emulator client to remote or loopback virtual robot server. | Clean socket-based transport satisfying `ITransport`. | - [x] Maintain TCP socket transport abstraction. |
| `INF-05` | `gui/canvas/*` | Presentation Layer | 🟢 RESOLVED | 2D/3D kinematic visualizer canvases (`canvas_xy.py`, `canvas_z.py`, `robot_arm_renderer.py`, `trail_renderer.py`). | Specialized rendering components following SRP, bound to simulation ticker updates. | - [x] Verify rendering decoupling and viewports. |

---

## 3. Master Status & Maintenance Walkthrough

* **Last Audit Walkthrough:** 2026-09-26
* **Status:** Binary protocol parser and frame builder from `scaralang` integrated into digital twin server.
