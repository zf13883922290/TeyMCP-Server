#!/bin/bash
# GPU 功能测试脚本

set -e

cd "$(dirname "$0")"

echo "======================================"
echo "  TeyMCP-Server GPU 测试工具"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试结果统计
PASSED=0
FAILED=0
TOTAL=0

# 测试函数
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TOTAL=$((TOTAL + 1))
    echo -e "${BLUE}[测试 $TOTAL]${NC} $test_name"
    
    if eval "$test_command" &> /dev/null; then
        echo -e "${GREEN}✅ 通过${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ 失败${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
    echo ""
}

# 1. 基础检查
echo -e "${YELLOW}═══ 第一部分: 基础检查 ═══${NC}"
echo ""

run_test "Docker 服务运行" "docker ps &> /dev/null"
run_test "容器正在运行" "docker ps | grep teymcp-server-gpu"
run_test "主服务端口响应" "curl -s -f http://localhost:1215/health"
echo ""

# 2. GPU 检查
echo -e "${YELLOW}═══ 第二部分: GPU 检查 ═══${NC}"
echo ""

run_test "宿主机 GPU 可见" "nvidia-smi"
run_test "容器内 GPU 可见" "docker exec teymcp-server-gpu nvidia-smi"
run_test "CUDA 环境变量" "docker exec teymcp-server-gpu printenv | grep NVIDIA"
echo ""

# 3. GPU 功能测试
echo -e "${YELLOW}═══ 第三部分: GPU 功能测试 ═══${NC}"
echo ""

echo -e "${BLUE}[测试]${NC} GPU 信息查询"
docker exec teymcp-server-gpu nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
echo ""

echo -e "${BLUE}[测试]${NC} CUDA 可用性检查"
docker exec teymcp-server-gpu python3 -c "
try:
    import torch
    print(f'PyTorch 版本: {torch.__version__}')
    print(f'CUDA 可用: {torch.cuda.is_available()}')
    if torch.cuda.is_available():
        print(f'CUDA 版本: {torch.version.cuda}')
        print(f'GPU 数量: {torch.cuda.device_count()}')
        print(f'GPU 名称: {torch.cuda.get_device_name(0)}')
except ImportError:
    print('PyTorch 未安装（可选）')
except Exception as e:
    print(f'检查失败: {e}')
" 2>/dev/null || echo -e "${YELLOW}⚠️  PyTorch 未安装（可选依赖）${NC}"
echo ""

# 4. MCP 服务测试
echo -e "${YELLOW}═══ 第四部分: MCP 服务测试 ═══${NC}"
echo ""

echo -e "${BLUE}[测试]${NC} API 状态查询"
if curl -s http://localhost:1215/api/status | jq -e . &> /dev/null; then
    echo -e "${GREEN}✅ API 响应正常${NC}"
    PASSED=$((PASSED + 1))
    
    # 显示启用的服务器
    echo ""
    echo "启用的 MCP 服务器:"
    curl -s http://localhost:1215/api/status | jq -r '.servers | to_entries[] | select(.value.enabled) | "  - \(.key): \(.value.status)"'
else
    echo -e "${RED}❌ API 响应失败${NC}"
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

echo -e "${BLUE}[测试]${NC} 工具列表查询"
tool_count=$(curl -s http://localhost:1215/api/tools | jq '. | length' 2>/dev/null || echo "0")
if [ "$tool_count" -gt 0 ]; then
    echo -e "${GREEN}✅ 发现 $tool_count 个工具${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ 未发现任何工具${NC}"
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# 5. GPU 加速服务测试（可选）
echo -e "${YELLOW}═══ 第五部分: GPU 加速服务测试 ═══${NC}"
echo ""

# 检查 Ollama 是否启用
if docker ps | grep ollama-gpu &> /dev/null; then
    echo -e "${BLUE}[测试]${NC} Ollama GPU 服务"
    
    if curl -s http://localhost:11434/api/version &> /dev/null; then
        echo -e "${GREEN}✅ Ollama 服务运行中${NC}"
        ollama_version=$(curl -s http://localhost:11434/api/version | jq -r .version)
        echo "  版本: $ollama_version"
        PASSED=$((PASSED + 1))
        
        # 测试模型列表
        echo ""
        echo "已安装的模型:"
        docker exec ollama-gpu ollama list 2>/dev/null || echo "  暂无模型"
    else
        echo -e "${RED}❌ Ollama 服务无响应${NC}"
        FAILED=$((FAILED + 1))
    fi
    TOTAL=$((TOTAL + 1))
else
    echo -e "${YELLOW}⚠️  Ollama 服务未启用（可选）${NC}"
fi
echo ""

# 6. 端口测试
echo -e "${YELLOW}═══ 第六部分: 端口测试 ═══${NC}"
echo ""

run_test "端口 1215 监听" "sudo netstat -tlnp | grep 1215"
run_test "端口 1215 可访问" "curl -s -f http://localhost:1215/health"
echo ""

# 7. 资源使用情况
echo -e "${YELLOW}═══ 第七部分: 资源使用情况 ═══${NC}"
echo ""

echo -e "${BLUE}[信息]${NC} GPU 使用情况:"
docker exec teymcp-server-gpu nvidia-smi --query-gpu=index,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "获取失败"
echo ""

echo -e "${BLUE}[信息]${NC} 容器资源使用:"
docker stats --no-stream teymcp-server-gpu 2>/dev/null || echo "获取失败"
echo ""

# 8. 日志检查
echo -e "${YELLOW}═══ 第八部分: 日志检查 ═══${NC}"
echo ""

echo -e "${BLUE}[信息]${NC} 最近的日志（最后 10 行）:"
docker logs --tail 10 teymcp-server-gpu 2>&1
echo ""

# 检查错误
error_count=$(docker logs teymcp-server-gpu 2>&1 | grep -i "error" | wc -l)
if [ "$error_count" -eq 0 ]; then
    echo -e "${GREEN}✅ 日志中无错误${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${YELLOW}⚠️  日志中发现 $error_count 个错误${NC}"
    echo "最近的错误:"
    docker logs teymcp-server-gpu 2>&1 | grep -i "error" | tail -5
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))
echo ""

# 测试总结
echo "======================================"
echo "  📊 测试结果总结"
echo "======================================"
echo ""
echo -e "总测试数: $TOTAL"
echo -e "${GREEN}通过: $PASSED${NC}"
echo -e "${RED}失败: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！GPU 功能正常！${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  有 $FAILED 个测试失败，请检查详细信息${NC}"
    echo ""
    echo "故障排除建议:"
    echo "1. 查看完整日志: docker logs teymcp-server-gpu"
    echo "2. 检查 GPU 驱动: nvidia-smi"
    echo "3. 重新配置: sudo bash install_nvidia_container_toolkit.sh"
    echo "4. 重启服务: docker-compose restart"
    echo "5. 查看文档: docs/GPU_SETUP.md"
    exit 1
fi
