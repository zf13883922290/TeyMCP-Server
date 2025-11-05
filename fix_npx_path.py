#!/usr/bin/env python3
"""
修复 servers.yaml 中的 npx 路径
"""

import re

config_file = '/home/sun/TeyMCP-Server/config/servers.yaml'
npx_full_path = '/home/sun/TeyMCP-Server/.local/bin/npx'

# 读取配置文件
with open(config_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 command: npx 为完整路径
content = re.sub(r'^(\s+command:\s+)npx$', rf'\1{npx_full_path}', content, flags=re.MULTILINE)

# 写回配置文件
with open(config_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已将所有 'command: npx' 替换为 'command: {npx_full_path}'")
