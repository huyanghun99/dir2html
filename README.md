
# 📂 dir2html

> 一个轻量级的 Python 脚本，用于扫描本地目录并生成带有现代化深色 UI、支持搜索和折叠的交互式 HTML 目录树文件。

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

## 📖 简介

这个工具旨在帮助开发者、文档编写者或系统管理员快速生成文件结构的概览。它将指定目录下的所有文件和文件夹递归扫描，并输出为一个**单文件 HTML**。

生成的 HTML 包含内嵌的 CSS 和 JavaScript，无需联网（除非需要加载字体图标缓存），具备即时搜索、展开/折叠控制和语法高亮风格的界面。
<img width="904" height="392" alt="image" src="https://github.com/user-attachments/assets/9d82e8cb-86b9-460a-9a6e-7bfd93294202" />

## ✨ 主要功能

*   **无需依赖**：仅使用 Python 标准库 (`os`, `html`, `pathlib`, `string`)，无需 `pip install`。
*   **单文件输出**：生成的 HTML 文件包含所有样式和脚本，便于分发和共享。
*   **现代化 UI**：
    *   深色模式（Dark Mode）设计，保护视力。
    *   基于文件类型的图标显示（使用 Font Awesome）。
    *   响应式布局。
*   **交互功能**：
    *   **实时搜索**：支持文件名/文件夹名搜索，自动展开匹配路径并高亮关键词。
    *   **层级控制**：一键展开至指定层级（3级、4级、5级或全部展开）。
    *   **折叠/展开**：点击文件夹图标即可切换状态。
*   **智能过滤**：自动识别并隐藏系统文件、隐藏文件夹以及常见的开发垃圾文件（如 `node_modules`, `.git` 等）。
*   **跨平台**：兼容 Windows 和 Unix-like 系统（Linux/macOS）。

## 🚀 快速开始

### 环境要求
*   Python 3.6+

### 使用步骤

1.  **下载脚本**：将本仓库的代码保存为 `scan_dir.py`（或其他名称）。
2.  **配置路径**：
    打开脚本，找到 `CONFIG` 字典，修改 `target_path` 为你想要扫描的文件夹路径：
    ```python
    CONFIG = {
        "target_path": 'D:/你的/目标/文件夹',
        # ... 其他配置
    }
    ```
3.  **运行脚本**：
    在终端或命令行中运行：
    ```bash
    python scan_dir.py
    ```
4.  **查看结果**：
    脚本运行完成后，会在当前目录下生成 `目录_v3.2.html`（文件名可在配置中修改），双击即可在浏览器中打开。

## ⚙️ 配置说明

脚本顶部的 `CONFIG` 变量允许你自定义扫描行为：

| 配置项 | 说明 | 默认值 / 示例 |
| :--- | :--- | :--- |
| `target_path` | **[必填]** 要扫描的根目录路径。建议使用 `/` 或 `\\`。 | `'D:/APP DATA'` |
| `output_filename` | 输出的 HTML 文件名称。 | `'目录_v3.2.html'` |
| `default_expand_depth`| 打开 HTML 时默认展开的层级深度。 | `3` |
| `ignore.hidden_dirs` | 是否忽略隐藏文件夹。 | `True` |
| `ignore.hidden_files` | 是否忽略隐藏文件。 | `True` |
| `ignore.dir_names` | 要完全忽略的文件夹名称集合（支持 `.git`, `node_modules` 等）。 | `{'.git', '__pycache__', ...}` |
| `ignore.file_names` | 要完全忽略的文件名称集合。 | `{'.DS_Store', 'thumbs.db'}` |


## 📄 许可证

本项目基于 MIT 许可证开源。
