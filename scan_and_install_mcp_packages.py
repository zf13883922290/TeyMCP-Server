#!/usr/bin/env python3
"""
MCP 包扫描和自动安装脚本
扫描 docs/ 文件夹中提到的所有 MCP 服务器包，检查可用性并自动配置
"""

import subprocess
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# 当前已配置的服务器
CURRENT_SERVERS_FILE = Path("config/servers.yaml")
DOCS_FOLDER = Path("docs")

# MCP 相关包的模式
MCP_PACKAGE_PATTERNS = [
    r'@[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]*mcp[a-zA-Z0-9_-]*',  # @xxx/xxx-mcp-xxx
    r'@modelcontextprotocol/server-[a-zA-Z0-9_-]+',     # 官方服务器
    r'[a-zA-Z0-9_-]*-mcp-[a-zA-Z0-9_-]*',               # xxx-mcp-xxx
    r'mcp-[a-zA-Z0-9_-]+',                               # mcp-xxx
]

def extract_packages_from_docs() -> Set[str]:
    """从文档中提取所有提到的 MCP 包"""
    packages = set()
    
    for md_file in DOCS_FOLDER.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            
            # 使用多个模式匹配
            for pattern in MCP_PACKAGE_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                packages.update(matches)
            
            # 特殊处理：提取 npx -y 后面的包名
            npx_matches = re.findall(r'npx\s+-y\s+([a-zA-Z0-9@/_-]+)', content)
            packages.update(npx_matches)
            
        except Exception as e:
            print(f"⚠️  读取 {md_file} 失败: {e}")
    
    return packages

def clean_package_names(packages: Set[str]) -> List[str]:
    """清理和过滤包名"""
    cleaned = set()
    
    # 排除的模式
    exclude_patterns = [
        r'@localhost',
        r'@types/',
        r'@microsoft/microsoft-graph',
        r'@microsoft/tsdoc',
        r'@microsoft/applicationinsights',
        r'@azure/msal',
        r'@azure/identity',
        r'@babel/',
        r'@grpc/',
        r'@ai-sdk/',
        r'@mastra/core',
        r'@cap-js/',
        r'@ui5/',
        r'@sap-ux/',
        r'@wordbricks/fetch',
    ]
    
    for pkg in packages:
        # 移除版本号
        pkg = re.sub(r'@[\d.]+$', '', pkg)
        pkg = re.sub(r'@latest$', '', pkg)
        
        # 检查是否应该排除
        should_exclude = any(re.match(pattern, pkg) for pattern in exclude_patterns)
        
        if not should_exclude and len(pkg) > 3:
            cleaned.add(pkg)
    
    return sorted(list(cleaned))

def check_npm_package(package: str) -> Tuple[bool, str, str]:
    """检查 npm 包是否存在"""
    try:
        result = subprocess.run(
            ['npm', 'view', package, 'version', 'description'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            version = lines[0] if len(lines) > 0 else ''
            description = lines[1] if len(lines) > 1 else ''
            return True, version, description
        else:
            return False, '', ''
    except Exception as e:
        return False, '', str(e)

def load_current_servers() -> Set[str]:
    """加载当前已配置的服务器"""
    try:
        with open(CURRENT_SERVERS_FILE) as f:
            config = yaml.safe_load(f)
            servers = config.get('servers', {})
            
            # 提取所有使用的包名
            packages = set()
            for server_name, server_config in servers.items():
                args = server_config.get('args', [])
                for arg in args:
                    # 提取包名
                    if '@' in arg or 'mcp' in arg.lower():
                        packages.add(arg.strip())
            
            return packages
    except Exception as e:
        print(f"⚠️  读取配置文件失败: {e}")
        return set()

def main():
    print("=" * 80)
    print("🔍 MCP 包扫描和自动安装工具")
    print("=" * 80)
    print()
    
    # 1. 从文档中提取包名
    print("📖 步骤 1: 扫描 docs/ 文件夹...")
    raw_packages = extract_packages_from_docs()
    print(f"   找到 {len(raw_packages)} 个原始包引��")
    
    # 2. 清理包名
    print("\n🧹 步骤 2: 清理和过滤包名...")
    packages = clean_package_names(raw_packages)
    print(f"   过滤后剩余 {len(packages)} 个有效包")
    
    # 3. 加载当前配置
    print("\n📋 步骤 3: 检查当前配置...")
    current_packages = load_current_servers()
    print(f"   当前已配置 {len(current_packages)} 个包")
    
    # 4. 找出缺失的包
    print("\n🔎 步骤 4: 识别缺失的包...")
    missing_packages = []
    for pkg in packages:
        # 检查是否已在配置中
        is_configured = any(pkg in current for current in current_packages)
        if not is_configured:
            missing_packages.append(pkg)
    
    print(f"   发现 {len(missing_packages)} 个未配置的包")
    
    # 5. 验证包可用性
    print("\n✅ 步骤 5: 验证包可用性...")
    print()
    
    available_packages = []
    unavailable_packages = []
    
    for i, pkg in enumerate(missing_packages, 1):
        print(f"   [{i}/{len(missing_packages)}] 检查 {pkg}...", end=' ')
        
        exists, version, description = check_npm_package(pkg)
        
        if exists:
            print(f"✅ v{version}")
            available_packages.append({
                'name': pkg,
                'version': version,
                'description': description
            })
        else:
            print("❌ 不存在")
            unavailable_packages.append(pkg)
    
    # 6. 生成报告
    print("\n" + "=" * 80)
    print("📊 扫描结果总结")
    print("=" * 80)
    print()
    
    print(f"✅ 可用的新包: {len(available_packages)}")
    for pkg_info in available_packages:
        print(f"   • {pkg_info['name']} (v{pkg_info['version']})")
        if pkg_info['description']:
            print(f"     {pkg_info['description'][:70]}...")
    
    print(f"\n❌ 不可用的包: {len(unavailable_packages)}")
    for pkg in unavailable_packages[:10]:  # 只显示前10个
        print(f"   • {pkg}")
    if len(unavailable_packages) > 10:
        print(f"   ... 还有 {len(unavailable_packages) - 10} 个")
    
    # 7. 保存结果到文件
    report_file = Path("docs/MCP_PACKAGE_SCAN_REPORT.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# MCP 包扫描报告\n\n")
        f.write(f"扫描日期: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n\n")
        
        f.write("## 📊 统计信息\n\n")
        f.write(f"- 文档中提到的包: {len(packages)}\n")
        f.write(f"- 当前已配置: {len(current_packages)}\n")
        f.write(f"- 未配置的包: {len(missing_packages)}\n")
        f.write(f"- 可用的新包: {len(available_packages)}\n")
        f.write(f"- 不可用的包: {len(unavailable_packages)}\n\n")
        
        f.write("## ✅ 可用的新 MCP 包\n\n")
        for pkg_info in available_packages:
            f.write(f"### {pkg_info['name']}\n\n")
            f.write(f"- **版本**: {pkg_info['version']}\n")
            f.write(f"- **描述**: {pkg_info['description']}\n")
            f.write(f"- **安装**: `npm install {pkg_info['name']}`\n")
            f.write(f"- **使用**: `npx -y {pkg_info['name']}`\n\n")
        
        f.write("## ❌ 不可用的包\n\n")
        for pkg in unavailable_packages:
            f.write(f"- `{pkg}`\n")
        
        f.write("\n## 📝 建议配置\n\n")
        f.write("以下是可以添加到 `config/servers.yaml` 的配置:\n\n")
        f.write("```yaml\n")
        for pkg_info in available_packages[:5]:  # 只显示前5个作为示例
            server_name = pkg_info['name'].split('/')[-1].replace('-mcp', '').replace('mcp-', '')
            f.write(f"  {server_name}:\n")
            f.write(f"    server_type: stdio\n")
            f.write(f"    command: /home/sun/TeyMCP-Server/.local/bin/npx\n")
            f.write(f"    args:\n")
            f.write(f"      - \"-y\"\n")
            f.write(f"      - \"{pkg_info['name']}\"\n")
            f.write(f"    enabled: false\n")
            f.write(f"    critical: false\n")
            f.write(f"    description: \"{pkg_info['description'][:60]}...\"\n")
            f.write(f"\n")
        f.write("```\n")
    
    print(f"\n📄 详细报告已保存到: {report_file}")
    print()
    
    # 8. 询问是否自动添加
    if available_packages:
        print("=" * 80)
        print(f"💡 提示: 发现 {len(available_packages)} 个可用的新 MCP 包")
        print("   您可以手动查看报告文件并选择性地添加到 config/servers.yaml")
        print("=" * 80)

if __name__ == '__main__':
    main()
