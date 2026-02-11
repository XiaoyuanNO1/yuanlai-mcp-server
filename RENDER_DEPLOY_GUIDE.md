# 🚀 在 Render 上部署 MCP Server（免费方案）

## 📋 部署步骤

### 第一步：注册 Render 账号

1. 访问：https://render.com
2. 点击右上角 **"Get Started"** 或 **"Sign Up"**
3. 选择 **"Sign up with GitHub"**（推荐）
4. 授权 Render 访问你的 GitHub 账号

---

### 第二步：创建 Web Service

1. 登录后，点击 **"New +"** 按钮
2. 选择 **"Web Service"**
3. 在仓库列表中找到 **`yuanlai-mcp-server`**
   - 如果看不到，点击 **"Configure account"** 授权访问
4. 点击 **"Connect"**

---

### 第三步：配置服务

Render 会自动检测到 `render.yaml` 配置文件，你只需确认：

| 配置项 | 值 |
|--------|-----|
| **Name** | `yuanlai-mcp-server` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python yuanlai_mcp_server_knot.py 8080` |
| **Plan** | `Free` ✅ |

点击 **"Create Web Service"**

---

### 第四步：等待部署

- Render 会自动：
  1. 克隆你的 GitHub 仓库
  2. 安装依赖
  3. 启动服务
  4. 生成公网 URL

- 部署时间：约 2-3 分钟
- 状态显示 **"Live"** 表示部署成功 ✅

---

### 第五步：获取服务 URL

部署成功后，你会看到类似这样的 URL：

```
https://yuanlai-mcp-server.onrender.com
```

📝 **复制这个 URL**，后面在 Knot 配置时需要用到！

---

### 第六步：测试服务

在浏览器访问：

```
https://yuanlai-mcp-server.onrender.com/health
```

应该看到：

```json
{
  "status": "healthy",
  "service": "yuanlai-company-agent",
  "version": "1.0.0",
  "timestamp": "2026-02-11T16:19:22Z"
}
```

✅ 如果看到这个响应，说明服务正常运行！

---

## 🔧 在 Knot 平台配置

### 1. 创建 MCP

访问：https://knot.woa.com

#### 基本信息

| 字段 | 填写内容 |
|------|---------|
| **MCP 名称** | `元来如此公司智能Agent集群` |
| **Server Name** | `yuanlai-company-agent` |
| **MCP 类型** | `Streamable HTTP` |
| **URL 地址** | `https://yuanlai-mcp-server.onrender.com/mcp` ⚠️ 替换为你的实际 URL |
| **超时时间** | `60` |
| **安全区域** | `公网 (public)` ⚠️ 注意选择公网 |

#### MCP 配置 JSON

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "public",
      "url": "https://yuanlai-mcp-server.onrender.com/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

⚠️ **重要**：将 `yuanlai-mcp-server.onrender.com` 替换为你的实际域名！

#### 工具定义 JSON

```json
{
  "tools": [
    {
      "name": "query_finance",
      "description": "查询元来如此公司的财务数据，包括营业收入、利润、资产、负债等信息",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "财务相关的查询问题"
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "query_hr",
      "description": "查询元来如此公司的人力资源数据，包括员工信息、职级、薪资、入职时间等",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "人力资源相关的查询问题"
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "query_rd",
      "description": "查询元来如此公司的研发项目数据，包括项目名称、进度、负责人、技术栈等",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "研发项目相关的查询问题"
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "query_company",
      "description": "智能查询元来如此公司的综合信息，自动识别问题类型并调用相应的子Agent（财务、人力资源、研发），支持跨领域查询",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "关于公司的任何问题，系统会自动识别并调用相应的子Agent"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

点击 **"检测"** 测试连接 → 应该显示 ✅ **连接成功**

点击 **"确认"** 保存配置

---

### 2. 创建 Agent

#### 基本信息

| 字段 | 填写内容 |
|------|---------|
| **智能体名称** | `元来如此公司助手` |
| **智能体描述** | `元来如此公司的智能助手，可以查询财务、人力资源、研发项目等信息` |
| **智能体类型** | `对话助手` |

#### 系统提示词

```
你是"元来如此"公司的智能助手，可以帮助用户查询公司的各类信息。

你可以回答以下类型的问题：
1. 财务相关：营业收入、利润、资产、负债等
2. 人力资源：员工信息、职级、薪资、入职时间等
3. 研发项目：项目进度、负责人、技术栈等

当用户提问时，你会：
1. 识别问题类型（财务/人力/研发/综合）
2. 调用相应的工具获取信息
3. 以友好、专业的方式回答

对于超出服务范围的问题，你会礼貌地告知用户。
```

#### 工具配置

- 启用 MCP：`yuanlai-company-agent`
- 确认 4 个工具已加载：
  - ✅ query_finance
  - ✅ query_hr
  - ✅ query_rd
  - ✅ query_company

点击 **"保存"** 并 **"发布"**

---

## 🎮 在企微中测试

### 测试用例 1：人力资源查询

**提问**：
```
老李的职级是多少？
```

**预期回复**：
```
老李是 P15 职级，月薪 88,888 元，2019年1月15日入职，已经工作 7 年了。
```

---

### 测试用例 2：财务查询

**提问**：
```
公司有什么负债？
```

**预期回复**：
```
元来如此公司目前的负债情况：
- 短期借款：500万元
- 应付账款：300万元
- 总负债：800万元
```

---

### 测试用例 3：综合查询

**提问**：
```
公司整体情况怎么样？
```

**预期回复**：
```
元来如此公司整体情况良好：

【财务情况】
- 营业收入：5000万元
- 净利润：800万元
- 总资产：3000万元

【人力资源】
- 总人数：50人
- 核心骨干：老张（P16）、老李（P15）等

【研发项目】
- 智能运维平台：进度 85%
- 智能Agent框架：进度 45%
```

---

## 💡 Render 免费套餐说明

### ✅ 优点

- **完全免费**：无需信用卡
- **自动部署**：GitHub 推送自动更新
- **HTTPS 支持**：自动配置 SSL 证书
- **公网访问**：可以从任何地方访问

### ⚠️ 限制

- **休眠机制**：15 分钟无请求会自动休眠
  - 下次请求时需要 30 秒左右唤醒
  - 对于 POC 测试完全够用
- **每月 750 小时**：免费运行时间（约 31 天）
- **带宽限制**：100GB/月（对 MCP Server 完全够用）

### 💡 避免休眠的方法（可选）

如果你希望服务始终在线，可以：

1. **使用 UptimeRobot**（免费）：
   - 访问：https://uptimerobot.com
   - 添加监控：每 5 分钟 ping 一次你的服务
   - 这样服务就不会休眠

2. **在 GitHub Actions 中添加定时任务**：
   - 每 10 分钟自动访问一次健康检查接口

---

## 🔧 故障排查

### 问题 1：部署失败

**检查**：
- Render 日志中是否有错误信息
- `requirements.txt` 是否正确
- Python 版本是否兼容

**解决**：
- 查看 Render Dashboard 的 "Logs" 标签
- 根据错误信息调整配置

---

### 问题 2：Knot 连接失败

**检查**：
- URL 是否正确（注意 `/mcp` 后缀）
- 安全区域是否选择 `public`
- 服务是否处于 "Live" 状态

**解决**：
- 访问 `https://你的域名/health` 确认服务运行
- 在 Knot 中重新测试连接

---

### 问题 3：服务响应慢

**原因**：
- 免费套餐的服务休眠了
- 首次请求需要 30 秒唤醒

**解决**：
- 使用 UptimeRobot 保持服务活跃
- 或者接受首次请求较慢的情况（POC 测试可接受）

---

## 📊 方案对比

| 特性 | Render（推荐） | DevCloud |
|------|---------------|----------|
| 访问性 | ✅ 公网可访问 | ❌ 需要内网 |
| 部署难度 | ✅ 一键部署 | ⚠️ 需要配置 |
| 费用 | ✅ 完全免费 | ⚠️ 可能收费 |
| HTTPS | ✅ 自动配置 | ❌ 需要手动 |
| 自动更新 | ✅ GitHub 集成 | ❌ 需要手动 |
| 适合场景 | ✅ POC 测试 | ⚠️ 生产环境 |

---

## 🎯 总结

使用 Render 部署的优势：

1. ✅ **零门槛**：无需 DevCloud 访问权限
2. ✅ **快速部署**：5 分钟完成
3. ✅ **公网访问**：Knot 可以直接连接
4. ✅ **完全免费**：适合 POC 测试
5. ✅ **自动更新**：GitHub 推送自动部署

**Neil，现在你可以完全通过 GitHub + Render 来完成 POC 测试了！** 🎉
