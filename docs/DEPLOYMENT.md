# 🚀 部署指南

TeyMCP-Server 生产环境部署完整指南。

---

## 📋 目录

- [系统要求](#系统要求)
- [部署方式对比](#部署方式对比)
- [单机部署](#单机部署)
- [Docker部署](#docker部署)
- [Kubernetes部署](#kubernetes部署)
- [反向代理配置](#反向代理配置)
- [SSL证书配置](#ssl证书配置)
- [性能优化](#性能优化)
- [备份策略](#备份策略)

---

## 💻 系统要求

### 最低配置
- **CPU**: 1核
- **内存**: 512MB
- **磁盘**: 10GB
- **系统**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

### 推荐配置
- **CPU**: 2核+
- **内存**: 2GB+
- **磁盘**: 20GB+
- **系统**: Ubuntu 22.04 LTS

### 软件依赖
- Python 3.10+
- Node.js 18+ (用于上游MCP)
- Git 2.30+
- systemd (可选，用于服务管理)

---

## 🔄 部署方式对比

| 方式 | 难度 | 资源占用 | 隔离性 | 扩展性 | 推荐场景 |
|------|------|----------|--------|--------|----------|
| 单机部署 | ⭐ | 低 | 低 | 低 | 开发测试 |
| Docker | ⭐⭐ | 中 | 高 | 中 | 小型生产 |
| K8s | ⭐⭐⭐⭐ | 高 | 高 | 高 | 大规模生产 |
| Systemd | ⭐⭐ | 低 | 低 | 低 | 简单生产 |

---

## 🖥️ 单机部署

### 1. 准备环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install -y python3.10 python3.10-venv python3-pip \
                    nodejs npm git curl

# 验证安装
python3.10 --version
node --version
npm --version
```

### 2. 创建部署用户

```bash
# 创建专用用户
sudo useradd -r -m -s /bin/bash teymcp

# 切换用户
sudo su - teymcp
```

### 3. 安装应用

```bash
# 克隆仓库
git clone https://github.com/zf13883922290/TeyMCP-Server.git
cd TeyMCP-Server

# 运行安装脚本
bash scripts/install.sh

# 配置环境变量
cp config/.env.example config/.env
nano config/.env
```

### 4. 配置Systemd服务

```bash
# 退出teymcp用户
exit

# 创建systemd服务文件
sudo tee /etc/systemd/system/teymcp.service > /dev/null << 'EOF'
[Unit]
Description=TeyMCP-Server
After=network.target

[Service]
Type=simple
User=teymcp
Group=teymcp
WorkingDirectory=/home/teymcp/TeyMCP-Server
Environment="PATH=/home/teymcp/TeyMCP-Server/venv/bin"
ExecStart=/home/teymcp/TeyMCP-Server/venv/bin/python src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start teymcp

# 设置开机自启
sudo systemctl enable teymcp

# 查看状态
sudo systemctl status teymcp
```

### 5. 验证部署

```bash
# 检查服务状态
curl http://localhost:8080/health

# 查看日志
sudo journalctl -u teymcp -f
```

---

## 🐳 Docker部署

### 1. 使用项目自带的Docker配置

项目已包含完整的Docker配置文件：

```bash
cd TeyMCP-Server

# 查看Docker文件
ls -la docker/
# Dockerfile
# docker-compose.yml
# .dockerignore
```

### 2. 配置环境变量

```bash
# 复制环境变量示例
cp config/.env.example config/.env

# 编辑环境变量
nano config/.env
```

### 3. 使用Docker Compose部署

```bash
# 进入docker目录
cd docker

# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看状态
docker-compose ps

# 停止服务
docker-compose down
```

### 4. 单独使用Docker运行

```bash
# 构建镜像
docker build -t teymcp-server -f docker/Dockerfile .

# 运行容器
docker run -d \
  --name teymcp-server \
  -p 8080:8080 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  --env-file config/.env \
  teymcp-server

# 查看日志
docker logs -f teymcp-server

# 进入容器
docker exec -it teymcp-server /bin/bash
```

### 5. Docker镜像优化

```bash
# 多阶段构建（减小镜像大小）
# 已在 docker/Dockerfile 中实现

# 查看镜像大小
docker images | grep teymcp

# 清理未使用的镜像
docker system prune -a
```

---

## ☸️ Kubernetes部署

### 1. 创建命名空间

```bash
kubectl create namespace teymcp
```

### 2. 创建Secret

```bash
# 从.env文件创建Secret
kubectl create secret generic teymcp-secret \
  --from-env-file=config/.env \
  -n teymcp
```

### 3. 应用ConfigMap

```bash
# 项目已包含k8s配置文件
cd k8s

# 应用ConfigMap
kubectl apply -f configmap.yaml
```

### 4. 部署应用

```bash
# 应用Deployment
kubectl apply -f deployment.yaml

# 应用Service
kubectl apply -f service.yaml

# 查看部署状态
kubectl get pods -n teymcp
kubectl get svc -n teymcp
```

### 5. 创建Ingress（可选）

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: teymcp-ingress
  namespace: teymcp
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - teymcp.yourdomain.com
    secretName: teymcp-tls
  rules:
  - host: teymcp.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: teymcp-service
            port:
              number: 80
```

```bash
kubectl apply -f k8s/ingress.yaml
```

### 6. 验证部署

```bash
# 查看Pod状态
kubectl get pods -n teymcp

# 查看服务
kubectl get svc -n teymcp

# 查看日志
kubectl logs -f deployment/teymcp-server -n teymcp

# 进入Pod
kubectl exec -it <pod-name> -n teymcp -- /bin/bash
```

### 7. 扩容

```bash
# 手动扩容
kubectl scale deployment teymcp-server --replicas=5 -n teymcp

# 或配置HPA（水平自动扩缩容）
kubectl autoscale deployment teymcp-server \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n teymcp
```

---

## 🌐 反向代理配置

### Nginx配置

```nginx
# /etc/nginx/sites-available/teymcp
server {
    listen 80;
    server_name teymcp.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name teymcp.yourdomain.com;

    # SSL证书
    ssl_certificate /etc/letsencrypt/live/teymcp.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/teymcp.yourdomain.com/privkey.pem;

    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 日志
    access_log /var/log/nginx/teymcp.access.log;
    error_log /var/log/nginx/teymcp.error.log;

    # 代理配置
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket支持
    location /ws {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # 静态文件缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        proxy_pass http://localhost:8080;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/teymcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Apache配置

```apache
# /etc/apache2/sites-available/teymcp.conf
<VirtualHost *:80>
    ServerName teymcp.yourdomain.com
    Redirect permanent / https://teymcp.yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName teymcp.yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/teymcp.yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/teymcp.yourdomain.com/privkey.pem

    ProxyPreserveHost On
    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/

    # WebSocket支持
    RewriteEngine on
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://localhost:8080/$1" [P,L]

    ErrorLog ${APACHE_LOG_DIR}/teymcp.error.log
    CustomLog ${APACHE_LOG_DIR}/teymcp.access.log combined
</VirtualHost>
```

启用配置：
```bash
sudo a2enmod proxy proxy_http proxy_wstunnel rewrite ssl
sudo a2ensite teymcp
sudo systemctl reload apache2
```

---

## 🔒 SSL证书配置

### 使用Let's Encrypt

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书（Nginx）
sudo certbot --nginx -d teymcp.yourdomain.com

# 或手动获取（Apache）
sudo certbot --apache -d teymcp.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

### 配置自动续期

```bash
# 添加cron任务
sudo crontab -e

# 每天凌晨2点检查续期
0 2 * * * certbot renew --quiet && systemctl reload nginx
```

---

## ⚡ 性能优化

### 1. Worker配置

```yaml
# config/app.yaml
server:
  workers: 4    # 设置为CPU核心数
```

### 2. 启用缓存

```yaml
cache:
  enabled: true
  ttl: 300
  max_size: 1000
```

### 3. 数据库优化

```bash
# 使用PostgreSQL替代SQLite
# config/.env
DATABASE_URL=postgresql://user:password@localhost/teymcp
```

### 4. 使用Redis缓存

```yaml
cache:
  backend: redis
  redis_url: redis://localhost:6379/0
```

### 5. 启用gzip压缩（Nginx）

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript;
```

---

## 💾 备份策略

### 1. 数据备份脚本

```bash
#!/bin/bash
# /home/teymcp/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/teymcp/backups"
PROJECT_DIR="/home/teymcp/TeyMCP-Server"

mkdir -p $BACKUP_DIR

# 备份配置
tar -czf $BACKUP_DIR/config_$DATE.tar.gz -C $PROJECT_DIR config/

# 备份数据
tar -czf $BACKUP_DIR/data_$DATE.tar.gz -C $PROJECT_DIR data/

# 备份数据库
if [ -f "$PROJECT_DIR/data/teymcp.db" ]; then
    cp $PROJECT_DIR/data/teymcp.db $BACKUP_DIR/teymcp_$DATE.db
fi

# 删除30天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "✅ 备份完成: $BACKUP_DIR"
```

### 2. 配置自动备份

```bash
# 添加执行权限
chmod +x /home/teymcp/backup.sh

# 配置cron任务
crontab -e

# 每天凌晨3点备份
0 3 * * * /home/teymcp/backup.sh >> /home/teymcp/backup.log 2>&1
```

### 3. 远程备份

```bash
# 同步到远程服务器
rsync -avz /home/teymcp/backups/ \
  user@backup-server:/path/to/backups/teymcp/

# 或使用rclone同步到云存储
rclone sync /home/teymcp/backups/ remote:teymcp-backups
```

---

## 📊 监控配置

### 1. Prometheus监控

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'teymcp'
    static_configs:
      - targets: ['localhost:9090']
```

### 2. Grafana仪表盘

导入预制仪表盘：
```bash
# 下载仪表盘JSON
curl -o teymcp-dashboard.json \
  https://github.com/zf13883922290/TeyMCP-Server/blob/main/grafana/dashboard.json

# 在Grafana中导入
```

### 3. 日志聚合

```bash
# 使用ELK Stack或Loki
# docker-compose.yml
version: '3.8'
services:
  loki:
    image: grafana/loki
    ports:
      - "3100:3100"
  
  promtail:
    image: grafana/promtail
    volumes:
      - /home/teymcp/TeyMCP-Server/data/logs:/logs
```

---

## 🔍 健康检查

### 1. 健康检查脚本

```bash
#!/bin/bash
# /home/teymcp/healthcheck.sh

HEALTH_URL="http://localhost:8080/health"
ALERT_EMAIL="admin@yourdomain.com"

response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $response -ne 200 ]; then
    echo "⚠️ TeyMCP-Server不健康！" | mail -s "服务告警" $ALERT_EMAIL
    exit 1
fi

echo "✅ 服务健康"
exit 0
```

### 2. 配置监控

```bash
# cron任务 - 每5分钟检查
*/5 * * * * /home/teymcp/healthcheck.sh
```

---

## 🚨 故障恢复

### 1. 服务崩溃

```bash
# systemd会自动重启（已配置Restart=always）
sudo systemctl status teymcp

# 查看崩溃日志
sudo journalctl -u teymcp -n 100
```

### 2. 数据恢复

```bash
# 停止服务
sudo systemctl stop teymcp

# 恢复数据
tar -xzf backups/data_20250104.tar.gz -C /home/teymcp/TeyMCP-Server/

# 启动服务
sudo systemctl start teymcp
```

---

## 📚 相关文档

- [配置说明](CONFIGURATION.md) - 详细配置选项
- [API文档](API.md) - API接口说明
- [故障排查](TROUBLESHOOTING.md) - 问题诊断
- [快速入门](QUICKSTART.md) - 快速上手

---

**部署成功，稳定运行！** 🚀
