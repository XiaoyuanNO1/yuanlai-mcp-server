# Knot 平台 POC 部署 - 填写内容清单

## ⚠️ 使用说明
本文档列出了在 Knot 平台创建 MCP 时需要填写的所有内容。
请将 `你的DevCloud服务器IP` 替换为实际的 IP 地址。

---

## 📝 第一步：DevCloud 部署

### 1. 获取服务器 IP
```bash
# 在 DevCloud 服务器上执行
hostname -I
```
**记录 IP 地址**：________________（例如：10.141.8.253）

### 2. 启动服务
```bash
git clone https://github.com/XiaoyuanNO1/yuanlai-mcp-server.git
cd yuanlai-mcp-server
bash start_server.sh
```

### 3. 验证服务
```bash
curl http://localhost:8080/health
```

---

## 📝 第二步：Knot 创建 MCP

访问：https://knot.woa.com → MCP 管理 → 新建 MCP

### 基本信息

| 字段 | 填写内容 |
|------|---------|
| MCP 名称 | `元来如此公司智能Agent集群` |
| Server Name | `yuanlai-company-agent` |
| 描述 | `支持财务、人力资源、研发三个子 Agent 的智能调度` |
| MCP 类型 | `Streamable HTTP` |
| URL 地址 | `http://你的IP:8080/mcp` |
| 超时时间 | `60` |
| 安全区域 | `开发网络 (devnet)` |

### MCP 配置 JSON

**复制以下内容并粘贴（记得替换 IP）：**

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "devnet",
      "url": "http://你的IP:8080/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

### 工具定义 JSON

**复制以下内容并粘贴：**

```json
{
  "tools": [
    {
      "name": "query_finance",
      "description": "查询公司财务数据（收入、利润、负债、资产等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体财务情况）"
          }
        }
      }
    },
    {
      "name": "query_hr",
      "description": "查询人力资源数据（员工信息、职级、薪资等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体人力情况）"
          }
        }
      }
    },
    {
      "name": "query_rd",
      "description": "查询研发项目数据（项目进度、团队规模等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体项目情况）"
          }
        }
      }
    },
    {
      "name": "query_company",
      "description": "智能综合查询，自动识别意图并调用相应的子 Agent（推荐使用）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（必填）"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

---

## 📝 第三步：Knot 创建 Agent

访问：https://knot.woa.com → 创建 Agent

### 基本信息

| 字段 | 填写内容 |
|------|---------|
| Agent 名称 | `元来如此公司助手` |
| 描述 | `公司智能助手，可查询财务、人力、研发信息` |
| 类型 | `智能体` |

### 系统提示词

**复制以下内容并粘贴：**

```
你是"元来如此"公司的智能助手，名字叫"小小元"。

你可以帮助用户查询公司的以下信息：
1. 财务数据：收入、利润、负债、资产等
2. 人力资源：员工信息、职级、薪资等
3. 研发项目：项目进度、团队规模等

当用户提问时，你应该：
1. 识别用户的问题类型
2. 调用相应的工具获取信息
3. 以友好、清晰的方式回答用户

对话风格：轻松、友好，可以使用表情😊
```

### 工具配置

- ✅ 勾选启用 `yuanlai-company-agent`
- 确认 4 个工具已加载：
  - query_finance
  - query_hr
  - query_rd
  - query_company

---

## 📝 第四步：企微测试

### 测试用例

**测试 1：单领域查询**
```
老李的职级是多少？
```

**测试 2：跨领域查询**
```
公司经营情况怎么样？另外在做什么项目呢？
```

**测试 3：综合查询**
```
公司整体情况如何？
```

**测试 4：超出范围**
```
今天天气怎么样？
```

---

## ✅ 检查清单

- [ ] DevCloud 服务器已启动（端口 8080）
- [ ] 健康检查通过（curl http://localhost:8080/health）
- [ ] Knot MCP 创建成功
- [ ] Knot MCP 连接测试通过
- [ ] Knot Agent 创建成功
- [ ] Agent 已启用 MCP 工具
- [ ] 企微测试通过

---

## 🔧 快速故障排查

### 连接失败？
```bash
# 检查服务是否运行
ps aux | grep yuanlai_mcp_server_knot.py

# 检查端口是否监听
netstat -tlnp | grep 8080

# 测试本地访问
curl http://localhost:8080/health
```

### IP 地址忘记了？
```bash
hostname -I
```

---

## 📞 需要帮助？

- GitHub: https://github.com/XiaoyuanNO1/yuanlai-mcp-server
- 详细部署指南: 查看 KNOT_POC_DEPLOYMENT_GUIDE.md
