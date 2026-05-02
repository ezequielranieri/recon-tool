# 🚀 recon-tool

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![Checked with mypy](https://img.shields.io/badge/mypy-checked-2a6db2)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

**Professional Network Reconnaissance Tool built with Python and Asyncio.**

`recon-tool` is a high-performance CLI utility designed for fast, secure, and reliable network scanning. It leverages asynchronous I/O to perform concurrent port discovery, banner grabbing, and service identification, providing detailed reports in human-readable and machine-interoperable formats.

---

## 🛡️ Why this project?

This tool was developed to demonstrate a senior-level mastery of the Python ecosystem, specifically focused on **Security** and **Backend Engineering**. It serves as a practical showcase of:

- **Asynchronous Concurrency**: Using `asyncio` and semaphores to handle massive network I/O without blocking.
- **Security-First Mindset**: Implementing robust input validation, blocking scans on reserved/private IP ranges, and sanitizing untrusted data (banners).
- **Clean Architecture**: A modular, highly-typed, and tested codebase following SOLID principles and Google Style documentation.
- **Professional UX**: A polished CLI experience using `Typer` and `Rich` with real-time feedback and structured outputs.

---

## ✨ Features

- **Concurrent TCP Scanning**: Lightning-fast port discovery using non-blocking sockets.
- **Intelligent Service Identification**: Port-to-service mapping and heuristic-based detection using captured banners.
- **Advanced Banner Grabbing**: Securely captures service banners with automated sanitization to prevent terminal injection.
- **Smart Input Parsing**: Supports complex port specifications (e.g., `80,443,1-1024,8080`).
- **Exportable Reports**: Generate detailed findings in structured `JSON` or formatted `TXT`.
- **Safety Boundaries**: Built-in protection against scanning local/reserved networks (RFC compliance).

---

## 🛠️ Technologies

- **Python 3.12+**
- **Asyncio**: Main concurrency engine.
- **Typer**: Professional CLI framework.
- **Rich**: Terminal formatting, tables, and progress bars.
- **Pydantic v2**: Data modeling and strict validation.
- **Pydantic Settings**: Environment-based configuration.
- **Pytest**: Comprehensive unit and integration testing.
- **Ruff & Mypy**: Industry-standard linting and strict type checking.

---

## 📦 Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/ezequielranieri/recon-tool.git
cd recon-tool
pip install -e .
```

For development dependencies:
```bash
pip install -e ".[dev]"
```

---

## 🚀 Usage

### Basic Scan
Scan the top 1000 ports of a target host:
```bash
python -m recon scan google.com
```

### Advanced Port Selection
Scan specific ports and ranges:
```bash
python -m recon scan 8.8.8.8 --ports 22,80,443,8000-9000
```

### High-Performance Scanning
Adjust concurrency (workers) and timeouts:
```bash
python -m recon scan example.com --workers 500 --timeout 0.5
```

### Exporting Reports
Save findings to a file in JSON format:
```bash
python -m recon scan scanme.nmap.org -o results.json -f json
```

---

## 📊 Expected Output

```text
╭─────────────────────────────────────╮
│   recon-tool v0.1.0                 │
│   Network Reconnaissance Tool       │
╰─────────────────────────────────────╯

Target:  scanme.nmap.org
Ports:   22,80,443 (3 ports)
Workers: 100 | 1.0s

Scanning scanme.nmap.org... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

                          Results for scanme.nmap.org
┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Port   ┃ State   ┃ Service         ┃ Banner                                  ┃
┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 22     │ open    │ SSH             │ SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2 │
│ 80     │ open    │ HTTP            │ -                                       │
└────────┴─────────┴─────────────────┴─────────────────────────────────────────┘

Completed in 1.42s
Open: 2
```

---

## 🏗️ Architecture

The project follows a modular structure designed for maintainability and testability:

- **`core/`**: The engine. Handles socket connections (`scanner.py`), banner acquisition (`banner.py`), and service logic (`service.py`).
- **`utils/`**: Shared logic. Contains strict security validators and network parsers.
- **`reports/`**: Data persistence. Decoupled logic for different export formats.
- **`models/`**: Pydantic models ensuring data integrity across the entire pipeline.
- **`cli.py`**: The interface layer. Orchestrates the flow and handles the UI.

---

## 🧪 Quality & Testing

The project maintains high standards through automated checks:

- **Unit Tests**: Coverage for all core logic, validators, and report generators.
- **Integration Tests**: End-to-end CLI flow verification.
- **Static Analysis**: 100% type-safe (Mypy strict) and lint-free (Ruff).

Run tests:
```bash
pytest
```

Run linting:
```bash
ruff check .
mypy src/
```
