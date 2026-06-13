# MYLINK Router

> 一个面向个人工作区的本地 URI 协议路由器。

[English](./README.md)

---

## 开发阶段说明

> **MYLINK Router 目前仍处于持续开发阶段。**
>
> 项目的核心思路和基础路由流程已经明确，但代码结构、配置格式、安装方式和内部 API 仍在继续整理中。在第一个稳定版本发布之前，相关实现可能会发生调整。

---

## MYLINK Router 是什么？

**MYLINK Router** 是一个优先面向 Windows 的本地链接路由器。它通过 `mylink://` 协议，把笔记、文档、浏览器、脚本、文件夹和本地项目统一连接到一套可跳转、可扩展、可配置的入口系统中。

它不是一个普通的快捷方式工具。

它更像是你电脑上的一层**本地链接路由系统**。你可以让每个本地项目通过一个配置文件描述自己，例如：

```text
mylink.demo.yml
mylink.course.yml
mylink.work.yml
```

然后通过本地 URI 链接调用它们：

```text
mylink://demo/
mylink://course/
mylink://work/
```

当你点击或打开一个 `mylink://` 链接时，MYLINK Router 会解析链接中的主机名，查找对应的配置文件，读取项目配置，定位服务目录，并执行配置好的入口函数。

整体流程可以理解为：

```text
mylink://demo/
        ↓
查找 mylink.demo.yml
        ↓
读取本地项目配置
        ↓
定位 service_path
        ↓
执行配置好的入口函数
        ↓
打开、跳转、提醒或触发本地动作
```

---

## 为什么要做这个项目？

很多长期使用电脑做知识管理、课程开发、自动化脚本、资料整理的人，都会遇到一个问题：

- 项目分散在多个硬盘；
- 文件夹分布在 OneDrive、ownCloud、本地目录、移动硬盘中；
- Obsidian、Markdown、课程文档里经常需要引用本地资源；
- 普通快捷方式不够稳定，也不方便写进文档；
- 启动器可以打开文件，但不理解每个项目自己的配置和动作逻辑；
- 项目移动位置以后，原来的路径引用容易失效。

MYLINK Router 要解决的就是这个问题：

> 给每个本地项目一个稳定的链接身份。

也就是说，你不用一直记住项目到底放在哪个盘，只需要记住：

```text
mylink://vfd-course/
mylink://obsidian/
mylink://toolbox/
```

只要 MYLINK Router 能找到对应的 `mylink.<host>.yml` 配置文件，它就能把链接路由到正确的本地项目。

---

## 核心理念

MYLINK Router 的核心理念是：

> 链接身份和物理路径分离。

项目可以从 F 盘移动到 G 盘，也可以从本地目录移动到同步盘，但它对外暴露的链接可以不变：

```text
mylink://demo/
```

只要对应配置文件还存在：

```text
mylink.demo.yml
```

MYLINK Router 就可以重新找到它，并执行对应动作。

这使得本地资源可以更方便地被引用到：

- Markdown 笔记；
- Obsidian 文档；
- 浏览器书签；
- 课程资料；
- 自动化脚本；
- 本地知识库；
- 个人工作流系统。

---

## 功能特性

当前和计划支持的能力包括：

- 在 Windows 上注册并处理 `mylink://` 协议；
- 解析 `mylink://demo/` 这类本地 URI；
- 根据 host 查找 `mylink.<host>.yml` 配置文件；
- 支持多个目标目录搜索；
- 支持搜索结果缓存，减少重复扫盘；
- 读取 YAML 项目配置；
- 执行项目自定义 Python 入口函数；
- 支持项目级 `.postbox` 消息目录；
- 为个人工作区自动化提供一层轻量基础设施。

---

## MYLINK Router 不是什么？

MYLINK Router 不打算做成一个大而全工具。

它不准备替代：

- Everything；
- PowerToys Run；
- Keypirinha；
- Obsidian URI；
- AutoHotkey；
- 完整自动化平台；
- 云端短链接服务。

它只专注一件事：

> 把 `mylink://` 链接路由到本地项目和本地动作。

其他工具仍然可以和 MYLINK Router 配合使用。

---

## 命名约定

推荐统一命名如下：

| 使用场景 | 名称 |
|---|---|
| GitHub 仓库名 | `mylink-router` |
| 项目展示名 | `MYLINK Router` |
| Python 包名 | `mylink_router` |
| 命令行命令 | `mylink` |
| URI 协议名 | `mylink://` |
| 配置文件名 | `mylink.<host>.yml` |

例如：

```text
mylink://demo/
```

会查找：

```text
mylink.demo.yml
```

---

## 配置文件示例

一个最小配置文件可以这样写：

```yaml
CONFIG:
  index: "index.py"
  entrypoint: "init"
  service_path: "."
```

字段说明：

| 字段 | 说明 |
|---|---|
| `index` | 本地服务入口 Python 文件 |
| `entrypoint` | 需要调用的入口函数名 |
| `service_path` | 实际项目或服务目录 |

对应的 `index.py` 可以这样写：

```python
from pathlib import Path


def init(service_path: Path, parse_result):
    print("MYLINK service started")
    print("Service path:", service_path)
    print("URI:", parse_result.geturl())
```

---

## URI 示例

基础路由：

```text
mylink://demo/
```

开发模式查找：

```bash
mylink dev demo
```

Postbox 消息：

```text
mylink://demo/#post
```

具体行为由项目配置文件和入口函数决定。

---

## 推荐项目结构

一个更干净的项目结构可以整理成：

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

建议忽略这些本地文件：

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

## 安装方式

> 当前项目仍处于早期整理阶段，正式安装方式可能会在第一个稳定版本前调整。

克隆项目：

```bash
git clone https://github.com/<your-name>/mylink-router.git
cd mylink-router
```

创建虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果后续完成 Python 包配置，可以使用：

```bash
pip install -e .
```

---

## 注册 Windows URI 协议

为了让 Windows 能识别并打开：

```text
mylink://demo/
```

需要在注册表中注册 `mylink` 协议。

示例：

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\mylink]
@="URL:MYLINK Router Protocol"
"URL Protocol"=""

[HKEY_CLASSES_ROOT\mylink\shell\open\command]
@="\"python\" \"C:\\path\\to\\mylink-router\\mylinkuri.py\" \"%1\""
```

请把路径替换成你自己电脑中的实际路径。

---

## 当前状态

MYLINK Router 目前还是一个实验性的个人工具，并且仍处于持续开发阶段。

项目的核心想法已经明确，但实现还在继续整理中。当前重点包括：

- 收口并标准化入口；
- 分离私有配置和源码；
- 优化异常处理；
- 增加基础测试；
- 提供可复现的 demo 项目；
- 整理安装和注册流程；
- 完善 `.postbox` 及相关本地工作流的行为说明。

---

## 路线图

计划中的改进：

- [ ] 整理为 `mylink_router/` 标准包结构；
- [ ] 添加 `pyproject.toml`；
- [ ] 提供 `mylink` 命令行入口；
- [ ] 提供安全的 Windows 协议注册脚本；
- [ ] 添加 examples 示例项目；
- [ ] 添加 URI 解析和配置查找测试；
- [ ] 优化缓存失效机制；
- [ ] 优化错误提示；
- [ ] 完善 `.postbox` 行为说明；
- [ ] 研究与 Everything 集成，提高本地搜索速度。

---

## 安全说明

MYLINK Router 可以执行本地 Python 入口函数。这个能力很方便，但也意味着配置文件和入口脚本必须可信。

建议遵守以下规则：

- 不运行未知来源的 `mylink.<host>.yml`；
- 不执行不可信目录里的脚本；
- 不把个人路径、私有配置提交到公开仓库；
- 导入注册表文件前先检查内容；
- 不提交 `.data/`、`.postbox/`、`.testbox/` 和私有配置文件。

---

## License / 许可证

This project is released under the MIT License.  
本项目基于 MIT License 发布。
