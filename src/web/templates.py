"""
HTML模板
内嵌在Python中的Web界面
"""

def get_dashboard_html() -> str:
    """获取管理面板HTML"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeyMCP-Server 管理面板</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .log-entry {
            transition: all 0.3s ease;
        }
        .log-entry:hover {
            transform: translateX(5px);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="text-3xl">🚀</div>
                    <div>
                        <h1 class="text-2xl font-bold text-gray-800">TeyMCP-Server</h1>
                        <p class="text-xs text-gray-500">The One MCP to Rule Them All</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-500" id="current-time"></span>
                    <span class="status-dot bg-green-500"></span>
                    <span class="text-sm font-medium text-green-600">在线</span>
                </div>
            </div>
        </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 py-8">
        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500 mb-1">服务器总数</p>
                        <p class="text-3xl font-bold text-gray-800" id="server-count">0</p>
                    </div>
                    <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-server text-blue-600 text-xl"></i>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500 mb-1">可用工具</p>
                        <p class="text-3xl font-bold text-gray-800" id="tool-count">0</p>
                    </div>
                    <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-tools text-green-600 text-xl"></i>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500 mb-1">总调用</p>
                        <p class="text-3xl font-bold text-gray-800" id="total-calls">0</p>
                    </div>
                    <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-chart-line text-purple-600 text-xl"></i>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500 mb-1">成功率</p>
                        <p class="text-3xl font-bold text-gray-800" id="success-rate">100%</p>
                    </div>
                    <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-check-circle text-orange-600 text-xl"></i>
                    </div>
                </div>
            </div>
        </div>

        <!-- 服务器列表 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 mb-8">
            <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
                <h2 class="text-lg font-semibold text-gray-800">
                    <i class="fas fa-list-check mr-2"></i>服务器状态
                </h2>
                <button onclick="refreshData()" class="text-sm text-blue-600 hover:text-blue-800">
                    <i class="fas fa-sync-alt mr-1"></i>刷新
                </button>
            </div>
            <div class="p-6">
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="text-left text-sm text-gray-500 border-b">
                                <th class="pb-3 font-medium">名称</th>
                                <th class="pb-3 font-medium">状态</th>
                                <th class="pb-3 font-medium">工具数</th>
                                <th class="pb-3 font-medium">最后检查</th>
                                <th class="pb-3 font-medium">错误数</th>
                            </tr>
                        </thead>
                        <tbody id="server-table" class="text-sm">
                            <tr>
                                <td colspan="5" class="text-center py-8 text-gray-400">
                                    加载中...
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 实时日志 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100">
            <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
                <h2 class="text-lg font-semibold text-gray-800">
                    <i class="fas fa-terminal mr-2"></i>实时日志
                </h2>
                <button onclick="clearLogs()" class="text-sm text-gray-500 hover:text-gray-700">
                    <i class="fas fa-trash mr-1"></i>清空
                </button>
            </div>
            <div class="p-6">
                <div id="logs-container" class="space-y-2 max-h-96 overflow-y-auto font-mono text-sm">
                    <div class="text-gray-400 text-center py-8">
                        等待日志...
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 更新时间
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = 
                now.toLocaleString('zh-CN');
        }
        setInterval(updateTime, 1000);
        updateTime();

        // 获取状态
        async function fetchStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('获取状态失败:', error);
            }
        }

        // 更新仪表盘
        function updateDashboard(data) {
            document.getElementById('server-count').textContent = data.servers.length;
            document.getElementById('tool-count').textContent = data.tools_count || 0;
            document.getElementById('total-calls').textContent = data.metrics.total_calls;
            
            const successRate = data.metrics.total_calls > 0 
                ? ((data.metrics.successful_calls / data.metrics.total_calls) * 100).toFixed(1)
                : 100;
            document.getElementById('success-rate').textContent = successRate + '%';

            // 更新服务器表格
            const tbody = document.getElementById('server-table');
            if (data.servers.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center py-8 text-gray-400">
                            暂无服务器
                        </td>
                    </tr>
                `;
            } else {
                tbody.innerHTML = data.servers.map(server => `
                    <tr class="border-b border-gray-50 hover:bg-gray-50 transition">
                        <td class="py-4">
                            <span class="font-medium text-gray-800">${server.name}</span>
                        </td>
                        <td class="py-4">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                server.status === 'healthy' 
                                    ? 'bg-green-100 text-green-800' 
                                    : 'bg-red-100 text-red-800'
                            }">
                                <span class="status-dot ${
                                    server.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'
                                } mr-1"></span>
                                ${server.status === 'healthy' ? '健康' : '异常'}
                            </span>
                        </td>
                        <td class="py-4 text-gray-600">${server.tools_count || 0}</td>
                        <td class="py-4 text-gray-600">${formatTime(server.last_check)}</td>
                        <td class="py-4">
                            <span class="${server.error_count > 0 ? 'text-red-600' : 'text-gray-600'}">
                                ${server.error_count || 0}
                            </span>
                        </td>
                    </tr>
                `).join('');
            }
        }

        // 格式化时间
        function formatTime(isoString) {
            if (!isoString) return '-';
            const date = new Date(isoString);
            return date.toLocaleTimeString('zh-CN');
        }

        // 获取日志
        async function fetchLogs() {
            try {
                const response = await fetch('/api/logs?limit=50');
                const data = await response.json();
                updateLogs(data.logs);
            } catch (error) {
                console.error('获取日志失败:', error);
            }
        }

        // 更新日志
        function updateLogs(logs) {
            const container = document.getElementById('logs-container');
            
            if (logs.length === 0) {
                container.innerHTML = '<div class="text-gray-400 text-center py-8">暂无日志</div>';
                return;
            }
            
            container.innerHTML = logs.reverse().map(log => `
                <div class="log-entry p-3 rounded-lg border ${
                    log.status === 'success' 
                        ? 'bg-green-50 border-green-200' 
                        : 'bg-red-50 border-red-200'
                }">
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <span class="font-semibold">${log.tool_name}</span>
                            <span class="text-gray-500 ml-2">${log.server}</span>
                        </div>
                        <span class="text-gray-500">${log.duration_ms}ms</span>
                    </div>
                    <div class="text-xs text-gray-600 mt-1">
                        ${new Date(log.timestamp).toLocaleString('zh-CN')}
                    </div>
                    ${log.error ? `<div class="text-xs text-red-600 mt-1">${log.error}</div>` : ''}
                </div>
            `).join('');
        }

        // 清空日志
        async function clearLogs() {
            if (!confirm('确定要清空所有日志吗？')) return;
            
            try {
                await fetch('/api/logs', { method: 'DELETE' });
                document.getElementById('logs-container').innerHTML = 
                    '<div class="text-gray-400 text-center py-8">日志已清空</div>';
            } catch (error) {
                console.error('清空日志失败:', error);
            }
        }

        // 刷新数据
        function refreshData() {
            fetchStatus();
            fetchLogs();
        }

        // 定时刷新
        setInterval(refreshData, 5000);
        
        // 初始加载
        refreshData();
    </script>
</body>
</html>
    """
