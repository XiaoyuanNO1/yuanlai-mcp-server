# 🚀 Render 部署快速清单

## 📋 第一步：在 Render 部署服务（5分钟）

### 1. 注册并连接 GitHub
- 访问：https://render.com
- 点击 **"Sign up with GitHub"**
- 授权 Render 访问你的 GitHub

### 2. 创建 Web Service
- 点击 **"New +"** → **"Web Service"**
- 选择仓库：`yuanlai-mcp-server`
- 点击 **"Connect"**

### 3. 确认配置（自动检测）
- Plan: **Free** ✅
- 点击 **"Create Web Service"**

### 4. 等待部署（2-3分钟）
- 状态变为 **"Live"** 表示成功
- 复制你的服务 URL：`https://yuanlai-mcp-server-xxxx.onrender.com`

### 5. 测试服务
访问：`https://你的域名/health`

应该看到：
```json
{"status": "healthy", "service": "yuanlai-company-agent", ...}
```

---

## 📋 第二步：在 Knot 配置 MCP（3分钟）

### 1. 创建 MCP

访问：https://knot.woa.com → "MCP 管理" → "新建 MCP Server"

#### 基本信息填写

| 字段 | 填写内容 |
|------|---------|
| MCP 名称 | `元来如此公司智能Agent集群` |
| Server Name | `yuanlai-company-agent` |
| MCP 类型 | `Streamable HTTP` |
| URL 地址 | `https://你的Render域名/mcp` ⚠️ |
| 超时时间 | `60` |
| 安全区域 | `公网 (public)` ⚠️ |

⚠️ **重要**：
- URL 地址要加 `/mcp` 后缀
- 安全区域必须选 `public`（公网）

#### MCP 配置 JSON

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "public",
      "url": "https://你的Render域名/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

⚠️ 替换 `你的Render域名` 为实际域名

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

### 2. 测试连接
- 点击 **"检测"** 按钮
- 应该显示 ✅ **连接成功**
- 点击 **"确认"** 保存

---

## 📋 第三步：创建 Agent（2分钟）

在 Knot 平台：**"智能体管理"** → **"创建智能体"**

### 基本信息

| 字段 | 填写内容 |
|------|---------|
| 智能体名称 | `元来如此公司助手` |
| 智能体描述 | `元来如此公司的智能助手，可以查询财务、人力资源、研发项目等信息` |
| 智能体类型 | `对话助手` |

### 系统提示词

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

### 工具配置

- 启用 MCP：`yuanlai-company-agent` ✅
- 确认 4 个工具已加载

### 保存并发布

点击 **"保存"** → **"发布"**

---

## 📋 第四步：在企微测试（1分钟）

### 测试 1：人力资源查询
```
老李的职级是多少？
```

### 测试 2：财务查询
```
公司有什么负债？
```

### 测试 3：综合查询
```
公司整体情况怎么样？
```

---

## ✅ 完成！

总耗时：**约 10 分钟**

现在你可以在企微中使用"元来如此公司助手"了！🎉

---

## 💡 常见问题

### Q1: Render 服务休眠了怎么办？
**A**: 首次请求需要 30 秒唤醒，这是免费套餐的正常现象。如果希望始终在线，可以使用 UptimeRobot 每 5 分钟 ping 一次。

### Q2: Knot 连接测试失败？
**A**: 检查：
- URL 是否有 `/mcp` 后缀
- 安全区域是否选择 `public`
- Render 服务是否处于 "Live" 状态

### Q3: 如何更新代码？
**A**: 直接 push 到 GitHub，Render 会自动重新部署。

---

## 📚 详细文档

查看完整指南：`RENDER_DEPLOY_GUIDE.md`
