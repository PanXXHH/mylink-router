# MYLINK Router

> A local URI router for personal workspace.

[中文文档](./README.zh-CN.md)

---

## Development Status

> **MYLINK Router is currently under active development.**
>
> The core concept and basic routing workflow have been established, but the project is still being cleaned up and standardized. APIs, configuration formats, installation methods, and internal structure may change before the first stable release.

---

## What is MYLINK Router?

**MYLINK Router** is a Windows-first local URI routing tool. It uses the `mylink://` protocol to connect notes, documents, browsers, scripts, folders, and local projects into one unified entry system.

It is not just a shortcut launcher.

MYLINK Router acts as a small local routing layer for your personal computer. Instead of hard-coding every folder, script, or project into a launcher, each local project can describe itself with a configuration file such as:

```text
mylink.demo.yml
mylink.course.yml
mylink.work.yml
```

Then you can call them through local URI links:

```text
mylink://demo/
mylink://course/
mylink://work/
```

When a `mylink://` URI is opened, MYLINK Router parses the host name, searches for the matching configuration file, loads the target service, and executes the configured entry point.

In short:

```text
mylink://demo/
        ↓
Find mylink.demo.yml
        ↓
Load local project configuration
        ↓
Resolve service_path
        ↓
Execute the configured entry point
        ↓
Open, route, notify, or trigger local actions
```

---

## Why this project exists

Many personal knowledge workers, developers, teachers, and content creators face the same problem:

- projects are scattered across multiple drives;
- files are stored in OneDrive, cloud sync folders, local folders, and external disks;
- notes often need to reference local resources;
- scripts and project folders need stable entry points;
- normal shortcuts are not portable enough;
- launchers can open things, but they do not understand project-level routing logic.

MYLINK Router was created to solve this problem:

> Give every local project a stable link identity.

Instead of remembering where a project is physically stored, you only need to remember its link:

```text
mylink://vfd-course/
mylink://obsidian/
mylink://toolbox/
```

As long as MYLINK Router can find the corresponding `mylink.<host>.yml` configuration file, it can route the link to the right local project.

---

## Core idea

MYLINK Router separates **link identity** from **physical location**.

A project may move from one disk to another, but its URI can stay the same:

```text
mylink://demo/
```

As long as MYLINK Router can find:

```text
mylink.demo.yml
```

it can route the link to the right local project or action.

This makes local resources easier to reference from:

- Markdown notes;
- Obsidian documents;
- browser bookmarks;
- PDF or course materials;
- scripts;
- local automation workflows;
- personal knowledge bases.

---

## Features

Current and planned features include:

- Register and handle the `mylink://` URI protocol on Windows;
- Parse local URI links such as `mylink://demo/`;
- Search target directories for matching `mylink.<host>.yml` configuration files;
- Cache search results to improve routing speed;
- Load project-level configuration from YAML;
- Execute a configured Python entry point;
- Support project-level `.postbox` message folders;
- Provide a lightweight foundation for personal workspace automation.

---

## What MYLINK Router is not

MYLINK Router is intentionally small.

It is **not** trying to replace:

- Everything;
- PowerToys Run;
- Keypirinha;
- Obsidian URI;
- AutoHotkey;
- a full workflow automation platform;
- a cloud short-link service.

Instead, MYLINK Router focuses on one thing:

> Route `mylink://` links to local projects and local actions.

Other tools can still be used together with MYLINK Router.

---

## Naming convention

Recommended naming scheme:

| Usage | Name |
|---|---|
| Repository | `mylink-router` |
| Project name | `MYLINK Router` |
| Python package | `mylink_router` |
| CLI command | `mylink` |
| URI protocol | `mylink://` |
| Config file | `mylink.<host>.yml` |

Example:

```text
mylink://demo/
```

will search for:

```text
mylink.demo.yml
```

---

## Example configuration

A minimal project configuration may look like this:

```yaml
CONFIG:
  index: "index.py"
  entrypoint: "init"
  service_path: "."
```

Field description:

| Field | Description |
|---|---|
| `index` | Python file used as the local service entry module |
| `entrypoint` | Function name to call inside the entry module |
| `service_path` | The actual project or service directory |

A minimal `index.py`:

```python
from pathlib import Path


def init(service_path: Path, parse_result):
    print("MYLINK service started")
    print("Service path:", service_path)
    print("URI:", parse_result.geturl())
```

---

## URI examples

Basic routing:

```text
mylink://demo/
```

Development lookup:

```bash
mylink dev demo
```

Postbox message:

```text
mylink://demo/#post
```

The exact behavior depends on the project configuration and entry point implementation.

---

## Suggested project structure

A clean project structure may look like this:

```text
mylink-router/
├─ mylink_router/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ router.py
│  ├─ config.py
│  └─ utils.py
├─ examples/
│  └─ demo/
│     ├─ mylink.demo.yml
│     └─ index.py
├─ scripts/
│  └─ register-windows-protocol.reg
├─ tests/
├─ README.md
├─ README.zh-CN.md
├─ LICENSE
├─ pyproject.toml
└─ .gitignore
```

Recommended ignored files:

```gitignore
__pycache__/
*.pyc
.data/
.postbox/
.testbox/
_private_*
config.local.*
```

---

## Installation

> The project is still in early development. The installation method may change before the first stable release.

Clone the repository:

```bash
git clone https://github.com/<your-name>/mylink-router.git
cd mylink-router
```

Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or, after packaging is completed:

```bash
pip install -e .
```

---

## Register the Windows URI protocol

To make links such as `mylink://demo/` clickable on Windows, register the `mylink` protocol in the Windows Registry.

A registry entry may look like this:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\mylink]
@="URL:MYLINK Router Protocol"
"URL Protocol"=""

[HKEY_CLASSES_ROOT\mylink\shell\open\command]
@="\"python\" \"C:\\path\\to\\mylink-router\\mylinkuri.py\" \"%1\""
```

Please replace the path with your actual installation path.

---

## Current status

MYLINK Router is currently an experimental personal tool and is still under active development.

The core idea is stable, but the implementation is still being cleaned up. The current focus is:

- simplify and standardize entry points;
- separate private configuration from source code;
- improve error handling;
- add basic tests;
- provide a clean demo project;
- prepare a reproducible installation process;
- document the behavior of `.postbox` and related local workflows.

---

## Roadmap

Planned improvements:

- [ ] Clean package structure under `mylink_router/`;
- [ ] Provide `pyproject.toml` packaging;
- [ ] Add the `mylink` CLI command;
- [ ] Add a safe Windows protocol registration script;
- [ ] Add example projects;
- [ ] Add unit tests for URI parsing and config lookup;
- [ ] Improve cache invalidation;
- [ ] Improve error reporting;
- [ ] Document `.postbox` behavior;
- [ ] Explore integration with Everything for faster local search.

---

## Security notes

MYLINK Router can execute local Python entry points. This is powerful, but it also means configuration files and entry scripts should be trusted.

Recommended rules:

- Do not run unknown `mylink.<host>.yml` files;
- Do not execute scripts from untrusted folders;
- Keep private paths and local configuration out of the public repository;
- Review registry files before importing them;
- Keep `.data/`, `.postbox/`, `.testbox/`, and private configuration files out of version control.

---

## License

This project is released under the MIT License.
