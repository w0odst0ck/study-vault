# study-vault 跨设备同步 · 部署指南

用 Cloudflare Workers + KV 实现**秒级跨设备复习同步**，同时 GitHub PAT 不再暴露在浏览器中。

## 架构

```
┌──────────┐  GET/PUT /state  ┌──────────────┐  KV（全局秒级）
│ 浏览器 A  │ ───────────────→  │  CF Worker   │ ────────→  ☁️ 复习状态
│ (手机)   │ ←──────────────── │  (代理层)    │ ←────────  持久化
└──────────┘                  └──────┬───────┘
                                     │ POST /push-to-github
                                     ↓
┌──────────┐                  ┌──────────────┐
│ 浏览器 B  │ ──→ Worker ──→  │  GitHub API  │ → main → Actions → Pages
│ (电脑)   │                  │  (PAT 在服务  │
└──────────┘                  └──────────────┘
```

## 部署步骤

### 1. 创建 KV 命名空间

在 Cloudflare Dashboard → Workers & Pages → KV → 创建命名空间：

- **名称:** `STUDY_VAULT`（随意）

记下命名空间 ID，稍后绑定用。

### 2. 部署 Worker

```bash
# 安装 wrangler
npm install -g wrangler

# 登录
wrangler login

# 进入项目
cd /path/to/study-vault
```

创建 `wrangler.toml`：

```toml
name = "study-vault-sync"
main = "scripts/sync-worker.js"
compatibility_date = "2025-04-01"

[[kv_namespaces]]
binding = "STUDY_VAULT"
id = "粘贴你的 KV 命名空间 ID"

[vars]
AUTH_KEY = "生成一个随机字符串（如 openssl rand -hex 16）"
GITHUB_REPO = "w0odst0ck/study-vault"
```

**设置 GITHUB_PAT 为 secret（不会暴露在代码中）：**

```bash
# 生成一个 fine-grained PAT（repo contents: write）
# 然后设为 Worker secret
echo "你的PAT" | wrangler secret put GITHUB_PAT
```

**部署：**

```bash
wrangler deploy
```

部署成功后你会得到一个 Worker URL，如：
```
https://study-vault-sync.你的用户名.workers.dev
```

验证健康检查：

```bash
curl https://study-vault-sync.你的用户名.workers.dev/HEALTH_AUTH_KEY/health
# → {"ok":true,"ts":"2026-07-24T..."}
```

### 3. 修改 `site/review/app.js` 配置

打开 `site/review/app.js`，开头的常量区：

```js
const WORKER_URL = 'https://study-vault-sync.你的用户名.workers.dev';
const AUTH_KEY = '你在 wrangler.toml 里设的 AUTH_KEY';
```

### 4. 部署复习站

提交推送 `main`，GitHub Actions 会自动部署到 Pages。

此后任何设备的复习数据都会：
- ✅ **每次评分后自动同步**到 KV（秒级，防抖 5 秒或 10 张）
- ✅ **每次打开页面自动拉取**云端最新状态
- ✅ **点击"推送仓库"** 将 KV 状态写入 GitHub（触发 Pages 部署）

## 冲突处理

每个卡片按 `last_reviewed` 时间戳合并，**新覆盖旧**。

- 手机评了卡 A（2026-07-24T09:00）
- 电脑评了卡 B（2026-07-24T09:05）
- 两个设备下次加载 → 两张卡的最新状态都在

如果几乎同时评了同一张卡，后提交的覆盖先提交的。单人使用场景足够。

## 费用说明

| 项目 | 免费额度 | 预估用量 | 费用 |
|------|---------|---------|------|
| Workers 请求 | 10 万/天 | ～50 次/天 | $0 |
| KV 读写 | 10 万次/天 | ～100 次/天 | $0 |
| KV 存储 | 1 GB | < 1 MB | $0 |

**总费用：$0**

## 回退方案

如果 Worker 不可用，复习站**完全离线可用**：

- 本地 localStorage 是主存储
- Worker/KV 是辅助桥接层
- 网络断开时正常复习，恢复后自动同步

## 其他

新的 PAT 不再嵌入 `app.js`，而是存在 Worker 的 secret 环境变量中。
现有 `app.js` 中的 PAT 已从代码中移除。
