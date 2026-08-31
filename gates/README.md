# Quality Gates

A comprehensive suite of lightweight, Python standard library-based quality gate scripts for static code analysis, structural validation, and automated quality/architectural design enforcement.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Interfaces Checker](#1-interfaces-checker)
  - [Interface Segregation Principle (ISP) Checker](#2-interface-segregation-principle-isp-checker)
  - [Limits Checker](#3-limits-checker)
  - [Single Responsibility Principle (SRP) Checker](#4-single-responsibility-principle-srp-checker)
- [Exit Codes](#exit-codes)
- [License](#license)
- [Contributing](#contributing)
- [Support](#support)

## ✨ Features

- **Zero Third-Party Dependencies**: Relies entirely on the Python Standard Library (`ast`, `argparse`, `logging`, etc.), making integration into CI/CD pipelines seamless and fast.
- **SOLID Architectural Enforcement**: Directly validates the **Single Responsibility Principle (SRP)** and the **Interface Segregation Principle (ISP)** using Abstract Syntax Tree (AST) analysis.
- **Protocol & Interface Verification**: Ensures concrete classes correctly implement structural protocols and interface contracts.
- **Code Metric Controls**: Enforces module size and line length thresholds to maintain readable, clean code.
- **Logging and Verbose Reporting**: Built-in support for standard logging with detailed analysis output using `--verbose`.

## 📁 Project Structure

```text
.
├── gates/
│   ├── interfaces_checker.py  # Verifies concrete classes correctly implement defined protocols
│   ├── isp_checker.py         # Enforces Interface Segregation Principle bounds on abstract methods
│   ├── limits_checker.py      # Enforces file/module size and line length thresholds
│   └── srp_checker.py         # Enforces Single Responsibility Principle bounds (methods & lines)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 🚀 Installation

Since the quality gates are built using only the Python standard library, no external package installation is required.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vroncevic/quality-gates-py.git
   cd quality-gates-py
   ```

2. **Verify Python Installation**:
   Ensure you have Python 3.8+ installed:
   ```bash
   python3 --version
   ```

## 🛠 Usage

All checker scripts are located in the `gates/` package and can be run as Python modules. Each script accepts a target package/module directory as a positional argument.

### 1. Interfaces Checker

Verifies that concrete classes in the codebase correctly implement structural protocols (interfaces) defined in the package.

- **How it works**:
  1. Scans the package for protocol definitions (class names starting with `I` followed by an uppercase letter, e.g., `IRepository`).
  2. Extracts all methods and properties declared on these protocol classes.
  3. Scans concrete classes and verifies that they implement all methods and properties expected by their matching protocol (e.g., class `Repository` is checked against `IRepository`).
  4. Excludes dataclasses, exceptions, and specified base classes from verification.

- **CLI Usage**:
  ```bash
  python3 -m gates.interfaces_checker <package_dir> [options]
  ```

- **Options**:
  - `package_dir` (Required): Path to the target Python package directory to analyze.
  - `-v`, `--verbose`: Enable detailed parsing and check logs.

---

### 2. Interface Segregation Principle (ISP) Checker

Enforces interface segregation constraints by warning or failing if any interface/protocol becomes too "fat" (declares too many abstract methods).

- **How it works**:
  1. Scans for interface classes (named starting with `I` followed by an uppercase letter, or defined in modules whose names start with `i` followed by an uppercase letter).
  2. Counts the number of abstract methods decorated with `@abstractmethod` or `@abc.abstractmethod`.
  3. Validates against `MAX_ABSTRACT_METHODS = 9`. If an interface defines more than this limit, the check fails, prompting interface segregation.

- **CLI Usage**:
  ```bash
  python3 -m gates.isp_checker <package_dir> [options]
  ```

- **Options**:
  - `package_dir` (Required): Path to the target Python package directory.
  - `-v`, `--verbose`: Enable detailed logs of method counts for each interface.

---

### 3. Limits Checker

Enforces physical metrics constraints on modules, preventing the creation of unmaintainably large files or extremely long, unreadable lines.

- **How it works**:
  1. Scans all Python modules (`.py` files) recursively in the target directory.
  2. Measures module line count and checks against `MAX_MODULE_LINES = 500`.
  3. Scans each line's length and checks against `MAX_LINE_LENGTH = 150` characters.

- **CLI Usage**:
  ```bash
  python3 -m gates.limits_checker <package_dir> [options]
  ```

- **Options**:
  - `package_dir` (Required): Path to the target Python package directory.
  - `-v`, `--verbose`: Enable detailed reports of checked lines and counts.

---

### 4. Single Responsibility Principle (SRP) Checker

Validates Single Responsibility Principle boundaries at both the class and method levels.

- **How it works**:
  1. **Class-level**: Counts the number of methods defined in each class. Ensures the total does not exceed `MAX_METHODS_PER_CLASS = 15`.
  2. **Method-level**: Counts actual logical lines of code within methods (excluding docstrings, blank lines, and comments). Ensures no method exceeds `MAX_LOGICAL_LINES_PER_METHOD = 180`.

- **CLI Usage**:
  ```bash
  python3 -m gates.srp_checker <package_dir> [options]
  ```

- **Options**:
  - `package_dir` (Required): Path to the target Python package directory.
  - `-v`, `--verbose`: Enable detailed output including method and line counts.

---

## 🏁 Exit Codes

All checker scripts follow unified exit codes to integrate cleanly into automated environments:

| Exit Code | Meaning |
|-----------|---------|
| **0** | Quality Gate passed successfully (no violations found). |
| **1** | Quality Gate failed (violations/errors detected). |

## 📄 License

This project is licensed under the terms of the GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE) for details.

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. Create a **feature branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📞 Support

For issues, questions, or feature requests, please:

1. Check the [Issues](https://github.com/vroncevic/quality-gates-py/issues) section.
2. Open a new issue with detailed reproduction steps or information.
3. Contact the development team at [elektron.ronca@gmail.com].

---

*Built with ❤️ for quality code assurance*
