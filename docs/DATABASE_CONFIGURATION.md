# 🗄️ TeyMCP-Server 数据库连接配置指南

TeyMCP-Server 支持多种数据库的 MCP 服务器集成,允许 AI 直接查询和操作数据库。

---

## 📊 支持的数据库

### 1️⃣ PostgreSQL
**官方 MCP 服务器**: `@modelcontextprotocol/server-postgres`

**功能**:
- ✅ 只读数据库访问 (安全)
- ✅ 查询表结构和数据
- ✅ 执行 SELECT 查询
- ❌ 不支持写入操作 (安全限制)

**配置文件**: `config/servers.yaml`
```yaml
postgres:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-postgres"
    - "postgresql://localhost/mydb"
  enabled: false
  critical: false
  description: "PostgreSQL - 只读数据库访问"
```

**环境变量**: `config/.env`
```bash
# PostgreSQL 连接字符串
POSTGRES_URL=postgresql://username:password@localhost:5432/database_name
```

**使用示例**:
```bash
# 1. 修改 config/.env 设置你的数据库连接
POSTGRES_URL=postgresql://myuser:mypass@localhost:5432/mydb

# 2. 在 config/servers.yaml 中启用
postgres:
  enabled: true  # 改为 true

# 3. 重启服务
bash scripts/restart.sh
```

---

### 2️⃣ MySQL
**社区 MCP 服务器**: `@mysql/mcp-server-mysql`

**功能**:
- ✅ 完整的 MySQL 数据库访问
- ✅ 查询和修改数据
- ✅ 存储过程调用
- ⚠️ 支持写操作 (需谨慎使用)

**配置文件**: `config/servers.yaml`
```yaml
mysql:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@mysql/mcp-server-mysql"
  env:
    MYSQL_HOST: ${MYSQL_HOST}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    MYSQL_DATABASE: ${MYSQL_DATABASE}
  enabled: false
  critical: false
  description: "MySQL - 数据库集成"
```

**环境变量**: `config/.env`
```bash
# MySQL 连接信息
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

---

### 3️⃣ SQLite
**官方 MCP 服务器**: `@modelcontextprotocol/server-sqlite`

**功能**:
- ✅ 轻量级本地数据库
- ✅ 无需服务器配置
- ✅ 完整的读写访问
- ✅ 适合小型项目和测试

**配置文件**: `config/servers.yaml`
```yaml
sqlite:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@modelcontextprotocol/server-sqlite"
    - "/path/to/database.db"
  enabled: false
  critical: false
  description: "SQLite - 轻量级数据库"
```

**使用示例**:
```bash
# 修改路径指向你的 SQLite 数据库文件
sqlite:
  args:
    - "-y"
    - "@modelcontextprotocol/server-sqlite"
    - "/home/sun/mydata.db"  # 你的数据库路径
  enabled: true
```

---

### 4️⃣ MongoDB
**社区 MCP 服务器**: `@mongodb/mcp-server-mongodb`

**功能**:
- ✅ NoSQL 文档数据库
- ✅ 集合查询和聚合
- ✅ 文档增删改查
- ✅ MongoDB Atlas 云支持

**配置文件**: `config/servers.yaml`
```yaml
mongodb:
  server_type: stdio
  command: npx
  args:
    - "-y"
    - "@mongodb/mcp-server-mongodb"
  env:
    MONGODB_URI: ${MONGODB_URI}
  enabled: false
  critical: false
  description: "MongoDB - NoSQL数据库"
```

**环境变量**: `config/.env`
```bash
# MongoDB 连接字符串
MONGODB_URI=mongodb://username:password@localhost:27017/database_name

# 或 MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
```

---

## 🔒 安全建议

### ⚠️ 重要安全提示

1. **只读优先**: 
   - PostgreSQL MCP 默认只读,推荐用于生产环境
   - 避免给 AI 完整的数据库写入权限

2. **独立数据库用户**:
   ```sql
   -- PostgreSQL 示例
   CREATE USER mcp_readonly WITH PASSWORD 'secure_password';
   GRANT CONNECT ON DATABASE mydb TO mcp_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
   ```

3. **连接字符串保护**:
   ```bash
   # config/.env 文件权限
   chmod 600 config/.env
   
   # 不要提交到 Git
   echo "config/.env" >> .gitignore
   ```

4. **限制网络访问**:
   - 数据库防火墙只允许本地连接
   - 使用 SSH 隧道访问远程数据库

---

## 🚀 快速启动示例

### 场景1: 只读 PostgreSQL 查询

```bash
# 1. 配置环境变量
cat >> config/.env << 'DBEOF'
POSTGRES_URL=postgresql://readonly_user:pass@localhost:5432/analytics_db
DBEOF

# 2. 启用服务器
sed -i '/postgres:/,/enabled:/s/enabled: false/enabled: true/' config/servers.yaml

# 3. 重启
bash scripts/restart.sh

# 4. 测试
curl http://localhost:8080/api/tools | jq '.[] | select(.server=="postgres")'
```

### 场景2: SQLite 本地数据库

```bash
# 1. 创建测试数据库
sqlite3 /tmp/test.db "CREATE TABLE users (id INT, name TEXT); INSERT INTO users VALUES (1, 'Alice');"

# 2. 修改配置
sed -i 's|/path/to/database.db|/tmp/test.db|g' config/servers.yaml
sed -i '/sqlite:/,/enabled:/s/enabled: false/enabled: true/' config/servers.yaml

# 3. 重启并测试
bash scripts/restart.sh
curl http://localhost:8080/api/tools | jq '.[] | select(.server=="sqlite")'
```

### 场景3: MySQL 开发环境

```bash
# 1. 配置 MySQL 连接
cat >> config/.env << 'DBEOF'
MYSQL_HOST=localhost
MYSQL_USER=dev_user
MYSQL_PASSWORD=dev_password
MYSQL_DATABASE=dev_database
DBEOF

# 2. 启用服务器
sed -i '/mysql:/,/enabled:/s/enabled: false/enabled: true/' config/servers.yaml

# 3. 重启
bash scripts/restart.sh
```

---

## 🔧 故障排查

### 问题1: 连接失败

**症状**: `Could not connect to database`

**检查步骤**:
```bash
# 1. 验证数据库可访问
psql "postgresql://user:pass@localhost/db"  # PostgreSQL
mysql -h localhost -u user -ppass db        # MySQL

# 2. 检查环境变量加载
source config/.env
echo $POSTGRES_URL

# 3. 查看服务器日志
tail -f data/logs/teymcp_*.log | grep -i database
```

### 问题2: 权限不足

**症状**: `Permission denied on table`

**解决**:
```sql
-- PostgreSQL 授予权限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO your_user;

-- MySQL 授予权限
GRANT SELECT ON your_database.* TO 'your_user'@'localhost';
```

### 问题3: MCP 服务器未启动

**检查**:
```bash
# 查看服务器状态
curl http://localhost:8080/api/servers | jq '.[] | select(.name | contains("postgres"))'

# 手动测试 MCP 服务器
npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/mydb"
```

---

## 📚 更多资源

- [PostgreSQL MCP 文档](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
- [MySQL MCP 文档](https://github.com/mysql/mcp-server-mysql)
- [SQLite MCP 文档](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)
- [MongoDB MCP 文档](https://github.com/mongodb/mcp-server-mongodb)

---

## 🤝 常见用例

### 用例1: 数据分析查询
AI 可以查询数据库生成报告:
```
User: "分析最近30天的用户注册趋势"
AI: (执行 SELECT COUNT(*), DATE(created_at) FROM users WHERE created_at > NOW() - INTERVAL 30 DAY GROUP BY DATE(created_at))
```

### 用例2: 数据库模式探索
AI 可以理解你的数据结构:
```
User: "我的数据库有哪些表?"
AI: (执行 \dt 或 SHOW TABLES)
```

### 用例3: 业务洞察
AI 结合多表查询分析业务:
```
User: "哪些产品销量最好?"
AI: (JOIN orders, products, 聚合统计)
```

---

**提示**: 所有数据库 MCP 服务器默认都是 `enabled: false`,需要手动启用并配置连接信息后才能使用。
