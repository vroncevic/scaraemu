# Application Service Architecture Audit (`service_issues.md`)

## 1. Architectural Scope & Layer Boundaries

The **Application Service layer** (`scaraemu/core/service/`) orchestrates domain entities, implements use-case interactors, solves forward and inverse kinematics, coordinates motion simulation steps, and loads trajectories from `.scara` DSL scripts and plan files.

Per Clean Architecture and SOLID rules:
* **Protocol Segregation (ISP):** Abstract interfaces are defined with `@runtime_checkable` `Protocol` classes.
* **Structural Protocol Implementation:** Concrete classes must **not** inherit from protocols, must **not** use `@override`, and must **not** import the interface class.
* **Single Responsibility (SRP):** Classes must keep focused responsibilities, with line count target ≤250–300 lines and ≤15 public methods.
* **Granular Imports:** Strictly granular imports.

---

## 2. Service Layer Audit Matrix

| Identifier | Subsystem / File | Category | Status | Problem Description / Violation Rationale | Proposed Decoupled Architecture | Actionable Checklist Steps |
|---|---|---|---|---|---|---|
| `SVC-01` | `kinematics/kinematics_service.py` | Single Responsibility (SRP) | 🟢 RESOLVED | KinematicsService was handling forward/inverse kinematics, step conversions, and linear interpolation in a bloated file. | Decomposed into dedicated collaborating components: `KinematicsStepConverter` for discrete motor pulses and `LinearPathInterpolator` for Cartesian segmentation. | - [x] Extract `KinematicsStepConverter`.<br>- [x] Extract `LinearPathInterpolator`.<br>- [x] Verify `IKinematicsService` structural protocol compliance. |
| `SVC-02` | `simulation/emulator_service.py` | Core Simulation Interactor | 🟢 RESOLVED | Core simulation coordinator managing trajectory queue, kinematics solving, and stepper interpolation ticker. | Clean implementation satisfying `IEmulatorService` structural protocol without direct protocol inheritance. | - [x] Maintain thread-safe queue stepping and telemetry generation.<br>- [x] Verify `IEmulatorService` protocol compliance. |
| `SVC-03` | `script/scara_script_loader.py` | DSL Toolchain Integration | 🟢 RESOLVED | Naive line-by-line regex parsing of `.scara` files without AST validation or macro expansion. | Integrate `scaralang` SCARA DSL toolchain (`ScaraParserFactory` / `ScaraDslServiceFactory`), converting parsed AST instructions and compiled plans into `ScaraPose` sequences. | - [x] Integrate `scaralang` parser and AST instructions.<br>- [x] Preserve backward-compatible `.scara` and `.json` file loading.<br>- [x] Verify `IScaraScriptLoader` structural protocol. |
| `SVC-04` | `core/service/engine.py` | Service Facade / SRP | 🟢 RESOLVED | Service engine composition root assembling emulator and kinematics sub-services. | Dedicated facade providing unified application services to the CLI and GUI engines. | - [x] Verify service engine lifecycle and collaborators. |

---

## 3. Master Status & Maintenance Walkthrough

* **Last Audit Walkthrough:** 2026-09-26
* **Status:** Service contracts strictly adhere to ISP, structural typing, and modular decomposition.
