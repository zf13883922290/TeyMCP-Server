# 🗄️ TeyMCP-Server 数据库配置实战指南

## 📊 当前数据库环境

### PostgreSQL 14.19
- **状态**: ✅ 运行中
- **端口**: 5432
- **数据库列表**:
  - `ai_sales` - AI销售数据库 (有专用用户 ai_sales_user)
  - `km_ai_admin` - 知识管理AI管理数据库
  - `postgres` - 默认数据库
  
### MySQL 8.0.43
- **状态**: ✅ 运行中
- **端口**: 3306, 33060

---

## 🚀 快速配置步骤

### 步骤1: 为 MCP 创建只读数据库用户

#### PostgreSQL 只读用户 (推荐)

```bash
# 创建只读用户
sudo -u postgres psql << 'EOSQL'

-- 创建 MCP 专用只读用户
CREATE USER mcp_readonly WITH PASSWORD 'mcp_secure_pass_2025';

-- 授予连接权限到 ai_sales 数据库
GRANT CONNECT ON DATABASE ai_sales TO mcp_readonly;

-- 切换到 ai_sales 数据库
\c ai_sales

-- 授予只读权限
GRANT USAGE ON SCHEMA public TO mcp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO mcp_readonly;

-- 对 km_ai_admin 数据库重复相同操作
\c km_ai_admin
GRANT USAGE ON SCHEMA public TO mcp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO mcp_readonly;

EOSQL

echo "✅ PostgreSQL 只读用户 mcp_readonly 创建完成"
```

#### MySQL 只读用户 (推荐)

```bash
# 创建 MySQL 只读用户
mysql -u root -p << 'EOSQL'

-- 创建 MCP 专用只读用户
CREATE USER 'mcp_readonly'@'localhost' IDENTIFIED BY 'mcp_secure_pass_2025';

-- 查看所有数据库
SHOW DATABASES;

-- 根据需要授予权限 (示例: 假设有 myapp 数据库)
-- GRANT SELECT ON myapp.* TO 'mcp_readonly'@'localhost';

-- 授予所有数据库的只读权限 (慎用)
-- GRANT SELECT ON *.* TO 'mcp_readonly'@'localhost';

FLUSH PRIVILEGES;

EOSQL

echo "✅ MySQL 只读用户 mcp_readonly 创建完成"
```

---

### 步骤2: 配置环境变量

编辑 `config/.env` 文件:

```bash
nano config/.env
```

添加或修改以下配置:

```bash
# ============================================================
# 🗄️ 数据库连接配置
# ============================================================

# PostgreSQL - ai_sales 数据库
POSTGRES_URL=postgresql://mcp_readonly:mcp_secure_pass_2025@localhost:5432/ai_sales

# PostgreSQL - km_ai_admin 数据库 (备用)
POSTGRES_URL_KM=postgresql://mcp_readonly:mcp_secure_pass_2025@localhost:5432/km_ai_admin

# MySQL 连接
MYSQL_HOST=localhost
MYSQL_USER=mcp_readonly
MYSQL_PASSWORD=mcp_secure_pass_2025
MYSQL_DATABASE=your_database_name  # 根据实际情况修改
MYSQL_PORT=3306
```

保存文件 (Ctrl+O, Enter, Ctrl+X)

---

### 步骤3: 启用 MCP 数据库服务器

编辑 `config/servers.yaml`:

```bash
nano config/servers.yaml
```

找到 PostgreSQL 和 MySQL 配置,修改为:

```yaml
  # PostgreSQL - ai_sales 数据库
  postgres:
    server_type: stdio
    command: /home/sun/TeyMCP-Server/.local/bin/npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
      - "postgresql://mcp_readonly:mcp_secure_pass_2025@localhost:5432/ai_sales"
    enabled: true  # 改为 true
    critical: false
    description: "PostgreSQL - ai_sales 数据库只读访问"
    
  # MySQL 数据库
  mysql:
    server_type: stdio
    command: /home/sun/TeyMCP-Server/.local/bin/npx
    args:
      - "-y"
      - "@mysql/mcp-server-mysql"
    env:
      MYSQL_HOST: localhost
      MYSQL_USER: mcp_readonly
      MYSQL_PASSWORD: mcp_secure_pass_2025
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_PORT: 3306
    enabled: true  # 改为 true
    critical: false
    description: "MySQL - 数据库集成"
```

或者使用命令快速启用:

```bash
# 启用 PostgreSQL
sed -i '/^  postgres:/,/enabled:/ s/enabled: false/enabled: true/' config/servers.yaml

# 启用 MySQL
sed -i '/^  mysql:/,/enabled:/ s/enabled: false/enabled: true/' config/servers.yaml
```

---

### 步骤4: 重启 TeyMCP-Server

```bash
cd /home/sun/TeyMCP-Server
bash scripts/restart.sh
```

---

### 步骤5: 验证数据库 MCP 连接

```bash
# 等待 10 秒让服务器完全启动
sleep 10

# 检查 PostgreSQL MCP 工具
curl -s http://localhost:8080/api/tools | jq '.[] | select(.server=="postgres")'

# 检查 MySQL MCP 工具
curl -s http://localhost:8080/api/tools | jq '.[] | select(.server=="mysql")'

# 查看所有数据库相关工具
curl -s http://localhost:8080/api/tools | jq '.[] | select(.server | contains("sql"))'
```

---

## 🎯 MCP 数据库工具能做什么?

### PostgreSQL MCP 工具

1. **list_tables** - 列出所有表
2. **describe_table** - 查看表结构
3. **query** - 执行 SELECT 查询 (只读)
4. **get_schema** - 获取完整数据库模式

### 使用示例

```bash
# 调用 PostgreSQL 工具查询数据
curl -X POST http://localhost:8080/api/call-tool \
  -H "Content-Type: application/json" \
  -d '{
    "server": "postgres",
    "tool": "query",
    "arguments": {
      "query": "SELECT * FROM your_table LIMIT 10;"
    }
  }'
```

---

## 🔒 安全最佳实践

### ✅ 推荐做法

1. **使用只读用户**: PostgreSQL MCP 默认只支持 SELECT 查询
2. **限制权限**: 只授予必要的数据库和表访问权限
3. **强密码**: 使用复杂的密码
4. **本地连接**: 数据库只监听 127.0.0.1,不暴露到公网
5. **日志审计**: 监控 MCP 数据库访问日志

### ⚠️ 避免做法

- ❌ 不要使用 root/postgres 超级用户
- ❌ 不要授予 INSERT/UPDATE/DELETE 权限 (除非必要)
- ❌ 不要将密码硬编码在 servers.yaml (使用环境变量)
- ❌ 不要将 .env 文件提交到 Git

---

## 🔧 故障排查

### 问题1: "Could not connect to database"

**检查清单**:
```bash
# 1. 测试数据库连接
psql "postgresql://mcp_readonly:mcp_secure_pass_2025@localhost:5432/ai_sales" -c "SELECT version();"

# 2. 检查用户权限
sudo -u postgres psql -c "\du mcp_readonly"

# 3. 检查服务器日志
tail -f /home/sun/TeyMCP-Server/data/logs/teymcp_*.log | grep -i postgres
```

### 问题2: "Permission denied"

**解决**:
```sql
-- PostgreSQL
\c ai_sales
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;

-- MySQL
GRANT SELECT ON your_database.* TO 'mcp_readonly'@'localhost';
FLUSH PRIVILEGES;
```

### 问题3: MCP 服务器未出现在工具列表

**检查**:
```bash
# 查看服务器状态
curl http://localhost:8080/api/servers | jq '.[] | select(.name | contains("postgres") or contains("mysql"))'

# 手动测试 MCP 服务器
npx -y @modelcontextprotocol/server-postgres "postgresql://mcp_readonly:mcp_secure_pass_2025@localhost:5432/ai_sales"
```

---

## 🎨 高级配置: 多数据库支持

如果需要同时连接多个数据库,可以在 `config/servers.yaml` 中添加多个配置:

```yaml
  # PostgreSQL - ai_sales 数据库
  postgres_ai_sales:
    server_type: stdio
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
      - "postgresql://mcp_readonly:pass@localhost:5432/ai_sales"
    enabled: true
    description: "AI销售数据库"
    
  # PostgreSQL - km_ai_admin 数据库
  postgres_km_admin:
    server_type: stdio
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
      - "postgresql://mcp_readonly:pass@localhost:5432/km_ai_admin"
    enabled: true
    description: "知识管理数据库"
```

---

## 📊 数据库查询示例

### AI 辅助查询示例

当 AI 连接到您的数据库后,可以执行以下操作:

1. **探索数据库结构**
   ```
   User: "ai_sales 数据库有哪些表?"
   AI: (调用 list_tables 工具) → 返回表列表
   ```

2. **查看表结构**
   ```
   User: "sales_records 表有哪些字段?"
   AI: (调用 describe_table) → 返回表结构
   ```

3. **数据分析**
   ```
   User: "查询最近7天的销售总额"
   AI: (执行 SELECT SUM(amount) FROM sales WHERE date > NOW() - INTERVAL '7 days')
   ```

4. **生成报告**
   ```
   User: "按产品类别统计销量"
   AI: (执行 GROUP BY 查询并生成报告)
   ```

---

## 🌟 实战案例: AI 销售数据库

假设 `ai_sales` 数据库结构:

```sql
-- 客户表
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    amount DECIMAL(10,2),
    order_date DATE,
    status VARCHAR(20)
);

-- 产品表
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);
```

### AI 可以回答的问题:

- "本月新增了多少客户?"
- "销售额排名前10的产品是什么?"
- "哪些订单还在待处理状态?"
- "按月份统计销售趋势"
- "客户平均订单金额是多少?"

---

## 📝 配置文件模板

### config/.env (数据库部分)
```bash
# PostgreSQL
POSTGRES_URL=postgresql://mcp_readonly:YOUR_PASSWORD@localhost:5432/ai_sales

# MySQL
MYSQL_HOST=localhost
MYSQL_USER=mcp_readonly
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DATABASE=your_database
MYSQL_PORT=3306
```

### pg_hba.conf (PostgreSQL 访问控制)
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all            mcp_readonly                            md5
host    all            mcp_readonly    127.0.0.1/32            md5
```

---

## 🚀 下一步

1. ✅ 创建只读数据库用户
2. ✅ 配置 config/.env
3. ✅ 启用数据库 MCP 服务器
4. ✅ 重启 TeyMCP-Server
5. ✅ 验证连接和工具可用性
6. 🎯 开始使用 AI 查询和分析数据!

---

**提示**: 数据库连接配置好后,您可以直接在 Claude Desktop、Cursor、或其他 MCP 客户端中通过自然语言与数据库交互,无需编写 SQL 代码!
