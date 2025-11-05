QTR MCP Server
TypeScript 实现的 MCP 工具集：辅助从 TS → Java 的依赖与 API 映射，支持从私有 Nexus 拉取 JAR、本地解析类与方法签名，并借助 LLM 进行“最匹配”判断。

环境要求
Node.js ≥ 18 LTS（已启用 corepack）
已安装 JDK（需 jar、javap）
包管理：pnpm（建议通过 corepack 管理）
快速启用兼容 pnpm 版本：

corepack enable
corepack prepare pnpm@8.15.4 --activate
pnpm -v
安装
pnpm i
配置（环境变量）
Nexus 访问
QTR_NEXUS_HOST（必填）：例如 https://nexus.example.com
QTR_NEXUS_REPOSITORY（必填）：仓库名，例如 maven-releases
QTR_NEXUS_USERNAME / QTR_NEXUS_PASSWORD
运行参数
QTR_TIMEOUT_MS（默认 20000）
QTR_RETRY（默认 1）
QTR_CONCURRENCY（默认 4）
缓存
QTR_CACHE_DIR_SHARED（默认 ~/.cache/qtr_mcp，支持 ~ 展开）
QTR_USE_SHARED_CACHE（默认 true）：开启后会同时使用共享目录 ~/.cache/qtr_mcp
LLM
QTR_LLM_PROVIDER：openai-compatible | deepseek（默认 openai-compatible）
QTR_LLM_BASE_URL（可选）：OpenAI-compatible/DeepSeek 的 Base URL
QTR_LLM_API_KEY（可选）：API Key
QTR_LLM_MODEL（可选）：模型名，例如 deepseek-chat、gpt-4o、o1-mini
QTR_LLM_TEMPERATURE（默认 0.2）
QTR_LLM_TOP_P（默认 1.0）
QTR_LLM_MAX_TOKENS（默认 4096）
示例（DeepSeek 私有/官方）：

export QTR_LLM_PROVIDER=deepseek
export QTR_LLM_BASE_URL=https://api.deepseek.com
export QTR_LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
export QTR_LLM_MODEL=deepseek-chat
查看生效配置（敏感信息打码）：运行时会打印 JSON 摘要。

使用
1) 配置mcp
{
  "mcpServers": {
    "qtr-mcp-server": {
      "command": "npx",
      "args": ["-y", "qtr-mcp-server"],
      "env": {
        "QTR_CONCURRENCY": "2",
        "QTR_TIMEOUT_MS": "20000",
        "QTR_RETRY": "1",
        "QTR_NEXUS_HOST": "https://nexus.example.com",
        "QTR_NEXUS_REPOSITORY": "maven-releases",
        "QTR_NEXUS_USERNAME": "admin",
        "QTR_NEXUS_PASSWORD": "admin123",
        "QTR_LLM_BASE_URL": "https://api.openai.com",
        "QTR_LLM_API_KEY": "sk-xxxxxxxxxxxxxxxx",
        "QTR_LLM_MODEL": "gpt-4o",
        "QTR_LLM_TEMPERATURE": "0.2",
        "QTR_LLM_TOP_P": "1.0",
        "QTR_LLM_MAX_TOKENS": "4096",
        "QTR_CACHE_DIR_SHARED": "~/.cache/qtr_mcp",
        "QTR_USE_SHARED_CACHE": "true",
        "QTR_LOG_LEVEL": "info"
      }
    }
  }
}
输出：

Dev 模式会打印构建的下载 URL
保存路径（本地）：./.cache/qtr_mcp/<groupId 斜杠路径>/<artifact>/<version>/<artifact>-<version>.jar
若启用共享缓存：~/.cache/qtr_mcp/... 会被同时使用
2) 运行 MCP Server（stdio 传输）
pnpm dev
# 或使用构建产物/全局安装后的可执行
npx qtr-mcp-server
默认 stdio 传输，可让兼容 MCP 的客户端进行连接与调用
已注册工具（接口见 specs/001-mcp-tooling-ts/contracts/tool-schemas.json）：
match_package_and_class：匹配 npm 类名到 Maven 类
match_methods：匹配 npm 方法到 Maven 方法
list_classes：列出 JAR 包中所有类
list_class_meta：获取指定类的元数据（方法、字段）
get_methods_code：获取方法源码或字节码
clear_cache：清除缓存
调试
日志与进度：已接入 ora + colorette，在 dev 模式输出；NODE_ENV=production 会抑制部分调试输出
构建的 Nexus 下载 URL 会在 dev 模式下通过 log.debug 打印（函数：buildJarUrl）
常用脚本：
pnpm dev：本地启动（MCP）
pnpm build：构建到 dist/
pnpm start：运行构建产物
pnpm fetch:jar：下载示例 JAR
pnpm metrics：打印指标快照（含 RAW_JSON）
pnpm test：运行测试
发布（npm / 私有 Nexus）
方式A（推荐，从根发布）：

打包并检查
pnpm install
pnpm run build
npm pack  # 可选：生成 tar 包用于检查
发布到 npmjs
npm login
pnpm publish --access public
发布到私有 Nexus（npm 仓库）
在根目录配置 .npmrc：
registry=https://<nexus-host>/repository/<npm-repo>/
always-auth=true
//<nexus-host>/repository/<npm-repo>/:_authToken=${NPM_TOKEN}
或在 package.json 增加：
{
  "publishConfig": { "registry": "https://<nexus-host>/repository/<npm-repo>/" }
}
执行发布：
pnpm publish
说明：本项目已配置 files 与 prepublishOnly，发布时仅包含 dist/、README.md、LICENSE，并会在发布前自动构建。

审计（依赖与许可证）
依赖使用情况检查：
pnpm depcheck
许可证摘要：
pnpm license:summary
测试
已提供契约测试与集成测试：

# 运行所有测试
pnpm test

# 运行单个测试文件
pnpm test -- --run tests/integration/get_methods_code.int.test.ts

# 运行多个测试文件（使用正则表达式）
pnpm test -- --run "tests/integration/get_methods_code.int.test.ts|tests/integration/match_methods.int.test.ts"

# 运行特定目录下的所有测试
pnpm test -- --run tests/integration/

# 运行特定测试名称（使用正则表达式）
pnpm test -- --testNamePattern "returns code or bytecode text"

# 运行特定文件中的特定测试
pnpm test -- --run tests/integration/get_methods_code.int.test.ts --testNamePattern "returns code"

# 查看测试覆盖率
pnpm test -- --coverage
契约测试：tests/contract/tools.contract.test.ts（基于 JSON Schema 校验 tools 的入参/出参）
集成测试：
tests/integration/match_package_and_class.int.test.ts
tests/integration/match_methods.int.test.ts
tests/integration/get_methods_code.int.test.ts
tests/integration/list_classes.int.test.ts
tests/integration/list_class_meta.int.test.ts
tests/integration/clear_cache.int.test.ts
tests/integration/errors.int.test.ts
tests/integration/mcp_end_to_end.int.test.ts（可选跳过）
缓存机制
项目采用统一缓存管理器（CacheManager）管理所有缓存，包括：

Keyv 缓存：工具结果缓存（通过 keyv-file）
文件系统缓存：JAR 解析结果缓存
缓存目录结构
~/.cache/qtr_mcp/                      # 共享缓存根目录（可通过 QTR_CACHE_DIR_SHARED 配置）
├── results/
│   └── request-cache.json             # Keyv 缓存（工具结果）
├── logs/                              # 日志文件
└── jars/
    └── com/qunhe/diybe/module/math2/2.22.1/
        ├── math2-2.22.1.jar           # 下载的 JAR 包
        ├── math2-2.22.1-sources.jar   # 源码 JAR（如果可用）
        ├── entries.json               # JAR 条目列表（listJarEntries）
        ├── classes.json               # 类列表（listJarClasses）
        ├── jar-minimal.json           # 简化 JAR 元数据（parseJarMinimal）
        ├── signatures/                # 类签名缓存（parseClassSignatures，按类）
        │   └── com_qunhe_..._Vector3d.json
        ├── meta/                      # 类元数据缓存（parseClassMeta，按类）
        │   └── com_qunhe_..._Vector3d.json
        ├── methods/                   # 方法列表缓存（workflow，按类）
        │   └── com_qunhe_..._Vector3d.json
        └── methodCode/                # 方法代码缓存（getMethodsCode，按方法）
            ├── com_qunhe_..._Vector3d_cross__.json
            └── com_qunhe_..._Vector3d_add_Vector3d_.json
缓存管理器功能
CacheManager 提供以下功能：

工具缓存 Key 生成

toolKey(tool: string, input: object): string
// 生成包含版本号的唯一 key，用于 Keyv 缓存
Keyv 缓存操作

getFromKeyv<T>(key: string): Promise<T | undefined>
setToKeyv<T>(key: string, value: T): Promise<void>
文件系统缓存操作

readFromFileCache<T>(jarPath, type, fqcn?): T | null
writeToFileCache<T>(jarPath, type, data, fqcn?): void
hasFileCache(jarPath, type, fqcn?): boolean
缓存清理

clearJarCache(jarPath): { deletedFiles: number }
clearSharedCache(): { deletedFiles, deletedDirs }
clearAllCache(): { sharedFiles, deletedFiles, deletedDirs }
缓存统计

getCacheStats(jarPath?): { shared, jar? }
缓存配置
QTR_CACHE_DIR_SHARED：共享缓存目录（默认 ~/.cache/qtr_mcp）
QTR_USE_SHARED_CACHE：是否启用共享缓存（默认 true）
缓存 TTL：30 天（Keyv 缓存自动过期）
缓存版本：wf-v0.1.8（破坏性变更时更新以避免旧缓存冲突）
工具使用示例
详细示例请参考 specs/001-mcp-tooling-ts/quickstart.md，包括：

match_package_and_class：匹配 npm 类到 Maven 类
match_methods：匹配方法签名
list_classes：列出 JAR 包中的所有类
list_class_meta：获取类的方法和字段元数据
get_methods_code：获取方法源码或字节码（优先源码，失败时使用 javap）
clear_cache：清除全部或共享缓存
项目结构
src/lib/：配置（Zod）、日志
src/services/：
cacheManager.ts：统一缓存管理器（Keyv + 文件系统）
cache.ts：Keyv 缓存基础设施（已被 cacheManager.ts 整合）
nexus.ts：Nexus 下载
jarParser.ts：JAR 解析（jar/javap）
matcher.ts：类与方法匹配算法
workflow.ts：工具工作流编排
llm.ts：LLM 调用桩
metrics.ts：指标收集
src/mcp/：MCP 服务器与 tools 注册
src/cli/：命令行入口（start.ts、fetchJar.ts）
src/utils/：工具函数（ID 生成、字节码提取、源码提取等）
src/constant/：Zod schema 定义
specs/001-mcp-tooling-ts/：规范、计划、契约、样例
tests/：单元测试、集成测试、契约测试
备注
Node 18 兼容性：已固定 pnpm@8.15.4、vitest@0.34.x、vite@4.x、undici@5.x
后续工作：对接 LLM（LangChain.js）、完善类/方法解析与匹配逻辑、实现工具缓存与指标导出
Readme
Keywords
none
Package Sidebar
Install
npm i qtr-mcp-server