# 🤝 贡献指南

感谢你有兴趣为 TeyMCP-Server 做出贡献！

---

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试](#测试)

---

## 📜 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：

- 使用友善和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---

## 🚀 如何贡献

### 报告Bug

发现Bug？请通过以下步骤报告：

1. 访问 [Issues](https://github.com/zf13883922290/TeyMCP-Server/issues)
2. 点击 "New Issue"
3. 选择 "Bug Report" 模板
4. 填写以下信息：
   - Bug描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息（Python版本、OS等）
   - 相关日志

### 建议新功能

有好的想法？欢迎提出：

1. 访问 [Issues](https://github.com/zf13883922290/TeyMCP-Server/issues)
2. 选择 "Feature Request" 模板
3. 描述功能需求和使用场景

### 提交代码

1. Fork 仓库
2. 创建特性分支
3. 进行开发
4. 提交Pull Request

---

## 💻 开发流程

### 1. 环境准备

```bash
# Fork并克隆仓库
git clone https://github.com/YOUR_USERNAME/TeyMCP-Server.git
cd TeyMCP-Server

# 添加上游仓库
git remote add upstream https://github.com/zf13883922290/TeyMCP-Server.git

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. 创建分支

```bash
# 更新主分支
git checkout main
git pull upstream main

# 创建特性分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关

### 3. 开发

```bash
# 运行开发服务器
uvicorn src.main:app --reload

# 在另一个终端运行测试
pytest --watch

# 代码格式化
black src/
isort src/

# 类型检查
mypy src/

# Lint检查
flake8 src/
```

### 4. 提交代码

```bash
# 添加更改
git add .

# 提交（遵循提交规范）
git commit -m "feat: add amazing feature"

# 推送到你的Fork
git push origin feature/your-feature-name
```

### 5. 创建Pull Request

1. 访问你的Fork仓库
2. 点击 "Compare & pull request"
3. 填写PR描述：
   - 简要说明更改内容
   - 相关Issue编号
   - 测试情况
   - 截图（如果有UI更改）

---

## 📝 代码规范

### Python代码规范

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范：

```python
# 好的示例
def calculate_average(numbers: List[int]) -> float:
    """
    计算数字列表的平均值
    
    Args:
        numbers: 整数列表
        
    Returns:
        平均值
    """
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


# 不好的示例
def calc(n):
    if not n:
        return 0
    return sum(n)/len(n)
```

### 文档字符串

使用Google风格的docstring：

```python
def function_name(param1: str, param2: int) -> bool:
    """
    函数简短描述
    
    详细描述（可选）
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
        
    Returns:
        返回值描述
        
    Raises:
        ValueError: 什么情况下抛出
    """
    pass
```

### 类型注解

强烈建议使用类型注解：

```python
from typing import List, Dict, Optional

def process_data(
    data: List[Dict[str, Any]], 
    threshold: Optional[int] = None
) -> List[str]:
    """处理数据"""
    pass
```

---

## 📨 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 示例

```bash
# 新功能
git commit -m "feat(api): add new endpoint for server management"

# Bug修复
git commit -m "fix(aggregator): resolve connection timeout issue"

# 文档更新
git commit -m "docs(readme): update installation instructions"

# 重构
git commit -m "refactor(core): simplify tool registry logic"
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_aggregator.py

# 查看覆盖率
pytest --cov=src tests/

# 生成HTML覆盖率报告
pytest --cov=src --cov-report=html tests/
```

### 编写测试

```python
# tests/test_example.py
import pytest
from src.core.aggregator import MCPAggregator

@pytest.fixture
def aggregator():
    """创建聚合器实例"""
    return MCPAggregator()

def test_add_server(aggregator):
    """测试添加服务器"""
    result = await aggregator.add_upstream_mcp(
        name="test-server",
        command="echo",
        args=["hello"]
    )
    assert result is True
    assert "test-server" in aggregator.upstream_clients
```

### 测试要求

- 新功能必须包含测试
- Bug修复必须包含回归测试
- 测试覆盖率不低于80%

---

## 📚 文档贡献

### 文档类型

- API文档 - `docs/API.md`
- 用户指南 - `docs/USER_GUIDE.md`
- 开发文档 - `docs/DEVELOPMENT.md`
- 部署文档 - `docs/DEPLOYMENT.md`

### 文档格式

- 使用Markdown格式
- 添加适当的标题层级
- 包含代码示例
- 添加截图（如果适用）

---

## 🎯 优先事项

当前优先级：

1. 🔴 高优先级
   - Bug修复
   - 安全问题
   - 性能优化

2. 🟡 中优先级
   - 新功能
   - 文档改进
   - 测试覆盖

3. 🟢 低优先级
   - 代码重构
   - UI美化
   - 小改进

---

## ✅ Pull Request检查清单

提交PR前，请确认：

- [ ] 代码遵循项目规范
- [ ] 已添加必要的测试
- [ ] 所有测试通过
- [ ] 已更新相关文档
- [ ] Commit信息符合规范
- [ ] 已同步最新的main分支
- [ ] PR描述清晰完整

---

## 🎉 成为贡献者

提交PR后：

1. 维护者会审核代码
2. 可能会有修改建议
3. 通过审核后会合并
4. 你的名字会出现在贡献者列表！

---

## 💬 获取帮助

需要帮助？

- 💡 [GitHub Discussions](https://github.com/zf13883922290/TeyMCP-Server/discussions)
- 📧 Email: support@example.com
- 💬 Discord: [加入社区](https://discord.gg/xxx)

---

## 🙏 感谢

感谢所有贡献者！你们让这个项目变得更好！

<div align="center">

[![Contributors](https://contrib.rocks/image?repo=zf13883922290/TeyMCP-Server)](https://github.com/zf13883922290/TeyMCP-Server/graphs/contributors)

</div>
