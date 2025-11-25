# -*- coding: utf-8 -*-
"""
@author: kongkong 
@version: 3.2 (Fixed Icons via CDN)
@date: 2025-11-25
"""
import os
import html
import stat
from pathlib import Path

# --- 1. 配置项 (Configuration) ---
# 在这里修改你的设置
CONFIG = {
    # 要扫描的根目录 (建议使用正斜杠 '/' 或双反斜杠 '\\')
    "target_path": r'D:\\workplace',
    # 输出的 HTML 文件名
    "output_filename": '目录.html',
    # 初始加载时默认展开的目录深度 (1 表示只展开根目录)
    "default_expand_depth": 3,
    # 忽略配置
    "ignore": {
        "hidden_dirs": True,
        "hidden_files": True,
        "dir_names": {'.git', '.svn', '__pycache__', 'node_modules', '.vscode', '$RECYCLE.BIN', 'System Volume Information', 'dist', 'build'},
        "file_names": {'.DS_Store', 'thumbs.db'},
    }
}


# --- 辅助函数 (Helper Function) ---
def is_hidden(path):
    """跨平台检查文件或文件夹是否隐藏"""
    try:
        # 对 Windows 系统，检查文件属性
        if os.name == 'nt':
            return bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        # 对 Unix-like 系统 (macOS, Linux)，检查是否以 '.' 开头
        else:
            return path.name.startswith('.')
    except (OSError, FileNotFoundError):
        return False


# --- 2. HTML 模板 (HTML Template) ---
# [FIXED] 移除了手动定义的 @font-face，改为使用 CDN 链接
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>目录浏览器</title>
    <!-- 引入 Font Awesome 6.4.0 CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Custom Styles */
        :root {{
            --bg-main: #111827; --bg-card: #1F2937; --border: #374151;
            --text-main: #D1D5DB; --text-link: #9CA3AF; --text-link-hover: #E5E7EB;
            --primary: #22C55E; --secondary: #A3E635; --highlight: #86EFAC;
            --btn-bg: #374151; --btn-bg-hover: #4B5563;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ height: 100%; overflow: hidden; }}
        body {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background-color: var(--bg-main); color: var(--text-main);
            display: flex; justify-content: center; align-items: center; padding: 20px;
        }}
        .file-explorer {{
            width: 100%; max-width: 800px; height: 100%; max-height: 90vh;
            background-color: var(--bg-main); border: 1px solid var(--border);
            border-radius: 12px; display: flex; flex-direction: column;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5); overflow: hidden;
        }}
        .header-box {{
            padding: 20px; border-bottom: 1px solid var(--border);
            background-color: rgba(17, 24, 39, 0.95);
        }}
        .input-wrapper {{ position: relative; display: flex; align-items: center; }}
        .input-wrapper i {{ position: absolute; left: 12px; color: var(--secondary); }}
        #searchInput {{
            width: 100%; padding: 12px 12px 12px 40px; background-color: #1F2937;
            border: 1px solid var(--border); border-radius: 8px; color: var(--text-main);
            font-size: 14px; outline: none; transition: all 0.3s ease;
        }}
        #searchInput:focus {{
            border-color: var(--primary); box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);
        }}
        .controls {{ display: flex; gap: 10px; margin-top: 15px; }}
        .control-btn, .control-select {{
            flex-grow: 1; padding: 8px 12px; background-color: var(--btn-bg);
            color: var(--text-main); border: 1px solid var(--border); border-radius: 6px;
            cursor: pointer; transition: background-color 0.2s; font-size: 13px;
            -webkit-appearance: none; -moz-appearance: none; appearance: none;
        }}
        .control-btn:hover, .control-select:hover {{ background-color: var(--btn-bg-hover); }}
        .control-select {{
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239CA3AF' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.5rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 2.5rem;
        }}
        .tree-container {{
            flex: 1; padding: 10px 20px 20px 20px; overflow-y: auto;
        }}
        .tree-container::-webkit-scrollbar {{ width: 6px; }}
        .tree-container::-webkit-scrollbar-track {{ background: transparent; }}
        .tree-container::-webkit-scrollbar-thumb {{ background-color: var(--border); border-radius: 3px; }}
        ul {{ list-style-type: none; padding-left: 20px; }}
        .tree-root {{ padding-left: 0; }}
        li {{ margin: 2px 0; position: relative; }}
        .node-content {{
            display: flex; align-items: center; padding: 4px 8px;
            border-radius: 6px; transition: background 0.2s; user-select: none;
        }}
        .folder-node > .node-content {{ cursor: pointer; }}
        .node-content:hover {{ background-color: rgba(55, 65, 81, 0.5); }}
        .icon {{ margin-right: 10px; width: 20px; text-align: center; }} /* width adjusted for FA */
        .icon-folder {{ color: var(--primary); }}
        .icon-file {{ color: var(--text-main); opacity: 0.7; }}
        .item-name {{ text-decoration: none; color: var(--text-link); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        a.item-name:hover {{ color: var(--text-link-hover); }}
        .folder-content {{ display: none; }}
        .folder-open > .folder-content {{ display: block; }}
        .highlight-text {{ color: var(--highlight); font-weight: bold; background-color: rgba(134, 239, 172, 0.1); }}
        .hidden {{ display: none !important; }}
        .footer-box {{
            padding: 12px 20px; border-top: 1px solid var(--border);
            background-color: var(--bg-main); font-size: 12px; color: var(--text-link);
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="file-explorer">
        <div class="header-box">
            <div class="input-wrapper">
                <i class="fa-solid fa-search"></i>
                <input type="text" id="searchInput" placeholder="搜索文件或文件夹...">
            </div>
            <div class="controls">
                <select id="expandLevelSelect" class="control-select">
                    <option value="3">展开至 3 级</option>
                    <option value="4">展开至 4 级</option>
                    <option value="5">展开至 5 级</option>
                    <option value="999">全部展开</option>
                </select>
                <button id="collapseAllBtn" class="control-btn"><i class="fa-solid fa-compress-arrows-alt"></i>全部折叠</button>
            </div>
        </div>
        <div class="tree-container">
            <ul class="tree-root" id="fileTree">
                {file_tree}
            </ul>
        </div>
        <div class="footer-box">
            <p id="statsSummary">{stats_summary}</p>
        </div>
    </div>
    <script>
        const searchInput = document.getElementById('searchInput');
        const fileTree = document.getElementById('fileTree');
        const allNodes = fileTree.querySelectorAll('li');
        const allFolderNodes = fileTree.querySelectorAll('.folder-node');
        const allItemNames = fileTree.querySelectorAll('.item-name');
        const expandLevelSelect = document.getElementById('expandLevelSelect');
        const collapseAllBtn = document.getElementById('collapseAllBtn');

        function setFolderState(folderLi, isOpen) {{
            const icon = folderLi.querySelector('.icon-folder');
            folderLi.classList.toggle('folder-open', isOpen);
            if (icon) {{
                // 使用 toggle 切换 class，处理 Font Awesome 类名
                icon.classList.toggle('fa-folder-open', isOpen);
                icon.classList.toggle('fa-folder', !isOpen);
            }}
        }}

        function toggleFolder(element) {{
            const parentLi = element.closest('li.folder-node');
            if (parentLi) {{
                setFolderState(parentLi, !parentLi.classList.contains('folder-open'));
            }}
        }}

        function expandToLevel(targetLevel) {{
            const level = parseInt(targetLevel, 10);
            const isExpandAll = level >= 999;
            
            allFolderNodes.forEach(node => {{
                const nodeDepth = parseInt(node.dataset.depth, 10);
                // 根节点(depth=0)总是展开
                const shouldBeOpen = nodeDepth === 0 || isExpandAll || nodeDepth < level;
                setFolderState(node, shouldBeOpen);
            }});
        }}

        function collapseAll() {{
            allFolderNodes.forEach(node => {{
                // 只保持根目录(depth=0)展开
                setFolderState(node, node.dataset.depth === '0');
            }});
        }}

        function applySearch(filter) {{
            const isFilterEmpty = filter === '';
            allItemNames.forEach(item => {{ if (item.originalHTML) {{ item.innerHTML = item.originalHTML; item.originalHTML = null; }} }});

            allNodes.forEach(node => {{
                const itemNameEl = node.querySelector('.item-name');
                if (!itemNameEl) return;

                const isMatch = itemNameEl.textContent.toLowerCase().includes(filter);

                if (isFilterEmpty) {{
                    node.classList.remove('hidden');
                    if (node.classList.contains('folder-node')) {{
                        // 搜索清空后，恢复到默认展开深度
                        const defaultExpandDepth = {default_expand_depth};
                        const nodeDepth = parseInt(node.dataset.depth, 10);
                        setFolderState(node, nodeDepth < defaultExpandDepth);
                    }}
                }} else {{
                    if (isMatch) {{
                        node.classList.remove('hidden');
                        if (!itemNameEl.originalHTML) {{ itemNameEl.originalHTML = itemNameEl.innerHTML; }}
                        const regex = new RegExp(filter.replace(/[-\/\\^$*+?.()|[\\]{{}}]/g, '\\\\$&'), 'gi');
                        itemNameEl.innerHTML = itemNameEl.textContent.replace(regex, `<span class="highlight-text">$&</span>`);

                        let parent = node.parentElement;
                        while (parent && parent !== fileTree) {{
                            const parentLi = parent.closest('li.folder-node');
                            if (parentLi) {{
                                parentLi.classList.remove('hidden');
                                if (!parentLi.classList.contains('folder-open')) {{ setFolderState(parentLi, true); }}
                            }}
                            parent = parent.parentElement;
                        }}
                    }} else {{
                        node.classList.add('hidden');
                    }}
                }}
            }});
        }}

        searchInput.addEventListener('input', (e) => applySearch(e.target.value.toLowerCase().trim()));
        expandLevelSelect.addEventListener('change', (e) => expandToLevel(e.target.value));
        collapseAllBtn.addEventListener('click', collapseAll);
        
        // 初始化下拉框的选中状态以匹配默认展开深度
        expandLevelSelect.value = "{default_expand_depth}";
        // 页面加载后，根据默认深度展开
        expandToLevel("{default_expand_depth}");
    </script>
</body>
</html>
"""

# --- 3. 文件图标映射 (Icon Mapping) ---
# 这里的类名需要与 Font Awesome 6 兼容
ICON_MAP = {
    '.py': 'fa-brands fa-python', '.js': 'fa-brands fa-js-square', '.html': 'fa-brands fa-html5',
    '.css': 'fa-brands fa-css3-alt', '.json': 'fa-solid fa-file-code', '.xml': 'fa-solid fa-file-code',
    '.java': 'fa-brands fa-java', '.c': 'fa-solid fa-file-code', '.cpp': 'fa-solid fa-file-code',
    '.cs': 'fa-solid fa-file-code', '.txt': 'fa-solid fa-file-alt', '.md': 'fa-brands fa-markdown',
    '.pdf': 'fa-solid fa-file-pdf', '.doc': 'fa-solid fa-file-word', '.docx': 'fa-solid fa-file-word',
    '.xls': 'fa-solid fa-file-excel', '.xlsx': 'fa-solid fa-file-excel', '.ppt': 'fa-solid fa-file-powerpoint',
    '.pptx': 'fa-solid fa-file-powerpoint', '.png': 'fa-solid fa-file-image', '.jpg': 'fa-solid fa-file-image',
    '.jpeg': 'fa-solid fa-file-image', '.gif': 'fa-solid fa-file-image', '.svg': 'fa-solid fa-file-image',
    '.mp3': 'fa-solid fa-file-audio', '.wav': 'fa-solid fa-file-audio', '.mp4': 'fa-solid fa-file-video',
    '.avi': 'fa-solid fa-file-video', '.zip': 'fa-solid fa-file-archive', '.rar': 'fa-solid fa-file-archive',
    '.gz': 'fa-solid fa-file-archive', '.7z': 'fa-solid fa-file-archive',
    'default_file': 'fa-solid fa-file', 'default_folder': 'fa-solid fa-folder'
}

def get_icon_class(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ICON_MAP.get(ext, ICON_MAP['default_file'])

# --- 4. 目录树生成器 (Directory Tree Generator) ---
class DirectoryTreeGenerator:
    def __init__(self, config):
        self.config = config
        self.ignore_config = config.get("ignore", {})
        self.ignore_hidden_dirs = self.ignore_config.get("hidden_dirs", False)
        self.ignore_hidden_files = self.ignore_config.get("hidden_files", False)
        self.ignore_dir_names = self.ignore_config.get("dir_names", set())
        self.ignore_file_names = self.ignore_config.get("file_names", set())
        self.default_expand_depth = config.get("default_expand_depth", 3)
        self.folder_count = 0
        self.file_count = 0

    def generate_tree_html(self, root_path_str):
        root_path = Path(root_path_str)
        if not root_path.exists() or not root_path.is_dir():
            return f'<li><div class="node-content"><i class="fa-solid fa-ban icon" style="color: #ef4444;"></i><span class="item-name" style="color: #ef4444;">错误：根目录 "{html.escape(root_path_str)}" 不存在或不是一个目录。</span></div></li>'

        # 根目录总是展开
        folder_class = "folder-node folder-open"
        icon_class = f'{ICON_MAP["default_folder"]}-open'
        
        html_parts = [f'<li class="{folder_class}" data-depth="0">']
        html_parts.append('<div class="node-content" onclick="toggleFolder(this)">')
        root_name = html.escape(root_path.name or str(root_path))
        html_parts.append(f'<i class="fa-solid {icon_class} icon icon-folder"></i>')
        html_parts.append(f'<span title="{html.escape(str(root_path))}" class="item-name">{root_name}</span>')
        html_parts.append('</div>')
        
        html_parts.append('<ul class="folder-content">')
        html_parts.append(self._build_dir_html_recursive(root_path, depth=1))
        html_parts.append('</ul></li>')
        return "".join(html_parts)

    def _build_dir_html_recursive(self, current_path, depth):
        html_parts = []
        
        try:
            # 排序：文件夹在前，文件在后，然后按名称排序
            entries = sorted(current_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return '<li><div class="node-content"><i class="fa-solid fa-ban icon" style="color: #ef4444;"></i><span class="item-name" style="color: #ef4444;">无访问权限</span></div></li>'

        for entry in entries:
            if entry.is_dir():
                if (self.ignore_hidden_dirs and is_hidden(entry)) or entry.name in self.ignore_dir_names:
                    continue
                self.folder_count += 1
                
                is_expanded = depth < self.default_expand_depth
                folder_class = "folder-node folder-open" if is_expanded else "folder-node"
                icon_class = f'{ICON_MAP["default_folder"]}-open' if is_expanded else ICON_MAP["default_folder"]
                
                html_parts.append(f'<li class="{folder_class}" data-depth="{depth}">')
                html_parts.append('<div class="node-content" onclick="toggleFolder(this)">')
                html_parts.append(f'<i class="fa-solid {icon_class} icon icon-folder"></i>')
                html_parts.append(f'<span title="{html.escape(str(entry))}" class="item-name">{html.escape(entry.name)}</span>')
                html_parts.append('</div>')
                html_parts.append('<ul class="folder-content">')
                html_parts.append(self._build_dir_html_recursive(entry, depth + 1))
                html_parts.append('</ul></li>')
            else: # 是文件
                if (self.ignore_hidden_files and is_hidden(entry)) or entry.name in self.ignore_file_names:
                    continue
                self.file_count += 1
                
                icon_class = get_icon_class(entry.name)
                
                html_parts.append(f'<li class="file-node" data-depth="{depth}">')
                html_parts.append('<div class="node-content">')
                html_parts.append(f'<i class="{icon_class} icon icon-file"></i>')
                # 使用 as_uri() 生成标准的 file:/// 链接
                html_parts.append(f'<a href="{entry.as_uri()}" target="_blank" title="{html.escape(str(entry))}" class="item-name">{html.escape(entry.name)}</a>')
                html_parts.append('</div></li>')
                
        return "".join(html_parts)

# --- 5. 主执行模块 (Main Execution) ---
if __name__ == "__main__":
    print("开始生成目录树 HTML...")
    
    # 创建生成器实例
    generator = DirectoryTreeGenerator(CONFIG)
    
    # 生成目录树 HTML
    file_tree_html = generator.generate_tree_html(CONFIG["target_path"])
    
    # 生成统计信息
    stats_summary_text = f"共 {generator.folder_count} 个文件夹, {generator.file_count} 个文件。"
    
    # 填充模板
    final_html = HTML_TEMPLATE.format(
        file_tree=file_tree_html,
        stats_summary=stats_summary_text,
        default_expand_depth=CONFIG["default_expand_depth"]
    )
    
    # 写入文件
    output_filename = CONFIG["output_filename"]
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"✓ 成功！文件已保存为: {os.path.abspath(output_filename)}")
        print("  注意：图标显示需要连接互联网加载 CDN。")
    except IOError as e:
        print(f"✗ 错误：无法写入文件 {output_filename}。原因: {e}")
