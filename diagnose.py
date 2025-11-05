#!/usr/bin/env python3
"""
TeyMCP-Server 诊断工具
"""

import requests
import sys
import time

def check_health():
    """检查服务器健康状态"""
    try:
        resp = requests.get('http://localhost:8080/health', timeout=2)
        if resp.status_code == 200:
            print("✅ 服务器健康检查: 通过")
            return True
        else:
            print(f"❌ 服务器健康检查: 失败 (状态码: {resp.status_code})")
            return False
    except Exception as e:
        print(f"❌ 服务器健康检查: 无法连接 ({e})")
        return False

def check_status():
    """检查服务器状态"""
    try:
        resp = requests.get('http://localhost:8080/api/status', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n📊 服务器状态:")
            print(f"  - 服务器数量: {len(data.get('servers', []))}")
            print(f"  - 工具数量: {data.get('tools_count', 0)}")
            print(f"  - 总调用: {data.get('metrics', {}).get('total_calls', 0)}")
            
            print(f"\n📋 已加载的服务器:")
            for server in data.get('servers', []):
                status_icon = "✅" if server['status'] == 'healthy' else "❌"
                print(f"  {status_icon} {server['name']}: {server['tools_count']} 个工具 ({server['status']})")
            return True
        else:
            print(f"❌ 无法获取状态 (状态码: {resp.status_code})")
            return False
    except Exception as e:
        print(f"❌ 无法获取状态: {e}")
        return False

def check_tools():
    """检查可用工具"""
    try:
        resp = requests.get('http://localhost:8080/api/tools', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n🔧 可用工具: {data.get('count', 0)} 个")
            tools = data.get('tools', [])
            if tools:
                print("\n工具列表:")
                for tool in tools[:10]:  # 只显示前10个
                    print(f"  - {tool['name']} (来自: {tool['server']})")
                if len(tools) > 10:
                    print(f"  ... 还有 {len(tools) - 10} 个工具")
            return True
        else:
            print(f"❌ 无法获取工具列表 (状态码: {resp.status_code})")
            return False
    except Exception as e:
        print(f"❌ 无法获取工具列表: {e}")
        return False

def main():
    print("=" * 50)
    print("TeyMCP-Server 诊断工具")
    print("=" * 50)
    print()
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    max_retries = 30
    for i in range(max_retries):
        if check_health():
            break
        time.sleep(1)
        sys.stdout.write(f"\r⏳ 等待中... {i+1}/{max_retries}")
        sys.stdout.flush()
    else:
        print("\n\n❌ 服务器启动超时")
        sys.exit(1)
    
    print("\n")
    
    # 检查状态
    time.sleep(2)
    status_ok = check_status()
    
    # 检查工具
    if status_ok:
        time.sleep(1)
        check_tools()
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
