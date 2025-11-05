#!/bin/bash
#
# TeyMCP-Server 发布打包脚本
# 生成完整的项目压缩包供GitHub Release使用
#

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 项目信息
VERSION="v1.0.0"
PROJECT_NAME="TeyMCP-Server"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="${PROJECT_NAME}_Complete_${VERSION}"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  TeyMCP-Server 发布打包工具${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 进入项目根目录
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo -e "${CYAN}📦 项目路径:${NC} $PROJECT_ROOT"
echo -e "${CYAN}📦 版本号:${NC} $VERSION"
echo -e "${CYAN}📦 包名:${NC} $PACKAGE_NAME"
echo ""

# 创建临时目录
TEMP_DIR="/tmp/${PACKAGE_NAME}"
echo -e "${YELLOW}🗂️  创建临时目录...${NC}"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 复制项目文件
echo -e "${YELLOW}📂 复制项目文件...${NC}"
rsync -a \
    --exclude='venv' \
    --exclude='.local' \
    --exclude='.cache' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='.gitignore' \
    --exclude='data/logs/*' \
    --exclude='data/metrics/*' \
    --exclude='*.log' \
    --exclude='node_modules' \
    --exclude='.env' \
    --exclude='nohup.out' \
    --exclude='*.tar.gz' \
    --exclude='*.zip' \
    ./ "$TEMP_DIR/"

echo "  ✓ 源代码 (src/)"
echo "  ✓ 配置模板 (config/)"
echo "  ✓ 安装脚本 (scripts/)"
echo "  ✓ 文档 (docs/)"
echo "  ✓ README、License等"

# 创建空目录
mkdir -p "$TEMP_DIR/data/logs"
mkdir -p "$TEMP_DIR/data/metrics"
mkdir -p "$TEMP_DIR/.local"
mkdir -p "$TEMP_DIR/.cache"

# 创建安装说明
echo -e "${YELLOW}📝 创建INSTALL.txt...${NC}"
cat > "$TEMP_DIR/INSTALL.txt" << 'INSTALLEOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             TeyMCP-Server 安装说明                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📦 系统要求
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Python 3.10 或更高版本
  • Ubuntu 20.04+ / Debian 11+ / macOS
  • 最低512MB内存 (推荐2GB+)
  • 1GB可用磁盘空间

🚀 快速安装 (推荐)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 解压文件
   tar -xzf TeyMCP-Server_Complete_*.tar.gz
   cd TeyMCP-Server

2. 运行安装脚本
   bash scripts/install.sh

   脚本会自动:
   • 创建Python虚拟环境
   • 下载并安装本地Node.js
   • 安装所有依赖包
   • 生成配置文件

3. 配置环境变量 (可选)
   nano config/.env
   # 填入你的API密钥(如GitHub Token等)

4. 启动服务
   ./start.sh

5. 访问管理面板
   打开浏览器: http://localhost:8081

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 手动安装 (高级用户)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate

2. 安装依赖
   pip install -r requirements.txt

3. 启动服务
   python src/main.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 常用命令
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

激活环境:     source env.sh
启动服务:     ./start.sh
后台运行:     nohup ./start.sh > /tmp/teymcp.log 2>&1 &
查看日志:     tail -f data/logs/teymcp.log
停止服务:     pkill -f "python.*main.py"
检查状态:     curl http://localhost:8081/api/status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • README.md - 项目介绍
  • docs/QUICKSTART.md - 快速入门
  • docs/CONFIGURATION.md - 配置指南
  • docs/TROUBLESHOOTING.md - 故障排查
  • docs/API.md - API文档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 遇到问题?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • GitHub Issues: 
    https://github.com/zf13883922290/TeyMCP-Server/issues

  • 查看日志:
    tail -100 data/logs/teymcp.log

  • 检查端口:
    lsof -i :8081

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ 感谢使用 TeyMCP-Server!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTALLEOF

# 创建版本信息
echo -e "${YELLOW}📝 创建VERSION.txt...${NC}"
cat > "$TEMP_DIR/VERSION.txt" << EOF
TeyMCP-Server $VERSION
Build Date: $(date)
Author: zf13883922290
GitHub: https://github.com/zf13883922290/TeyMCP-Server
License: MIT

完全隔离的MCP聚合服务器
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ 特性:
  • 完全隔离的虚拟环境 (Python venv + 本地Node.js)
  • 统一的RESTful API接口
  • 实时Web管理面板
  • 灵活的YAML配置
  • 开箱即用的一键安装

📦 包含内容:
  ✓ 完整源代码 (src/)
  ✓ 配置文件模板 (config/)
  ✓ 自动化安装脚本 (scripts/)
  ✓ Docker配置 (docker/)
  ✓ 完整文档 (docs/)
  ✓ README、License等

🚀 快速开始:
  1. 解压: tar -xzf TeyMCP-Server_Complete_*.tar.gz
  2. 安装: bash scripts/install.sh
  3. 配置: nano config/.env (可选)
  4. 启动: ./start.sh
  5. 访问: http://localhost:8081

EOF

# 打包
echo ""
echo -e "${YELLOW}📦 创建压缩包...${NC}"
cd /tmp
tar -czf "${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}/"

# 移动到项目目录
mv "${PACKAGE_NAME}.tar.gz" "$PROJECT_ROOT/"

# 计算文件大小和哈希
PACKAGE_PATH="$PROJECT_ROOT/${PACKAGE_NAME}.tar.gz"
FILE_SIZE=$(du -h "$PACKAGE_PATH" | cut -f1)
FILE_HASH=$(sha256sum "$PACKAGE_PATH" | cut -d' ' -f1)

# 清理临时文件
rm -rf "$TEMP_DIR"

# 显示总结
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║                   ✅ 打包完成!                              ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📦 发布包信息:${NC}"
echo "  文件名: ${PACKAGE_NAME}.tar.gz"
echo "  大小: $FILE_SIZE"
echo "  SHA256: $FILE_HASH"
echo "  路径: $PACKAGE_PATH"
echo ""
echo -e "${CYAN}📤 发布步骤:${NC}"
echo "  1. 在GitHub创建新Release"
echo "  2. 上传文件: ${PACKAGE_NAME}.tar.gz"
echo "  3. 填写Release Notes"
echo ""
echo -e "${CYAN}🔗 用户下载后使用:${NC}"
echo "  ${YELLOW}tar -xzf ${PACKAGE_NAME}.tar.gz${NC}"
echo "  ${YELLOW}cd TeyMCP-Server${NC}"
echo "  ${YELLOW}bash scripts/install.sh${NC}"
echo "  ${YELLOW}./start.sh${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
