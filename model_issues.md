# Domain Model Architecture Audit (`model_issues.md`)

## 1. Architectural Scope & Layer Boundaries

The **Domain Model layer** (`scaraemu/core/model/`) encapsulates the fundamental entities, value objects, kinematic definitions, and simulation representations of the SCARA emulator digital twin.

Per Clean Architecture and Domain-Driven Design (DDD) principles:
* **Zero Dependencies on Outer Layers:** Models must never import services, infrastructure adapters, serializers, or GUI components.
* **Immutability & Slots:** Data structures must use `@dataclass(frozen=True, slots=True)` where state should be protected against accidental mutation.
* **Granular Imports:** Strictly granular imports from the standard library or sibling domain models.
* **Modern Type Annotations:** Mandatory `from __future__ import annotations` as the first line of code.

---

## 2. Domain Model Audit Matrix

| Identifier | Subsystem / File | Category | Status | Problem Description / Violation Rationale | Proposed Decoupled Architecture | Actionable Checklist Steps |
|---|---|---|---|---|---|---|
| `MOD-01` | `kinematics/scara_geometry.py` | Value Object / Invariants | 🟢 RESOLVED | Mutable defaults or non-slots dataclass representation in geometry representation. | Refactored to frozen dataclass with slots, default link lengths (`l1=150.0`, `l2=120.0`), explicit angular bounds and singularity tolerances. | - [x] Verify frozen slots on `ScaraGeometry`.<br>- [x] Validate immutable geometric constants. |
| `MOD-02` | `kinematics/scara_pose.py` | Value Object | 🟢 RESOLVED | End-effector Cartesian representation (`x, y, z, phi`). | Immutable `@dataclass(frozen=True, slots=True)` with explicit coordinate attributes and default elevation/orientation. | - [x] Maintain immutable 4-DOF Cartesian pose value object. |
| `MOD-03` | `kinematics/scara_joints.py` | Value Object | 🟢 RESOLVED | Kinematic joint coordinates (`theta1, theta2, z, theta4, reachable`). | Frozen slots dataclass tracking continuous angular/linear values and analytical reachability flag. | - [x] Maintain immutable joint coordinates representation. |
| `MOD-04` | `kinematics/scara_step_coords.py` | Value Object | 🟢 RESOLVED | Discrete stepper motor counts (`j1_steps, j2_steps, z_steps, j4_steps`). | Frozen slots dataclass mapping joint positions to discrete motor pulses for RP2040 stepper timers. | - [x] Maintain immutable stepper pulse coordinate representation. |
| `MOD-05` | `kinematics/kinematics_config.py` | Value Object | 🟢 RESOLVED | Mechanical transmission specs (steps per rev, microstepping, gear ratios, leadscrew pitch). | Frozen slots dataclass holding mechanical drivetrain specifications with safe default ratios. | - [x] Maintain transmission parameter definitions. |
| `MOD-06` | `simulation/simulation_state.py` | Enum Definition | 🟢 RESOLVED | Finite simulation states (`IDLE`, `RUNNING`, `PAUSED`, `ESTOP`, `ERROR`). | Standard `Enum` defining discrete emulator lifecycle states. | - [x] Maintain discrete simulation state enumeration. |
| `MOD-07` | `simulation/telemetry.py` | Value Object | 🟢 RESOLVED | Real-time simulation telemetry snapshot (pose, joints, steps, queue depth, motors enabled, estop, fps). | Frozen slots dataclass delivering immutable telemetry bundles to observers and presentation panels. | - [x] Maintain telemetry value object. |
| `MOD-08` | `scaralang/core/model/*` | External Package Integration | 🟢 RESOLVED | SCARA DSL AST and binary protocol models shared across tools. | Seamlessly integrate `scaralang` domain models (`BinaryFrame`, `JointSteps`, `MessageId`, `ScaraStatus`, `DiagnosticsSnapshot`, `MoveEvent`, `FaultEvent`) into digital twin protocol server. | - [x] Add `scaralang` dependency to `requirements.txt` and `setup.py`.<br>- [x] Interoperate with `scaralang.core.model.protocol.*`. |

---

## 3. Master Status & Maintenance Walkthrough

* **Last Audit Walkthrough:** 2026-09-26
* **Status:** 100% of domain models conform to SOLID, Clean Architecture, and PEP 563 postponed evaluation of annotations.
